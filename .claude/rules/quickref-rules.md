# 速查文档使用规则

## Load Trigger (懒加载条件)

Read this file when ANY of these occur:
- 执行命令失败 (command not found, permission denied, module not found)
- 数据库操作出错 (connection refused, authentication failed, migration errors)
- 服务启动失败 (port in use, environment variable missing)
- Django/Python执行错误 (import errors, settings errors)
- 用户询问环境配置、端口、路径、部署命令
- 需要验证执行规范或查找故障排查方案

---

## 速查文档体系

**核心文档**:
- `PROJECT-QUICKREF.md` - 综合速查手册（环境、端口、命令、故障排查）
- `docs/环境执行规范速查.md` - Python/Django/数据库正确执行方式
- `docs/数据速查.md` - 数据导入命令和统计

**使用方式**:
1. 遇到错误先查 `PROJECT-QUICKREF.md` 故障排查章节
2. 执行命令前查 `docs/环境执行规范速查.md` 确认正确方式
3. 数据导入问题查 `docs/数据速查.md`

---

## 速查原则

- 所有命令已验证可执行
- 包含正确/错误做法对比
- 提供故障排查快速索引
- 包含执行前检查清单

---

**Version:** v1.0  
**Created:** 2026-06-27
