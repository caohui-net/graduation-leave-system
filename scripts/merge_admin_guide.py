#!/usr/bin/env python3
"""合并管理员指南和流程图到主用户手册"""

import re

# 读取文件
with open('docs/用户操作手册.md', 'r', encoding='utf-8') as f:
    main_content = f.read()

with open('docs/管理员操作指南和流程图补充.md', 'r', encoding='utf-8') as f:
    supplement = f.read()

# 提取流程图部分（从"## 流程示意图"到"## 管理员操作指南"之间）
flow_diagrams_match = re.search(r'## 流程示意图.*?(?=## 管理员操作指南)', supplement, re.DOTALL)
flow_diagrams = flow_diagrams_match.group(0) if flow_diagrams_match else ""

# 提取管理员操作指南部分
admin_guide_match = re.search(r'## 管理员操作指南.*$', supplement, re.DOTALL)
admin_guide = admin_guide_match.group(0) if admin_guide_match else ""

# 插入流程图：在"## 学生操作指南"之前
insertion_point_flow = main_content.find('## 学生操作指南')
if insertion_point_flow > 0:
    main_content = (
        main_content[:insertion_point_flow] +
        flow_diagrams + "\n\n---\n\n" +
        main_content[insertion_point_flow:]
    )

# 插入管理员指南：在"## 常见问题"之前
insertion_point_admin = main_content.find('## 常见问题')
if insertion_point_admin > 0:
    main_content = (
        main_content[:insertion_point_admin] +
        admin_guide + "\n\n---\n\n" +
        main_content[insertion_point_admin:]
    )

# 更新目录
toc_old = """## 目录

1. [系统简介](#系统简介)
2. [学生操作指南](#学生操作指南)
3. [宿管员操作指南](#宿管员操作指南)
4. [辅导员操作指南](#辅导员操作指南)
5. [常见问题](#常见问题)"""

toc_new = """## 目录

1. [系统简介](#系统简介)
2. [流程示意图](#流程示意图)
3. [学生操作指南](#学生操作指南)
4. [宿管员操作指南](#宿管员操作指南)
5. [辅导员操作指南](#辅导员操作指南)
6. [管理员操作指南](#管理员操作指南)
7. [常见问题](#常见问题)"""

main_content = main_content.replace(toc_old, toc_new)

# 保存更新后的文档
with open('docs/用户操作手册.md', 'w', encoding='utf-8') as f:
    f.write(main_content)

print("✓ 流程图已插入")
print("✓ 管理员操作指南已插入")
print("✓ 目录已更新")
print("✓ docs/用户操作手册.md 更新完成")
