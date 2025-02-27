---
title: "Suggest Edits"
date: 2025-02-27
draft: false
description: "How to suggest edits and improvements for this website"
tags: ["about", "github", "contributions", "edit"]
---

## Help Improve This Website

This website is open-source and available on GitHub at [3sztof/3sztof.github.io](https://github.com/3sztof/3sztof.github.io). Suggestions, corrections, and improvements are always welcome! If you've found a typo, have an idea for new content, or want to suggest improvements, there are several ways to contribute.

## How to Suggest Edits

### Option 1: Opening a GitHub Issue

The easiest way to suggest changes is by opening a GitHub issue. You can use our issue templates to make the process easier:

#### Quick Links to Create an Issue:

- [📝 Suggest Content Change or Correction](https://github.com/3sztof/3sztof.github.io/issues/new?assignees=&labels=content&projects=&template=content-suggestion.md&title=%5BCONTENT%5D+)
- [🐛 Report a Bug or Display Issue](https://github.com/3sztof/3sztof.github.io/issues/new?assignees=&labels=bug&projects=&template=bug-report.md&title=%5BBUG%5D+)
- [🆓 Open a Blank Issue](https://github.com/3sztof/3sztof.github.io/issues/new)

#### Manual Process:

1. **Go to the repository**: Visit [https://github.com/3sztof/3sztof.github.io](https://github.com/3sztof/3sztof.github.io)

2. **Navigate to Issues**: Click on the "Issues" tab near the top of the repository page

3. **Create a new issue**: Click the green "New issue" button and select an appropriate template

4. **Provide details**: 
   - Use a clear, descriptive title 
   - Fill in the template with specific information about your suggestion
   - Include the URL of the page you're referring to
   - For content corrections, include both the current text and your suggested revision
   - You can use Markdown formatting in your issue description

5. **Submit**: Click "Submit new issue"

### Example Issue

Here's an example of a well-formatted issue:

```
Title: Typo on About page - "descriptn" should be "description"

Description:
On the About page (https://3sztof.github.io/about/page/), 
there's a typo in the second paragraph:

Current text: "TODO: add a descriptn how this site is built"
Suggested change: "TODO: add a description how this site is built"
```

### Option 2: Creating a Pull Request

If you're comfortable with Git and Hugo, you can directly propose changes by:

1. **Fork the repository**: Click the "Fork" button at the top right of the repository page

2. **Clone your fork**: 
   ```bash
   git clone https://github.com/YOUR-USERNAME/3sztof.github.io.git
   ```

3. **Create a branch**:
   ```bash
   git checkout -b fix-typo
   ```

4. **Make your changes**: Edit the relevant files

5. **Commit and push**:
   ```bash
   git commit -am "Fix typo in about page"
   git push origin fix-typo
   ```

6. **Create a pull request**: Go to the [original repository](https://github.com/3sztof/3sztof.github.io/compare) and click "New pull request", then select your branch

   The pull request will automatically use our [PR template](https://github.com/3sztof/3sztof.github.io/blob/main/.github/PULL_REQUEST_TEMPLATE.md) to help you provide all necessary information

## Content Guidelines

When suggesting content changes, please:

- Keep the same writing style as the rest of the site
- Ensure technical accuracy
- Include references or sources if adding new information
- Follow the existing formatting conventions

## Thank You!

Your contributions help make this site better for everyone. Thank you for taking the time to suggest improvements!