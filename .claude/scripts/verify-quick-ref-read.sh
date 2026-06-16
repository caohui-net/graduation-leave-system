#!/bin/bash
# 验证是否已读取快速文档的辅助脚本
# 用法: source verify-quick-ref-read.sh before-file-op

QUICK_REF="PROJECT-QUICK-REF.md"
SESSION_MARKER="/tmp/quick-ref-read-$$"

if [ "$1" = "before-file-op" ]; then
    if [ ! -f "$SESSION_MARKER" ]; then
        echo "❌ ERROR: Must read $QUICK_REF first!"
        echo "Execute: cat $QUICK_REF"
        exit 1
    fi
fi

if [ "$1" = "mark-read" ]; then
    touch "$SESSION_MARKER"
    echo "✓ Quick reference marked as read for session $$"
fi

if [ "$1" = "check" ]; then
    if [ -f "$SESSION_MARKER" ]; then
        echo "✓ Quick reference already read in this session"
    else
        echo "⚠ Quick reference not yet read in this session"
    fi
fi
