# Crypto Story Club · 币圈知识库（CSC）

币圈的人、事、机构与思潮，一条一条讲清楚，互相挂链。站点：https://kb.cryptostory.club

## 结构
- `data/kb.json` — 唯一数据源（条目：作品 / 机构 / 思潮 / 人物 / 事件…），供网页与 Agent 共用
- `build.py` — 生成器：kb.json → `site/`（index + 每条一页 `e/<id>.html` + `kb.json`）
- `site/` — 静态成品，部署在 GitHub Pages（gh-pages 分支），自定义域名 kb.cryptostory.club

## 加新条目
1. 在 `data/kb.json` 的 entries 里加一条（id 用英文短码，related 填相关条目 id）
2. `python3 build.py`
3. 把 `site/` 推到 gh-pages 分支

## 首批内容（2026-11-22）
FTX 专题 11 条：《利他主义者》The Altruists（奈飞新剧）、FTX、Alameda Research、有效利他主义（EA）、创始团队 7 人（SBF、Gary Wang、Tara Mac Aulay、Caroline Ellison、Nishad Singh、Sam Trabucco、Ryan Salame）。
