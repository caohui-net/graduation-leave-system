#!/bin/bash
# 安装Git Hooks到本地仓库
# 执行: ./scripts/install-hooks.sh

set -e

HOOKS_DIR="$(git rev-parse --show-toplevel)/scripts/git-hooks"
GIT_HOOKS_DIR="$(git rev-parse --git-dir)/hooks"

echo "安装Git Hooks..."

for hook in "$HOOKS_DIR"/*; do
  hook_name=$(basename "$hook")
  chmod +x "$hook"
  cp "$hook" "$GIT_HOOKS_DIR/$hook_name"
  echo "  ✓ $hook_name"
done

echo "✅ Git Hooks安装完成"
