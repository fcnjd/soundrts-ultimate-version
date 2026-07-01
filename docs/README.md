# SoundRTS 文档

源文件在 **`doc_src/src/{zh,en}/`**，只含 `.rst`。

```bash
python builddoc.py
# doc/zh/help-index.htm  ·  doc/en/help-index.htm
```

## 目录结构

```
doc_src/src/zh/
  help-index.rst      # 总入口
  relnotes.rst        # 版本说明（玩家与作者共用）
  player/             # 玩家：怎么玩
    index.rst         # 玩家文档索引
    manual.rst        # 游戏手册
    getting-started.rst
    …专题…
  mod/                # 模组作者：rules / 地图 / 战役
    index.rst         # 模组文档索引
    getting-started.rst   # Mod 入门（环境、rules、测试）
    advanced.rst          # Mod 进阶（技能、AI、元进度、导航）
    modding.rst           # 规则权威手册
    mapmaking.rst     # 地图语法权威手册
    map-guide.rst     # 地图入门与进阶
    campaign-guide.rst # 战役入门与进阶（含 campaign/ 专题）
    campaign/         # 战役专题附录
    skills-and-effects.rst
    aimaking.rst · randommap.rst · server.rst
    …元进度等专题…
```

| 读者 | 入口 | 路线 |
|------|------|------|
| 玩家 | `doc/zh/player/index.htm` | 入门 → 手册 → 专题 |
| 模组作者 | `doc/zh/mod/index.htm` | `getting-started` → `advanced` → 各专题手册 |
