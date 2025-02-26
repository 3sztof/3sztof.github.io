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

2. Initialize and update the theme submodule:
   ```bash
   git submodule init
   git submodule update
   ```
   
   Alternatively, clone with submodules in one command:
   ```bash
   git clone --recurse-submodules https://github.com/3sztof/3sztof.github.io.git
   ```

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
- `themes/blowfish/` - The Blowfish theme (as a git submodule)
- `public/` - Built site (generated when running `hugo`)

## Deployment

This site is set up to deploy automatically to GitHub Pages when changes are pushed to the main branch. The GitHub Actions workflow:

1. Checks out the repository (including submodules)
2. Sets up Hugo
3. Builds the site
4. Deploys to the gh-pages branch

## Updating the Theme

To update the Blowfish theme to the latest version:

```bash
cd themes/blowfish
git pull origin main
cd ../..
```

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

*This README was generated with [Claude Code](https://console.anthropic.com/claude/cli) (Claude 3.7) on February 26, 2025.*