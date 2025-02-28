---
title: "About This Site"
date: 2025-02-27
draft: false
description: "How this site is built and deployed"
tags: ["about", "hugo", "blowfish", "github", "static-site", "nodejs", "github-actions", "web-development"]
---

This page was made with [Hugo](https://gohugo.io/) and [Blowfish](https://blowfish.page/), and is deployed on [GitHub Pages](https://pages.github.com/).

## Building Static Websites with Blowfish and Hugo

### Setup Process

While [Hugo](https://gohugo.io/) is the core framework that powers this site, Blowfish provides a convenient CLI tool called `blowfish-tools` that simplifies the setup process.

1. **Install prerequisites**:
   - First, [install Node.js](https://nodejs.org/) on your local machine
   - [Install Hugo](https://gohugo.io/installation/) as it's required by Blowfish

2. **Install Blowfish Tools**:
   ```bash
   npm install -g blowfish-tools
   ```

3. **Create a new site**:
   ```bash
   blowfish new site your-site-name
   cd your-site-name
   ```
   This command automatically initializes Git, installs the Blowfish theme, and sets up the recommended configuration.

4. **Create content**:
   ```bash
   blowfish new post "My First Post"
   ```
   This command creates a new post with the proper front matter already configured.

5. **Preview your site locally**:
   ```bash
   blowfish serve
   ```
   This starts the development server with live reload enabled.

For more detailed instructions and additional features, see the [Blowfish documentation](https://blowfish.page/docs/getting-started/). The Blowfish CLI tool makes it much easier to get started while still leveraging the full power of Hugo under the hood.

## Publishing on GitHub Pages

This site is deployed using GitHub Pages with a GitHub Actions workflow. The source code is available at [3sztof/3sztof.github.io](https://github.com/3sztof/3sztof.github.io).

### How It Works

1. **Repository Structure**:
   - `main` branch: Contains the source code (Hugo content, configuration, etc.)
   - `gh-pages` branch: Contains the generated static site that GitHub serves

2. **GitHub Actions Workflow**:
   - When changes are pushed to the `main` branch, a GitHub Actions workflow automatically:
     1. Checks out the code
     2. Sets up Hugo
     3. Builds the site
     4. Deploys the generated static files to the `gh-pages` branch

3. **Setting Up Your Own**:
   - Create a repository named `username.github.io`
   - Push your Hugo site to the `main` branch
   - Create a GitHub Actions workflow file at `.github/workflows/hugo.yml`
   - Configure GitHub Pages to serve from the `gh-pages` branch

For a complete example, check out the [workflow configuration in this site's repository](https://github.com/3sztof/3sztof.github.io).

This setup provides a smooth workflow where you only need to focus on creating content in the `main` branch, and the deployment happens automatically whenever you push changes.