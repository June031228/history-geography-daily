# -*- coding: utf-8 -*-
"""临时脚本：将第005课内容转为MDX并追加到腾讯文档"""
import os
import re
import subprocess
import json

REPO_DIR = r"C:\Users\June0\WorkBuddy\历史地理每日学习\history-geography-daily"
TDOCS_DIR = r"C:\Users\June0\.workbuddy\plugins\cache\workbuddy-builtin\tencent-docs-plugin\1.0.3\skills\tencent-docs"
PYTHON_EXE = r"C:\Users\June0\.workbuddy\binaries\python\versions\3.13.12\python.exe"

md_path = os.path.join(REPO_DIR, "lessons", "2026-09-04-第005课-二里头：最早的王朝都邑.md")
with open(md_path, "r", encoding="utf-8") as f:
    md = f.read()

# 去掉本地文件开头的 H1，避免与 frontmatter 标题重复；保留其余 Markdown 结构
lines = md.splitlines()
if lines and lines[0].startswith("# "):
    body_lines = lines[1:]
else:
    body_lines = lines
body = "\n".join(body_lines).strip()

# 将 **加粗** 转为 <Mark bold>...</Mark>
body = re.sub(r"\*\*(.+?)\*\*", r"<Mark bold>\1</Mark>", body)

# 把最后的 SCQA 情境段落从 Markdown 引用块转为 Callout
# 找到以 "> 情境：" 开头、到下一个空行或下一个标题前的段落
callout_pattern = re.compile(r"^> 情境：(.+?)(?=\n## |\n\n---|\Z)", re.MULTILINE | re.DOTALL)

def to_callout(m):
    inner = m.group(1)
    # 去掉每行开头的 "> "
    inner = re.sub(r"^> ?", "", inner, flags=re.MULTILINE).strip()
    return f'''<Callout icon="💡" blockColor="light_blue" borderColor="blue">
    情境：{inner}
</Callout>'''

body = callout_pattern.sub(to_callout, body)

mdx_content = f'''---
title: 第 005 课：二里头——最早的王朝都邑
icon: 🏛️
---

{body}
'''

args = json.dumps({
    "file_id": "WCXltHmkirOb",
    "action": "INSERT_AFTER",
    "content": mdx_content
}, ensure_ascii=False)

result = subprocess.run(
    [PYTHON_EXE, os.path.join(TDOCS_DIR, "tencentdocs.py"), "tdoc_call", "tencent-docs", "smartcanvas.edit", args],
    capture_output=True, text=True, encoding="utf-8"
)
print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)
print("EXIT CODE:", result.returncode)
