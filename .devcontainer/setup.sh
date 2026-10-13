#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "--- opencode ---"
OPENCODE_BIN="$HOME/.opencode/bin"
if ! command -v opencode &>/dev/null && [ ! -x "$OPENCODE_BIN/opencode" ]; then
    curl -fsSL https://opencode.ai/install | bash
    if ! grep -qF "$OPENCODE_BIN" "$HOME/.bashrc" 2>/dev/null; then
        echo "export PATH=\"$OPENCODE_BIN:\$PATH\"" >> "$HOME/.bashrc"
    fi
fi

echo "--- zsh ---"
ZSH_CUSTOM="${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}"
for plugin in zsh-autosuggestions zsh-syntax-highlighting; do
    if [ ! -d "$ZSH_CUSTOM/plugins/$plugin" ]; then
        git clone --depth=1 "https://github.com/zsh-users/$plugin" \
            "$ZSH_CUSTOM/plugins/$plugin"
        echo "  cloned: $plugin"
    fi
done
if [ ! -d "$ZSH_CUSTOM/themes/powerlevel10k" ]; then
    git clone --depth=1 https://github.com/romkatv/powerlevel10k.git \
        "$ZSH_CUSTOM/themes/powerlevel10k"
    echo "  cloned: powerlevel10k"
fi

cp "$SCRIPT_DIR/.zshrc" "$HOME/.zshrc"
cp "$SCRIPT_DIR/.p10k.zsh" "$HOME/.p10k.zsh"
echo "  wrote ~/.zshrc and ~/.p10k.zsh"

CURRENT_USER="$(id -un)"
CURRENT_SHELL="$(getent passwd "$CURRENT_USER" | cut -d: -f7)"
if [ "$CURRENT_SHELL" != "/usr/bin/zsh" ]; then
    sudo chsh -s /usr/bin/zsh "$CURRENT_USER"
    echo "  default shell -> zsh"
fi

git config --global --add safe.directory "${containerWorkspaceFolder:-/workspace}" 2>/dev/null || true

cat <<'EOF'

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  hugo blog devcontainer ready
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  hugo server    → http://localhost:1313  (port auto-forwarded)
  blowfish       → blowfish --help
  opencode       → opencode  (then /connect to configure model)
  gh auth login  → browser OAuth

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EOF
