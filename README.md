# Personal Website

This repository contains my personal website built with [Hugo](https://gohugo.io/) and the [Blowfish](https://blowfish.page/) theme.

## Getting Started

### Prerequisites

- [Hugo Extended](https://gohugo.io/installation/) (latest version recommended)
- [Node.js and npm](https://nodejs.org/) (for Blowfish tools)

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/3sztof/3sztof.github.io.git
   cd 3sztof.github.io
   ```

2. No additional steps needed as the theme is included directly in the repository.

3. Install Blowfish tools:
   ```bash
   npm install -g blowfish-tools
   ```

### Development

To start the local development server:

```bash
hugo server -D
```

This will start a local server at http://localhost:1313/ with draft posts enabled.

### Using Blowfish Tools

Blowfish tools provide helpful commands for working with the Blowfish theme:

```bash
# Create a new post
blowfish new post "My New Post"

# Create a new page
blowfish new page "About Me"

# See all available commands
blowfish --help
```

## Project Structure

- `content/` - All website content (posts, pages)
- `assets/` - CSS, JavaScript, and images used in templates
- `config/` - Hugo configuration files
- `themes/blowfish/` - The Blowfish theme (included directly in the repository)
- `public/` - Built site (generated when running `hugo`)

## Deployment

This site is set up to deploy automatically to GitHub Pages when changes are pushed to the main branch. The GitHub Actions workflow:

1. Checks out the repository
2. Sets up Hugo
3. Builds the site
4. Deploys to the gh-pages branch

## Updating the Theme

Since the Blowfish theme is included directly in the repository (not as a submodule), use this process to update the theme:

```bash
# Navigate to the theme directory
cd themes/blowfish

# Add the upstream repository as a remote (only needed once)
git remote add upstream https://github.com/nunocoracao/blowfish.git

# Fetch the latest changes from the upstream repository
git fetch upstream

# Apply the updates (choose one approach)
# Option 1: Merge all upstream changes
git merge upstream/main

# Option 2: Create a branch to review changes first (recommended)
git checkout -b theme-update
git merge upstream/main
# After reviewing, merge the branch to main

# Option 3: Cherry-pick specific commits
git log --oneline upstream/main
git cherry-pick <commit-hash>

# Return to the project root
cd ../..
```

After updating the theme, test locally before committing and pushing the changes.

## Development with VS Code DevContainer

This repository includes a DevContainer configuration for VS Code that includes:

1. Hugo with extended features
2. Node.js for Blowfish tools
3. Port forwarding for the Hugo development server

To use it:
1. Install the Remote - Containers extension in VS Code
2. Open the repository in a container
3. The development environment will be automatically set up

## License

[MIT](LICENSE)

---

*This README was updated with [Claude Code](https://console.anthropic.com/claude/cli) (Claude 3.7) on February 26, 2025.*