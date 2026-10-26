#!/usr/bin/env python3
# 把 docs/*.md 转成与 index.html 同风格的独立 HTML 页（供 GitHub Pages 直接阅读）
import io, os, re, sys, html
import markdown

BASE = os.path.dirname(os.path.abspath(__file__))

TPL = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · Aevora</title>
<style>
  :root {{ --fg:#1a1a1a; --dim:#6b6b6b; --line:#e3e3e3; --bg:#fbfbfa;
           --accent:#8a6d3b; --codebg:#f3f1ec; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; padding:40px 20px 90px; background:var(--bg); color:var(--fg);
          font:16px/1.78 -apple-system,"Segoe UI","Noto Sans SC","PingFang SC","Microsoft YaHei",sans-serif; }}
  main {{ max-width:760px; margin:0 auto; }}
  .top {{ font-size:13.5px; color:var(--dim); margin-bottom:26px; }}
  .top a {{ color:var(--accent); text-decoration:none; }}
  .top a:hover {{ text-decoration:underline; }}
  .top span {{ margin:0 8px; color:#c9c5bd; }}
  h1 {{ font-size:27px; margin:0 0 22px; letter-spacing:.4px; line-height:1.35; }}
  h2 {{ font-size:18px; margin:38px 0 12px; padding-bottom:7px; border-bottom:1px solid var(--line); }}
  h3 {{ font-size:15.5px; margin:26px 0 8px; color:#333; }}
  p {{ margin:12px 0; }}
  a {{ color:var(--accent); }}
  strong {{ font-weight:600; }}
  hr {{ border:none; border-top:1px solid var(--line); margin:34px 0; }}
  ul, ol {{ padding-left:22px; margin:12px 0; }}
  li {{ margin:5px 0; }}
  code {{ background:var(--codebg); padding:1px 5px; border-radius:3px;
          font:13.5px/1.5 "SFMono-Regular",Consolas,"Liberation Mono",monospace;
          color:#5a4a2f; word-break:break-word; }}
  pre {{ background:var(--codebg); padding:14px 16px; border-radius:4px; overflow-x:auto;
         border:1px solid #e8e5dd; }}
  pre code {{ background:none; padding:0; color:#2c2c2c; font-size:13px; }}
  blockquote {{ margin:16px 0; padding:2px 16px; border-left:3px solid var(--accent);
                color:var(--dim); background:#f7f5f0; }}
  table {{ border-collapse:collapse; width:100%; margin:18px 0; font-size:14px;
           background:#fff; display:block; overflow-x:auto; }}
  th, td {{ border:1px solid var(--line); padding:8px 11px; text-align:left; vertical-align:top; }}
  th {{ background:#f4f2ed; font-weight:600; white-space:nowrap; }}
  .toc {{ border:1px solid var(--line); background:#fff; padding:14px 20px 16px;
          margin:0 0 34px; border-radius:4px; }}
  .toc-h {{ font-size:12.5px; letter-spacing:1.2px; color:var(--dim); font-weight:600;
            margin:0 0 8px; text-transform:uppercase; }}
  .toc ul {{ list-style:none; padding:0; margin:0; }}
  .toc ul ul {{ display:none; }}
  .toc li {{ margin:6px 0; font-size:14.5px; }}
  .toc a {{ text-decoration:none; }}
  .toc a:hover {{ text-decoration:underline; }}
  footer {{ margin-top:56px; padding-top:16px; border-top:1px solid var(--line);
            color:var(--dim); font-size:13px; }}
  footer a {{ text-decoration:none; }}
</style>
</head>
<body>
<main>
<div class="top"><a href="../index.html">← Aevora</a><span>·</span><a href="architecture.html">架构图</a><span>·</span><a href="{md_name}">本文 Markdown 原文</a></div>

<h1>{title}</h1>

<div class="toc">
  <p class="toc-h">目录</p>
  {toc}
</div>

{body}

<footer>
  自用分享 · 不承诺维护 · AS IS · MIT<br>
  本页由 <code>{md_name}</code> 生成，内容以该文件为准。
</footer>
</main>
</body>
</html>
"""

JOBS = [
    ("01-骨架说明.md", "01-platform.html", "01 · 平台说明"),
    ("02-数据模型.md", "02-data-model.html", "02 · 数据模型"),
    ("PROVENANCE.md", "provenance.html", "来源说明（Provenance）"),
]

def convert(src, dst, title):
    raw = io.open(os.path.join(BASE, src), encoding="utf-8").read()
    # 去掉首个 h1（标题由模板渲染，同时让目录只收 h2 及以下）
    raw = re.sub(r"^#\s+.*?\n", "", raw, count=1)
    md = markdown.Markdown(extensions=["extra", "sane_lists", "toc"],
                           extension_configs={"toc": {"permalink": False, "toc_depth": "2-3"}})
    body = md.convert(raw)
    # markdown 的 toc 自带 <div class="toc"> 外壳，模板已有同名容器，去掉避免双层缩进
    toc = md.toc or ""
    toc = re.sub(r'^\s*<div class="toc">\s*', "", toc)
    toc = re.sub(r"\s*</div>\s*$", "", toc)
    if not toc.strip():
        toc = '<p style="margin:0;color:#6b6b6b">（本页无小节）</p>'
    out = TPL.format(title=html.escape(title), body=body, toc=toc, md_name=src)
    io.open(os.path.join(BASE, dst), "w", encoding="utf-8", newline="\n").write(out)
    print(f"  {src}  ->  {dst}  ({len(out.encode('utf-8'))} B)")

if __name__ == "__main__":
    for j in JOBS:
        convert(*j)
    print("done")
