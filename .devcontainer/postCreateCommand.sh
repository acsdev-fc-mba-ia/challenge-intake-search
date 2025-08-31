#!/bin/zsh

# --- Set the Zsh theme ---
sed -i 's/ZSH_THEME="devcontainers"/ZSH_THEME="strug"/' "/$HOME/.zshrc"

# --- Any other setup tasks ---
echo "Dev container setup complete!"