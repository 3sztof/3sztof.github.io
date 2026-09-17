---
title: "Sending .ics calendar invites via AWS SES from a Python Lambda"
date: 2026-08-04
description: "The Python email.mime approach for sending ICS attachments through SES is underdocumented and has several non-obvious gotchas. Here's a working pattern."
tags: ["aws", "ses", "ics", "calendar", "python", "lambda"]
categories: ["Posts"]
draft: false
---

The project that forced me to figure all of this out is **Collide** - a serverless app I built in my free time that randomly pairs colleagues for short meetings to cut the social friction of large offices. I've written up [the whole story](/posts/virtual-coffee-the-story/) and [how it's built](/posts/openspec-agentic-dev/) separately; the short version is that every week the system matches pairs and trios, then emails each group a meeting invitation with a calendar block, a suggested time, and AI-generated conversation starters. It's not open-source yet, but I plan to eventually put it up on [my GitHub](https://github.com/3sztof).

Sending a calendar invite sounds trivial until you try to do it properly. The invite needs to render correctly in Gmail, Apple Mail, and Outlook. It needs to block the calendar, not just appear as an attachment. It needs to be reschedulable - meaning the reschedule email must update the existing calendar block rather than creating a duplicate. And it needs to work without any dependency on Microsoft Exchange, Google Workspace, or any other proprietary calendar infrastructure, because the whole system is designed to be deployable by anyone in any office without external company dependencies.

I also later discovered that SES can receive RSVP responses - attendees accepting or declining via their calendar client - which let me build central status tracking and proactive rescheduling suggestions entirely within the system. That's a separate post. But it only works if the original invite is correctly formed, which is where the pain lives.

## Why raw send

SES's `SendEmail` API handles text and HTML bodies but not arbitrary MIME attachments. As soon as you need a `.ics` file, you're on `SendRawEmail`, which takes a complete RFC 2822-formatted message as bytes. You construct it yourself with Python's `email` standard library.

## The structure that works

```python
import boto3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase

def build_invite_email(
    sender: str,
    recipients: list[str],
    subject: str,
    html_body: str,
    ics_content: str,
) -> MIMEMultipart:
    # Outer container - mixed allows body alternatives + attachment
    msg = MIMEMultipart("mixed")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)

    # Body: alternative allows HTML + plain text fallback
    body = MIMEMultipart("alternative")
    body.attach(MIMEText("Please view this email in an HTML-capable client.", "plain"))
    body.attach(MIMEText(html_body, "html"))
    msg.attach(body)

    # ICS attachment
    ics_part = MIMEBase("text", "calendar", method="REQUEST", charset="UTF-8")
    ics_part.set_payload(ics_content.encode("utf-8"))
    ics_part.add_header(
        "Content-Disposition",
        "attachment",
        filename="invite.ics",
    )
    msg.attach(ics_part)

    return msg


def send_via_ses(msg: MIMEMultipart, sender: str, recipients: list[str]) -> None:
    client = boto3.client("ses", region_name="eu-west-1")
    client.send_raw_email(
        Source=sender,
        Destinations=recipients,
        RawMessage={"Data": msg.as_bytes()},
    )
```

## The ICS content

A minimal `VEVENT` that actually works as a meeting invite across clients:

```python
from datetime import datetime, timezone

def build_ics(
    uid: str,
    summary: str,
    description: str,
    organizer_email: str,
    attendee_emails: list[str],
    start_dt: datetime,
    end_dt: datetime,
    location: str = "",
) -> str:
    def fmt(dt: datetime) -> str:
        return dt.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    attendees = "\r\n".join(
        f"ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-PARTICIPANT;"
        f"PARTSTAT=NEEDS-ACTION;RSVP=TRUE:mailto:{email}"
        for email in attendee_emails
    )

    return (
        "BEGIN:VCALENDAR\r\n"
        "VERSION:2.0\r\n"
        "PRODID:-//Collide//EN\r\n"
        "METHOD:REQUEST\r\n"
        "BEGIN:VEVENT\r\n"
        f"UID:{uid}\r\n"
        f"DTSTART:{fmt(start_dt)}\r\n"
        f"DTEND:{fmt(end_dt)}\r\n"
        f"SUMMARY:{summary}\r\n"
        f"DESCRIPTION:{description}\r\n"
        f"ORGANIZER:mailto:{organizer_email}\r\n"
        f"{attendees}\r\n"
        f"LOCATION:{location}\r\n"
        "STATUS:CONFIRMED\r\n"
        "SEQUENCE:0\r\n"
        "BEGIN:VALARM\r\n"
        "TRIGGER:-PT15M\r\n"
        "ACTION:DISPLAY\r\n"
        "DESCRIPTION:Reminder\r\n"
        "END:VALARM\r\n"
        "END:VEVENT\r\n"
        "END:VCALENDAR\r\n"
    )
```

## The gotchas - found the hard way

These came from my own testing, aided considerably by a group of early users who were vocal about every rough edge. Glory to the users.

**Line endings must be `\r\n` throughout.** RFC 5545 requires CRLF. Python strings default to `\n`. Gmail accepts `\n`, Apple Calendar mostly does, Outlook silently mangles or ignores the event. Every line in the ICS content - not just the separators, every single line - needs `\r\n`.

**`METHOD:REQUEST` is needed in two places.** The `METHOD:REQUEST` inside the `VCALENDAR` block tells calendar clients this is a meeting invitation rather than a static event. The `method="REQUEST"` parameter on the MIME Content-Type header (`MIMEBase("text", "calendar", method="REQUEST")`) tells the email client to present it as an actionable invite rather than an attachment. Both are required. Gmail handles the ICS-only case. Outlook requires both. This took several test rounds to pin down because the failure mode is silent - Outlook just shows a regular email with an attachment rather than an invite widget.

**`RSVP=TRUE` on the attendee line is what enables response tracking.** If you want to receive accept/decline responses back via SES (and track attendance centrally), the attendee needs `RSVP=TRUE`. Without it, some clients won't send a response at all even if the user clicks Accept.

**The `UID` must be stable across rescheduled invites.** When a meeting is rescheduled, you send a new invite with updated `DTSTART`/`DTEND` and an incremented `SEQUENCE` number. The `UID` must match the original exactly - that's how calendar clients know to update the existing block rather than create a second one. Generate it once (UUID4), store it on the match record, reuse it forever for that meeting.

**SES sandbox vs production.** Sandbox mode requires both sender and recipient to be verified. Production only requires the sender domain. Lambda IAM needs `ses:SendRawEmail` scoped to the sender identity ARN.

## Rescheduling

Increment `SEQUENCE`, keep the `UID`, update the times:

```python
# Original invite
"SEQUENCE:0\r\n"

# Reschedule
"SEQUENCE:1\r\n"
```

Most modern clients (Gmail, Apple Calendar, recent Outlook) update the existing block on receipt. Older Outlook versions are less reliable - if you need to support them, a `METHOD:CANCEL` followed by a fresh `METHOD:REQUEST` is more robust, but for most audiences the sequence increment is sufficient.

Collide doesn't send explicit cancellations - the initiative is opt-in by default, so a meeting that doesn't happen is just a meeting that didn't happen, no harm done. What it does instead: if any attendee declines, the match is flagged as "at risk" and the app surfaces a reschedule suggestion. Attendees can reschedule through the app, which sends a fresh invite with an incremented sequence. The calendar block updates, the meeting moves, nobody has to touch email manually.

- [RFC 5545 - iCalendar specification](https://datatracker.ietf.org/doc/html/rfc5545)
- [SES SendRawEmail API reference](https://docs.aws.amazon.com/ses/latest/APIReference/API_SendRawEmail.html)
- [Collide: how an introvert built a machine to meet people](/posts/virtual-coffee-the-story/) - the project this came from
- [The spec is the bottleneck, not the AI](/posts/openspec-agentic-dev/) - how Collide is built
