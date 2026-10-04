# TCG Live 对局记录

| 路径 | 内容 |
|---|---|
| `logs/` | 从 TCG Live 复制出来的原始对局记录（对局结束后 "Copy game log"），文件名 `<日期>_<序号>_vs-<对手卡组>.txt` |
| `timelines/` | `python -m ptcg.gamelog logs/*.txt --out timelines` 生成的逐回合时间线：先后攻、胜负、奖赏卡、对手亮出的牌和卡组推测、每次 Powerful Hand 时的手牌数 |
| `reviews/` | 人工复盘：每局的转折点、失误和打法建议，对照 `data/archetypes/<卡组>.yaml` |

```bash
python -m ptcg.gamelog data/gamelogs/logs/2026-10-05_3_vs-dragapult-ex.txt          # 打印时间线
python -m ptcg.gamelog data/gamelogs/logs/2026-10-05_3_vs-dragapult-ex.txt --json   # 完整解析结果
```

解析器的说明（日志格式、客户端文字里已知的错误）见 `ptcg/gamelog.py` 开头。新日志放进 `logs/` 后，`tests/test_gamelog.py` 里可以加对应的检查。
