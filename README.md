# Personal Website

This repository contains my personal website built with [Hugo](https://gohugo.io/) and the [Blowfish](https://blowfish.page/) theme.

## Getting Started

### Prerequisites

- [Hugo Extended](https://gohugo.io/installation/) (latest version recommended)

### Installation

1. Clone this repository with submodules:
   ```bash
   git clone --recurse-submodules https://github.com/3sztof/3sztof.github.io.git
   cd 3sztof.github.io
   ```

2. Start the local development server:
   ```bash
   hugo server -D
   ```

   This will start a local server at http://localhost:1313/ with draft posts enabled.

## Project Structure

- `content/` - All website content (posts, pages)
- `assets/` - CSS, JavaScript, and images used in templates
- `config/` - Hugo configuration files
- `themes/blowfish/` - The Blowfish theme (git submodule)
- `public/` - Built site (generated when running `hugo`)

## Deployment

This site deploys automatically to GitHub Pages when changes are pushed to the main branch. The GitHub Actions workflow:

1. Checks out the repository (including submodules)
2. Sets up Hugo Extended
3. Builds the site
4. Deploys to the `gh-pages` branch

## Updating the Theme

The Blowfish theme is managed as a git submodule pointing to the upstream repository:

```bash
# Update the submodule to the latest upstream commit
git submodule update --remote themes/blowfish

# Review and commit the pointer bump
git add themes/blowfish
git commit -S -m "chore: update blowfish theme"
```

## Development with DevContainer

This repository includes a DevContainer configuration for VS Code backed by a custom `Dockerfile`. It sets up a full development environment automatically, including:

- Hugo Extended
- Zsh with Powerlevel10k, zsh-autosuggestions, zsh-syntax-highlighting
- atuin (shell history), zoxide, fzf, eza, bat, fd
- gh CLI with shell completion
- OpenCode

To use it, open the repository in VS Code and select **Reopen in Container** when prompted (requires the Dev Containers extension).
