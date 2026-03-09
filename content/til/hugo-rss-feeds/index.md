---
title: "Hugo generates RSS feeds automatically"
date: 2026-03-09
description: "Hugo generates RSS 2.0 feeds for every section out of the box - no plugin needed"
tags: ["hugo", "rss", "static-sites"]
categories: ["TIL"]
---

If you add `RSS` to your Hugo output formats, you get a valid RSS 2.0 feed at `/index.xml` (site-wide) and `/<section>/index.xml` for each content section - for free, no plugin or extra config required.

The Blowfish theme even ships a custom RSS template that includes featured images via `<media:content>` and a `<follow_challenge>` block for [Follow.is](https://follow.is/) integration.
