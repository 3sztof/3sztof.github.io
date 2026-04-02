# ============================================================
# Hugo Blog Devcontainer
# ============================================================
# Based on: https://github.com/3sztof/devcontainer
# Debian 12 (Bookworm) base, arch-aware (x86_64 + arm64).
FROM mcr.microsoft.com/devcontainers/base:debian-12

ARG DEBIAN_FRONTEND=noninteractive
ARG NODE_MAJOR="22"

# ============================================================
# Layer 1: System packages + GitHub CLI
# ============================================================
RUN echo "=== [1/4] System packages + GitHub CLI ===" \
    && apt-get update \
    && apt-get -y install --no-install-recommends \
        git \
        curl \
        ca-certificates \
        unzip \
        make \
        fzf \
        bat \
        ripgrep \
        fd-find \
        jq \
        htop \
    && echo "--- GitHub CLI ---" \
    && curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg \
        | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
    && chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" \
        > /etc/apt/sources.list.d/github-cli.list \
    && apt-get update \
    && apt-get -y install --no-install-recommends gh \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/* \
    && echo "=== [1/4] Done: gh $(gh --version | head -1) ==="

# ============================================================
# Layer 1b: Binary tools (zoxide + eza)
# ============================================================
RUN echo "=== [1b/4] zoxide + eza ===" \
    && ARCH=$(uname -m) \
    && case "$ARCH" in \
        aarch64|arm64) BIN_ARCH="aarch64" ;; \
        x86_64)        BIN_ARCH="x86_64"  ;; \
        *)             echo "Unsupported arch: $ARCH" && exit 1 ;; \
    esac \
    && echo "--- zoxide ---" \
    && ZOXIDE_VER="$(curl -fsSL https://api.github.com/repos/ajeetdsouza/zoxide/releases/latest | grep '"tag_name"' | cut -d'"' -f4 | sed 's/^v//')" \
    && curl -fsSL "https://github.com/ajeetdsouza/zoxide/releases/download/v${ZOXIDE_VER}/zoxide-${ZOXIDE_VER}-${BIN_ARCH}-unknown-linux-musl.tar.gz" \
        | tar -xz -C /tmp \
    && mv /tmp/zoxide /usr/local/bin/zoxide \
    && chmod +x /usr/local/bin/zoxide \
    && echo "--- eza ---" \
    && curl -fsSL "https://github.com/eza-community/eza/releases/latest/download/eza_${BIN_ARCH}-unknown-linux-gnu.tar.gz" \
        | tar -xz -C /tmp \
    && mv /tmp/eza /usr/local/bin/eza \
    && chmod +x /usr/local/bin/eza \
    && echo "=== [1b/4] Done: zoxide $(zoxide --version), eza $(eza --version | head -1) ==="

# ============================================================
# Layer 2: Hugo Extended (latest) + Node.js LTS
# ============================================================
RUN echo "=== [2/4] Hugo Extended ===" \
    && ARCH=$(uname -m) \
    && case "$ARCH" in \
        aarch64|arm64) HUGO_ARCH="arm64" ;; \
        x86_64)        HUGO_ARCH="amd64" ;; \
        *)             echo "Unsupported arch: $ARCH" && exit 1 ;; \
    esac \
    && HUGO_VER="$(curl -fsSL https://api.github.com/repos/gohugoio/hugo/releases/latest | grep '"tag_name"' | cut -d'"' -f4 | sed 's/^v//')" \
    && curl -fsSL "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VER}/hugo_extended_${HUGO_VER}_linux-${HUGO_ARCH}.deb" \
        -o /tmp/hugo.deb \
    && dpkg -i /tmp/hugo.deb \
    && rm /tmp/hugo.deb \
    && echo "=== [2/4] Done: $(hugo version) ===" \
    && echo "--- Node.js LTS ---" \
    && curl -fsSL https://deb.nodesource.com/setup_${NODE_MAJOR}.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/* \
    && echo "--- Node.js: $(node --version), npm: $(npm --version) ---" \
    && npm install -g blowfish-tools \
    && echo "=== [2/4] Done: blowfish $(blowfish --version 2>/dev/null || echo ok) ==="

# ============================================================
# Layer 3: OpenCode + atuin + zsh plugins + p10k (as vscode user)
# ============================================================
USER vscode

RUN echo "=== [3/4] OpenCode + atuin + zsh plugins ===" \
    && curl -fsSL https://opencode.ai/install | bash \
    && echo "export PATH=\"/home/vscode/.opencode/bin:\$PATH\"" >> /home/vscode/.bashrc \
    && echo "--- atuin ---" \
    && curl --proto '=https' --tlsv1.2 -LsSf https://setup.atuin.sh | sh -s -- --non-interactive \
    && echo "--- zsh plugins + p10k ---" \
    && ZSH_CUSTOM="/home/vscode/.oh-my-zsh/custom" \
    && git clone --depth=1 \
        https://github.com/zsh-users/zsh-autosuggestions \
        "$ZSH_CUSTOM/plugins/zsh-autosuggestions" \
    && git clone --depth=1 \
        https://github.com/zsh-users/zsh-syntax-highlighting \
        "$ZSH_CUSTOM/plugins/zsh-syntax-highlighting" \
    && git clone --depth=1 \
        https://github.com/romkatv/powerlevel10k.git \
        "$ZSH_CUSTOM/themes/powerlevel10k" \
    && sudo chsh -s /usr/bin/zsh vscode \
    && echo "=== [3/4] Done ==="

ENV PATH="/home/vscode/.opencode/bin:/home/vscode/.atuin/bin:${PATH}"

USER root

WORKDIR /workspace
