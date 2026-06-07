#!/usr/bin/env python3
"""
检查研究生Excel文件是否存在并分析结构
"""
import os
import sys

# 检查文件
file_path = "docs/硕士研究生-毕业生290人.xls"

if os.path.exists(file_path):
    file_size = os.path.getsize(file_path)
    print(f"✓ 文件存在: {file_path}")
    print(f"  文件大小: {file_size:,} bytes ({file_size/1024:.1f} KB)")

    # 尝试用LibreOffice转换
    print("\n需要LibreOffice将XLS转换为CSV进行分析")
    print("建议执行: libreoffice --headless --convert-to csv --outdir /tmp docs/硕士研究生-毕业生290人.xls")
else:
    print(f"✗ 文件不存在: {file_path}")
    print("\n搜索包含'研究生'的文件:")
    os.system("find docs -name '*研究生*' -type f 2>/dev/null || echo '无搜索结果'")
