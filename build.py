#!/usr/bin/env python3
"""Crypto Story Club KB generator: data/kb.json -> site/ (index + entry pages + kb.json).
Usage: python3 build.py   (run from this directory)"""
import json, html, os, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data", "kb.json")
SITE = os.path.join(HERE, "site")

CSS = """
*{box-sizing:border-box} body{margin:0;font-family:-apple-system,'PingFang SC','Microsoft YaHei',sans-serif;background:#0d1117;color:#e6edf3}
a{color:#58a6ff;text-decoration:none} a:hover{text-decoration:underline}
.wrap{max-width:860px;margin:0 auto;padding:24px 16px 64px}
header.top{border-bottom:1px solid #30363d;padding:28px 0 18px;margin-bottom:20px}
h1{font-size:26px;margin:0 0 6px} .sub{color:#8b949e;font-size:14px}
.badge{display:inline-block;border:1px solid #30363d;border-radius:999px;padding:1px 10px;font-size:12px;color:#8b949e;margin-right:6px}
.card{border:1px solid #30363d;border-radius:10px;padding:16px 18px;margin:12px 0;background:#161b22}
.card h2,.card h3{margin:0 0 6px;font-size:18px}
.card p{margin:4px 0;color:#c9d1d9;line-height:1.6;font-size:14.5px}
.type{font-size:12px;color:#d29922;letter-spacing:.08em}
input#q{width:100%;padding:10px 12px;border-radius:8px;border:1px solid #30363d;background:#0d1117;color:#e6edf3;font-size:15px;margin:8px 0 4px}
table.facts{border-collapse:collapse;width:100%;margin:10px 0}
table.facts td{border-top:1px solid #21262d;padding:7px 8px;vertical-align:top;font-size:14.5px;line-height:1.55}
table.facts td.k{color:#8b949e;white-space:nowrap;width:92px}
.rel a{margin-right:10px;font-size:14px}
.src{font-size:13px;color:#8b949e} footer{color:#6e7681;font-size:12.5px;margin-top:40px;border-top:1px solid #21262d;padding-top:14px}
"""

def esc(s): return html.escape(s, quote=True)

def entry_page(e, by_id):
    facts = "".join(f'<tr><td class="k">{esc(k)}</td><td>{esc(v)}</td></tr>' for k, v in e.get("facts", []))
    facts_html = f'<table class="facts">{facts}</table>' if facts else ""
    body = "".join(f"<p>{esc(p)}</p>" for p in e.get("body", []))
    rel = " ".join(f'<a href="{esc(r)}.html">{esc(by_id[r]["title"])}</a>' for r in e.get("related", []) if r in by_id)
    rel_html = f'<p class="rel">相关条目：{rel}</p>' if rel else ""
    src = "".join(f'<li><a href="{esc(u)}">{esc(t)}</a></li>' for t, u in e.get("sources", []))
    src_html = f'<p class="src">来源</p><ul class="src">{src}</ul>' if src else ""
    photo_html = f'<img src="{esc(e["photo"])}" alt="{esc(e["title"])}" style="width:220px;max-width:60%;border-radius:10px;margin:4px 0 10px">' if e.get("photo") else ""
    media = "".join(f'<li><a href="{esc(u)}">{esc(t)}</a></li>' for t, u in e.get("media", []))
    media_html = f'<p class="src">影音存档</p><ul class="src">{media}</ul>' if media else ""
    aliases = " / ".join(e.get("aliases", []))
    return f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(e['title'])} · Crypto Story Club 知识库</title>
<meta name="description" content="{esc(e['summary'])}">
<style>{CSS}</style></head><body><div class="wrap">
<p><a href="../index.html">← Crypto Story Club 知识库</a></p>
<span class="type">{esc(e['type'])}</span>
<h1 style="margin-top:6px">{esc(e['title'])}</h1>
<p class="sub">{esc(aliases)}</p>
<div class="card">{photo_html}<p>{esc(e['summary'])}</p>{facts_html}{body}</div>
{rel_html}{media_html}{src_html}
<footer>cryptostory.club · 数据文件 <a href="../kb.json">kb.json</a>（供 Agent 检索）</footer>
</div></body></html>"""

def main():
    data = json.load(open(DATA, encoding="utf-8"))
    entries = data["entries"]
    by_id = {e["id"]: e for e in entries}
    os.makedirs(os.path.join(SITE, "e"), exist_ok=True)
    for e in entries:
        with open(os.path.join(SITE, "e", e["id"] + ".html"), "w", encoding="utf-8") as f:
            f.write(entry_page(e, by_id))
    types = []
    for e in entries:
        if e["type"] not in types: types.append(e["type"])
    cards = ""
    for e in entries:
        thumb = f'<img src="{esc(e["photo"])}" alt="" style="width:64px;height:64px;object-fit:cover;border-radius:8px;float:right;margin:0 0 8px 12px">' if e.get("photo") else ""
        cards += f"""<div class="card" data-t="{esc(e['type'])}" data-s="{esc((e['title']+' '+' '.join(e.get('aliases',[]))+' '+e['summary']).lower())}">
{thumb}<span class="type">{esc(e['type'])}</span><h3><a href="e/{esc(e['id'])}.html">{esc(e['title'])}</a></h3><p>{esc(e['summary'])}</p></div>"""
    chips = "".join(f'<a class="badge" href="#" onclick="flt(this,\'{esc(t)}\');return false">{esc(t)}</a>' for t in types)
    index = f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Crypto Story Club · 币圈知识库</title>
<meta name="description" content="币圈的人、事、机构与思潮，用故事串起来的知识库。Crypto Story Club, cryptostory.club">
<style>{CSS}</style></head><body><div class="wrap">
<header class="top"><h1>Crypto Story Club · 币圈知识库</h1>
<p class="sub">币圈的人、事、机构与思潮，一条一条讲清楚，互相挂链。首批：FTX 专题（奈飞新剧《利他主义者》、FTX、Alameda、EA 与创始团队 7 人）。</p>
<p style="margin-top:10px"><a class="badge" href="#" onclick="flt(this,'');return false">全部</a>{chips}<a class="badge" href="kb.json">kb.json · 给 Agent 读</a></p>
<input id="q" placeholder="搜索条目，如 SBF、EA、Alameda…" oninput="srch(this.value)">
</header>
<div id="list">{cards}</div>
<footer>cryptostory.club · Crypto Story Club（CSC）· 更新于 {esc(data['updated'])} · 共 {len(entries)} 条</footer>
</div><script>
let cur='';
function flt(el,t){{cur=t;apply()}}
function srch(v){{window._q=v.toLowerCase();apply()}}
function apply(){{const q=window._q||'';document.querySelectorAll('#list .card').forEach(c=>{{
const okT=!cur||c.dataset.t===cur; const okQ=!q||c.dataset.s.includes(q);
c.style.display=(okT&&okQ)?'':'none'}})}}
</script></body></html>"""
    with open(os.path.join(SITE, "index.html"), "w", encoding="utf-8") as f:
        f.write(index)
    shutil.copy(DATA, os.path.join(SITE, "kb.json"))
    # media files (photos/video) live on img.yatslist.com/cryptostory/ — kb.json holds absolute URLs
    with open(os.path.join(SITE, "CNAME"), "w") as f:
        f.write("kb.cryptostory.club\n")
    with open(os.path.join(SITE, ".nojekyll"), "w") as f:
        f.write("")
    print(f"built {len(entries)} entries")

if __name__ == "__main__":
    main()
