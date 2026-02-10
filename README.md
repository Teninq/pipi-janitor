# Pipi Janitor 🐽

一个基于 Python IMAP 的 Gmail 自动化清理工具集，旨在实现收件箱的“Inbox Zero”管理。

## 🚀 项目功能
- **自动化分类**：根据预设关键词识别推广、社交、通知类邮件。
- **智能归档**：将非核心邮件自动移出收件箱（Archive），保持主界面清爽。
- **自定义标记**：支持特定关键词（如 `CDISC`）的自动标签化（Data Science）。
- **安全优先**：保留所有涉及账单、支付、安全警报及手动审核关键词的邮件。

## 📂 脚本说明
- `gmail_janitor_v2.py`: 核心清理逻辑，包含分步处理及防超时机制。
- `gmail_cleanup_final.py`: 包含自定义标签逻辑的生产环境版。
- `check_inbox_all.py`: 全量收件箱状态盘点工具。

## 🛠️ 环境要求
- Python 3.x
- 开启 IMAP 访问的 Gmail 账户
- Gmail App Password

## 📅 定时任务 (SOP)
该项目支持通过 OpenClaw Cron 挂载定时任务。
- **推荐执行时间**: 凌晨 03:00 (Asia/Shanghai)
- **任务目标**: 执行过夜大扫除，清除当日堆积的推广和社交通知。

---
*Created by Pipi for Boss.*
