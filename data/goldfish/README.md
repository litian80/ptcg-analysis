# 单人抽样模拟（goldfish）

没有对手，只看卡组自己能多快成型。每套 20000 局先攻、20000 局后攻，卡表取 Frankfurt（2026-09-26）该卡组名次最高的一份。"第 N 回合"指自己的第 N 个回合。打法是简单的贪心策略，比高手弱，数字偏保守。完整数字在同目录的 `<slug>.json`，命令 `python -m ptcg.goldfish <slug|all> [局数]`。

## 结论

- **Alakazam Dusknoir 最稳。** 第 3 回合能攻击：先攻 70%，后攻 87%。第 2 回合只有 22% / 39%。后攻第 3 回合平均手牌 15.6 张，47% 的局能单靠 Powerful Hand 一击 Dragapult ex（16 张）；先攻只有 9%。
- **Dragapult ex 第 3 回合 Phantom Dive：先攻 38%，后攻 57%。** 第 4 回合才到 64% / 75%。"第 3 回合开始 Phantom Dive"是顺利时的打法，不是常态。
- **Crustle 后攻第 1 回合 Ascension 进化 46%**（前提是规则允许），第 2 回合有 Crustle 77% / 93%。但起手有 47% 没摸到 Dwebble、要放 Kangaskhan；重抽 40%。
- **Basic Box（这份卡表）的 Latias ex 很难早打。** 这份卡表只有 2 张 Psychic Energy（主流是 3 张），Eon Blade 要两张都用上；有 19% 的局至少一张在奖赏卡里，拿奖前根本打不出。后攻第 1 回合 Latias 能攻击只有 0.4%，第 2 回合 18%。改成 Kangaskhan 当主攻：后攻第 2 回合 39%，第 3 回合 58%。
- **Slowking 卡在能量上。** 第 2 回合场上有 Slowking 62% / 76%，但贴够 2 个能量能攻击只有 16% / 29%。复制 Kyurem 后能量被弃，第 3 回合也只有 30% / 32%。

## 卡表微调（单人模拟能看到的部分）

| 卡组 | 改动 | 效果 |
|---|---|---|
| Alakazam Dusknoir | Dawn 4→3，多 1 Gwynn | 第 3 回合能攻击 −1~2 个百分点；手牌≥10 −2~3。保留 4 张 Dawn |
| Alakazam Dusknoir | 第 3 张 Dusknoir（−1 Special Red Card） | 第 3 回合能用 Cursed Blast +4.5 |
| Dragapult ex | Darkness 3→2（+1 Judge） | 第 3 回合 Munkidori 有 Darkness −5~6 |
| Dragapult ex | 加 Dunsparce + Dudunsparce | 成型速度几乎不变（±1）；它的价值不在开局 |
| Basic Box | Psychic 2→3（−1 Glass Trumpet） | Latias 第 3 回合能攻击 +9 / +12；拿奖前打不出 Eon Blade 的局 −17 |
| Basic Box | 第 2 张 Iron Leaves ex | 任一主攻手能攻击 +1 左右 |
| Crustle | Growing Grass 4→3 | 第 2 回合前贴 2 张 Growing Grass −4 / −8 |
| Crustle | Bianca's Devotion 换第 3 张 Poffin | 第 2 回合有 Crustle +3.5 / +1.5 |
| Crustle | 若后攻第 1 回合不允许 Ascension | 第 3 回合 2 只 Crustle −11 |
| Slowking | +1 Pawmot | 盲翻翻到复制来源 +2 |
| Slowking | +Lana's Aid、Academy 4→3 | 指定复制目标 −1 左右 |
| Alakazam Dudunsparce | 第 4 张 Rare Candy | 第 2 回合有 Alakazam +7 / +9 |

## 和手册说法对照

支持：
- alakazam-dusknoir.md:95-97 默认选后攻：第 2 回合能攻击 22% → 39%，第 3 回合手牌 12.3 → 15.6。
- alakazam-dusknoir.md:231 能量压在奖赏卡里的情况：5 个能量里≥2 个在奖赏卡只有 7.6%，平时不是问题。
- alakazam-dusknoir.md:621 Fez 起手在战斗场：被迫这样起手只有 4%，多半是自己选的。
- dragapult-ex.md:37 Dragapult ex 最早第 3 回合攻击：规则如此，第 3 回合场上有 Dragapult ex 57% / 73%。
- slowking-scr.yaml:23 Trifrost 后下一只要先备能量：第 3 回合能攻击只比第 2 回合多 4~14 个百分点（后攻 29% → 32%）。
- crustle-dri.md:435 Growing Grass 4 张不要减：减 1 张，第 2 回合前贴 2 张的局少 4~8 个百分点。
- slowking-scr.md:51 复制来源起手别放：被迫放上场的局有 7%。
- dragapult-ex.md:31 Darkness 张数：3→2 让 Munkidori 第 3 回合就绪少 5~6 个百分点。

反驳或要打折：
- basic-box-m.md:30 后攻第 1 回合 Latias 能凑出 Eon Blade：按这份卡表只有 0.4%（要 Latias、Ogerpon、Psychic、Crispin、Energy Switch 同时在手）。不能当选后攻的理由。
- basic-box-m.md:28 "Psychic Energy 只有 3 张"：手册说的是主流（世界赛到法兰克福 116 份卡表里 63 份带 3 张），这里模拟的 Frankfurt 37 名只带 2 张，19% 的局拿奖前打不出 Eon Blade。带 3 张时 Latias 第 3 回合能攻击多 9~12 个百分点，支持手册的张数。
- basic-box-m.yaml:8 "第 1 回合就能摆好攻击手"：第 2 回合任一主攻手能攻击只有 5% / 20%（Latias 打法），Kangaskhan 打法 12% / 39%。slowking-scr.md:198 说 Basic Box 第 2 回合就能打 120 以上，同样要打折。
- crustle-dri.md:419 第一只 Crustle 第 2 回合结束前要有 2 张 Growing Grass：只有 9% / 21%。
- crustle-dri.md:61 第 3 回合 Crustle 有 3 个能量：先攻 33%，后攻 52%。
- dragapult-ex.yaml:23 第 3 回合进化 Dragapult ex 并 Phantom Dive：38% / 57%。
- slowking-scr.yaml:19 第 2 回合进化并贴第 2 个能量：能攻击 16% / 29%。slowking-scr.md:53 说先攻"代价很小"：第 2 回合差 12 个百分点，第 3 回合才接近（30% 对 32%）。
- alakazam-dudunsparce.yaml:98 手牌 16 张一击 Dragapult ex：Dudunsparce 版第 3 回合只有 1% / 5% 能到 16 张。

管不了（要对手）：Budew 锁物品、Unfair Stamp / Special Red Card 之后手牌够不够（alakazam-dusknoir.md:357）、Codebreaking 叠的牌会不会被打乱（slowking-scr.md:52）、Kangaskhan 撤不下来（basic-box-m.yaml:145）、后备区满了放不下 Kangaskhan（slowking-scr.md:467，模拟的打法不放 Kangaskhan，所以量不出来）。

## 没有模拟的卡（当空白卡）

- Alakazam Dusknoir：Budew、Shaymin、Fezandipiti ex、Boss's Orders、Strange Timepiece、Special Red Card、Night Stretcher、Sacred Ash；Abra TWM 80 当普通 Abra。
- Dragapult ex：Budew、Fezandipiti ex、Boss's Orders、Crushing Hammer、Night Stretcher、Unfair Stamp、Special Red Card、Handheld Fan、Watchtower；Munkidori 只看有没有 Darkness。
- Basic Box：Lillie's Clefairy ex、Fezandipiti ex、Chien-Pao、Maractus、Boss's Orders、Codebreaking、Xerosic、Night Stretcher、Unfair Stamp；Iron Leaves / Raging Bolt / Wellspring 只看攻击费用。
- Crustle：Boss's Orders、Xerosic、Eri、Pokémon Center Lady、Bianca's Devotion、Jumbo Ice Cream、Hero's Cape、Handheld Fan、Prism Tower；Mist / Spiky 只当无色能量。
- Slowking：Mega Kangaskhan ex（含 Run Errand）、Fezandipiti ex、Mew ex、Lillie's Clefairy ex、Night Stretcher、Dangle Tail。
- Alakazam Dudunsparce：Genesect、Dedenne、Fezandipiti ex、Shaymin、Boss's Orders、Lana's Aid、Eri、Enhanced Hammer、Sacred Ash、道具、Battle Cage、Psychic / Enriching Energy。

注意：Crustle 后攻第 1 回合用 Ascension（招式效果进化）按允许算，规则问题见上表。每项数字的随机误差约 ±0.7 个百分点。
