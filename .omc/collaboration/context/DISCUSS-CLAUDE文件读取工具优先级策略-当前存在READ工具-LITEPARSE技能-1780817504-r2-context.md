# Discussion Context

**Task:** DISCUSS-CLAUDE文件读取工具优先级策略-当前存在READ工具-LITEPARSE技能-1780817504
**Round:** 2

## Topic

Claude文件读取工具优先级策略：当前存在Read工具、liteparse技能（本地解析PDF/DOCX/PPTX/XLSX/图片）、pandas库三种方式。提议规则：1)liteparse支持的格式应最高优先级使用liteparse 2)PDF文件需要定义大小阈值（小文件用Read，大文件用liteparse）3)Excel数据分析场景才使用pandas，纯读取用liteparse。需讨论：PDF阈值应该是多少(1MB/5MB/10MB)？规则应记录在哪(.claude/rules/file-reading-strategy.md)？如何判断文件大小？

## Previous Discussion

[Earlier: 3 discussion events]

[claude]: Round 1 ended
[claude]: Round 2 started

## Referenced Artifacts

- .omc/collaboration/artifacts/DISCUSS-CLAUDE文件读取工具优先级策略-当前存在READ工具-LITEPARSE技能-1780817504-discuss-r1-gemini-20260607-073206.md
- .omc/collaboration/artifacts/DISCUSS-CLAUDE文件读取工具优先级策略-当前存在READ工具-LITEPARSE技能-1780817504-discuss-r1-codex-20260607-073221.md

