export ZSH="$HOME/.oh-my-zsh"

ZSH_THEME="powerlevel10k/powerlevel10k"

zstyle ':omz:update' mode disabled

plugins=(
    git
    zsh-autosuggestions
    zsh-syntax-highlighting
)

source "$ZSH/oh-my-zsh.sh"

ZSH_AUTOSUGGEST_STRATEGY=(history completion)
ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE="fg=244"

export PATH="/home/vscode/.opencode/bin:/home/vscode/.atuin/bin:$PATH"

[[ -f ~/.p10k.zsh ]] && source ~/.p10k.zsh

eval "$(atuin init zsh)"

eval "$(zoxide init zsh)"

source /usr/share/doc/fzf/examples/key-bindings.zsh 2>/dev/null || true
source /usr/share/doc/fzf/examples/completion.zsh   2>/dev/null || true

alias ls='eza --icons'
alias ll='eza -la --icons --git'
alias lt='eza --tree --icons --level=2'
alias la='eza -la --icons'

alias cat='batcat --paging=never'
alias bat='batcat'

alias fd='fdfind'

if command -v gh &>/dev/null; then
    eval "$(gh completion -s zsh)"
fi
