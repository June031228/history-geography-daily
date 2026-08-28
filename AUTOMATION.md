# 每日发布流程规范（自动化执行手册）

> 自动化每日 16:00 触发，严格按本文件执行。本地仓库目录：
> `C:\Users\June0\WorkBuddy\历史地理每日学习\history-geography-daily`（GitHub：June031228/history-geography-daily，main 分支）

## 目标文档

- 腾讯文档（课程阅读端）：file_id `WCXltHmkirOb`，URL https://docs.qq.com/aio/DV0NYbHRIbWtpck9i
- 大纲：`outline/syllabus.md`（150 课，课号 001-150）
- 进度状态：`progress.json`

## 日期角色判定（按自然日历，自愈式）

课程正式开始日 `start_date = 2026-08-31`（周一）。设今日为 today：

1. **today < 2026-08-31**（开学前）：
   - 2026-08-28：生成《开学预告》——课程结构总览 + 第一周 5 课预告，文件名 `lessons/2026-08-28-preview.md`
   - 2026-08-29：生成《热身一：中华文明地理总框架》（三级阶梯、黄河长江两大文明轴）
   - 2026-08-30：生成《热身二：左图右史——怎么用"事件+地点+风俗"学历史》
2. **today ≥ 2026-08-31 且周一~周五**：
   - 应发课号 N = (today 距 start_date 的完整周数) × 5 + 本周第几个工作日
   - 例：2026-08-31 为第 1 周第 1 天 → 第 001 课
   - 从 `outline/syllabus.md` 取第 N 课的「事件 / 发生地 / 当地一俗」
3. **today 为周六**：生成本周地理专题（把本周 5 课的地点串成一条地理线：路线、地形、古今交通逻辑）
4. **today 为周日**：生成本周复盘（3 个回顾问题 + 一页小结）
5. **N > 150**：生成结课总结（朝代-地点对照回顾 + 后续第二季建议）

### 防重与补发

- 先检查 `lessons/` 目录：若今日对应文件已存在 → 本日跳过，仅在回报中说明
- 若历史日期有缺课（日历推算应有而文件不存在）→ 今日优先补发**最近一课**，并在文首注明补发
- 每次发布后更新 `progress.json` 的 `last_published_date` 与 `next_lesson`

## 事件课内容规范（三段式）

文件名：`lessons/YYYY-MM-DD-第NNN课-事件简称.md`

1. **今日事件**（约 400 字）：用"情境-冲突-悬念-答案"讲故事，不写成百科条目
2. **发生地今昔**（约 300 字）：古地名→今天哪座城；地理变迁（河道改迁、气候、交通）如何决定了这座城的兴衰
3. **当地一俗**（约 200 字）：一个当地独有的风俗/吃食/方言梗，讲清它的来历和今天的样子，作为记忆锚点
4. 文末附：`上节回顾` 一句话（第 001 课除外）+ `明日预告` 一句话

## 同步腾讯文档

发布完 GitHub 后，将当日课程正文转换为 MDX（遵循 mdx_references 规范：
标题用 Markdown `#`/`##`，高亮块用 Callout，禁止 Markdown 表格与 **加粗**，行内样式一律 `<Mark bold>`），
调用 `smartcanvas.edit`：`{"file_id":"WCXltHmkirOb","action":"INSERT_AFTER","content":"<MDX内容>"}`
（id 为空即追加到文档末尾）。工具调用方式：
`python tencentdocs.py tdoc_call tencent-docs smartcanvas.edit '<json>'`
（tencentdocs.py 位于 tencent-docs 技能目录；Python 用
`C:\Users\June0\.workbuddy\binaries\python\versions\3.13.12\python.exe`；长内容请先写入临时 .py 文件再用 subprocess 传参，避免命令行超长）

## GitHub 推送

- 在本地仓库目录用 git 提交并推送 main 分支（凭据已由 gh CLI 配置）
- commit message 格式：`lesson: YYYY-MM-DD 第NNN课（事件简称）` 或 `special: YYYY-MM-DD 地理专题` / `review: YYYY-MM-DD 周复盘`
- 若 git 推送失败，重试一次；仍失败则在回报中说明，内容保留在本地

## 执行完成后

在本会话中回报：今日发布内容标题、GitHub commit 链接、腾讯文档同步结果、当前总进度（第 N/150 课）。
