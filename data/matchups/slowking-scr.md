# Slowking（呆呆王）对局手册

数据来源：2026 世界赛（8 月 28 日起）、Baltimore 区域赛（9 月 19 日）、Frankfurt 与 Brisbane 区域赛（9 月 26 日）的全部对局记录。Slowking 占环境约 6.1%，总战绩 1580 胜 1410 负 476 平，胜率 50.2%。本文所有胜率都把平局按 1/3 胜计算，环境平均约 47.6%。"关键卡与构筑"里的带卡/不带卡对比只来自公开了卡表的玩家（都是成绩较好的人），所以绝对数值偏高，只有两组的差值有参考意义；只有两组样本都不少于 15 局时才引用。没有先后攻数据，也没有逐局记录，凡是从卡牌文字推出、没有数据直接支持的打法都标了"（推断）"。

## 速查表

按环境份额排序（与对局次数大致一致）。

| 对手 | 胜率（局数） | 一句话要点 |
|---|---|---|
| Dragapult ex | 53.6%（637） | 趁对手还是 Dreepy/Drakloak 时用 Trifrost 一次收 3 只；Dragapult ex 在后备区时不吃招式伤害，别往它身上打 |
| N's Zoroark | 42.4%（317） | 对手任何招式都按恶属性双倍打 Slowking；先手抢在 Zorua 进化前 Trifrost，再处理后备区的 N's Zekrom |
| Dragapult Dusknoir | 54.0%（239） | 同 Dragapult，外加优先清掉 Duskull/Dusclops；后备区不要放 Fezandipiti ex、Meowth ex 让 Dusknoir 收 |
| Basic Box（Mega Kangaskhan） | 44.6%（254） | 战斗场的 ex（包括满血 Kangaskhan）Metallic Hammer 300 一击；后备区的 ex 用 Trifrost 110 + Thunder Raid 210；Tera Ogerpon 在后备区打不动 |
| Alakazam Dudunsparce | 28.4%（228） | 最差对局之一；Shaymin 废掉 Trifrost 的后备区伤害，靠 Metallic Hammer 逐只击倒 Alakazam，用 Thunder Raid 收 Fezandipiti ex |
| Mega Excadrill ex | 64.0%（173） | 两只 Mega 就是 6 张；提早用 Trifrost 断 Beldum/Drilbur/Metang，后备区 ex 用 Trifrost + Thunder Raid 收 |
| Dragapult Blaziken | 47.9%（208） | 后备区 Blaziken ex：Trifrost 110 + Thunder Raid 210 = 320 正好击倒 |
| Festival Lead | 49.0%（128） | Academy at Night 盖掉 Festival Grounds 就关掉连击；Rabsca/Shaymin 在场时 Trifrost 只打得到战斗场 |
| Dhelmise | 31.3%（114） | Dhelmise 140 HP：Trifrost 110 + Munkidori 30 = 140；Hide 'n' Sneak 挡指示物，但 Dhelmise 本身没有这个特性；对手有 Shaymin（58%）时 Trifrost 打不到后备区，先清 Shaymin |
| Ogerpon Meganium Hydrapple | 41.7%（92） | 早期 Trifrost 断 Chikorita/Bayleef/Applin 进化线；战斗场的 Hydrapple ex 用 Metallic Hammer 300 + Brave Bangle 30 一击 |
| Crustle | 68.0%（129） | Slowking 不是 ex，Crustle 挡不住；两次 Trifrost 收三只 Crustle，Metallic Hammer 300 一击任何 Crustle；对手的 Mega Kangaskhan ex 是 3 奖肥肉 |
| Alakazam Dusknoir | 29.4%（34） | 样本小；打法同 Alakazam，另外注意 Dusknoir 130 指示物 |

## 通用：Slowking 的复制工具箱

Slowking（SCR 58，120 HP，超属性，弱恶，撤退 3）的 Seek Inspiration（超 + 无色）弃掉牌库顶 1 张，如果是没有规则框的宝可梦，就用它的一个招式。被复制的招式不用付它自己的能量（推断，按"use it as this attack"的一般规则）。复制来的伤害按 Slowking 的超属性计算弱点（推断，同上）。牌库顶靠两张牌控制：Academy at Night（每回合一次，把手牌 1 张放到牌库顶）和 Ciphermaniac's Codebreaking（支援者，任选 2 张按顺序放牌库顶）。Poké Pad 把目标宝可梦拿到手上。Annihilape、Metagross、Pawmot、Drapion、Cofagrigus 在卡表里都没有进化前，只是复制来源。

| 复制来源（版本） | 招式 | 效果 | 卡表占比（4 场 103 份） |
|---|---|---|---|
| Kyurem（SFA 47） | Trifrost | 对手 3 只宝可梦各 110（后备区不算弱点抗性）；弃掉 Slowking 身上全部能量，Boomerang Energy 攻击后会贴回来 | 全部 2 张 |
| Zeraora（DRI 78） | Thunder Raid | 对手后备区 1 只宝可梦 ex 210；弃掉全部能量 | 约 53% |
| Metagross（CRI 61） | Metallic Hammer / Bounce Back | 300（选 +150 时，Slowking 没有钢能量就什么都不用弃，见下）/ 60 并把对手战斗场换下（对手选新战斗场） | 全部 2 张 |
| Annihilape（PBL 41） | Ghostly Blow | 100，再给对手后备区 1 只放 5 个伤害指示物 | 约 57% |
| Annihilape（SSP 100） | Tantrum / Destined Fight | 130 但 Slowking 混乱 / 双方战斗场宝可梦都被击倒 | 约 33%（21 份两种都带） |
| Pawmot（PFL 34） | Voltaic Fist | 130，可选自伤 60 让对手战斗场麻痹 | 约 17% |
| Drapion（POR 52） | Hazardous Tail | 100，自伤 70，对手麻痹 + 中毒 | 约 19% |
| Cofagrigus（SSP 83） | Law of the Underworld | 场上每只有特性的宝可梦（双方）各放 6 个指示物 | 约 16% |
| Smoochum（SSP 75） | Delightful Kiss | 从牌库找 2 个基本超能量贴给我方 1 只后备区宝可梦 | 约 17% |
| Unown（30C 72） | Mysterious Signal | 40，这一下击倒时多拿 1 张奖赏卡 | 约 12% |

几条每局都适用的规则：

- 复制来的 Metallic Hammer 是 300。官方裁定（[Chaos Rising FAQ](https://pokegym.net/2026/05/08/me-chaos-rising-faq/)，日本官方 Q&A 相同）：Slowking 身上没有钢能量也能选 +150，什么都不用弃；身上有钢能量时才要弃，最多 3 个。英文卡面读起来像必须先弃 3 个钢能量，是翻译造成的误会；Pokémon TCG Live 也按 300 结算。所以战斗场上 300 HP 以内的宝可梦都是一击：满血 Mega Kangaskhan ex（300）、N's Zoroark ex（280）、任何 Crustle（最高 290）；加 Brave Bangle 30 能一击 Hydrapple ex（330）；满血 Dragapult ex（320）剩 20，Fairy Zone 下是 600。录像里都是这样结算的：Baltimore 2026 第 1 天第 4 轮，Carullo 把满血 Dragapult ex 打到剩 20（[1:06:30](https://www.youtube.com/watch?v=Gq_tjemCPs8&t=3990s)）；B 桌 Smith 一下打倒满血 N's Zoroark ex（[1:25:20](https://www.youtube.com/watch?v=Gq_tjemCPs8&t=5120s)）；四强 Dreitzler 用 Brave Bangle 加 Hammer 一下打倒满血 Hydrapple ex（[6:14:06](https://www.youtube.com/watch?v=nLkFmtXdXGE&t=22446s)）。限制在张数：卡表只有 2 张 Metagross，用一次弃一张，要靠 Slowpoke 的 Dangle Tail 或 Night Stretcher 捡回（推断）。
- Tera 宝可梦 ex（Dragapult ex、Teal Mask Ogerpon ex、Wellspring Mask Ogerpon ex）在后备区时不受任何招式伤害，Trifrost 的后备区部分和 Thunder Raid 对它们无效；但伤害指示物的"放置"（Ghostly Blow、Cofagrigus、Munkidori）不是伤害，照样有效。
- Trifrost、Thunder Raid 之后 Slowking 只剩 Boomerang Energy。下回合手贴 1 个超能量就能再用 Seek Inspiration；Wondrous Patch 只能贴给后备区的超属性宝可梦，所以下一只 Slowking 要在后备区先补好能量。
- 攻击前的顺序：先用所有会洗牌或抽牌的东西（Lillie's Determination、Ultra Ball、Poké Pad、Surfer、Mega Kangaskhan ex 的 Run Errand），最后才用 Academy at Night 放目标，然后攻击。
- 对手打出别的场地卡会把 Academy at Night 弃掉，所以手里尽量常备一张。Codebreaking 放的第二张牌要过对手一个回合，会被 Judge、Unfair Stamp（洗牌）、Mega Excadrill ex 的 Undermine（弃牌库顶 2 张）破坏，不要把关键回合押在它上面。
- 能先攻就先攻（推断）。先攻第 1 回合不能攻击、不能打支援者，但 Slowking 本来就要到自己第 2 回合才能进化攻击，先攻的代价很小；收益是 Slowking 第一次攻击（整局第 3 回合）早于大多数进化卡组的主攻上场。对手后攻第 1 回合可以用 Budew 的 Itchy Pollen 锁你第 2 回合的物品，所以第 1 回合先用 Poké Pad 把 Kyurem 拿在手上，第 2 回合只靠 Academy at Night（场地卡不受锁）就能放到牌库顶。

---

## vs Dragapult ex（胜率 53.6%，637 局）

**对局性质**
- 双方都是进化卡组。对手核心卡表没有 Rare Candy，Dragapult ex 最早在对手第 3 回合进化；Slowking 从你第 2 回合就能攻击，中间有一到两个回合对手场上只有 Dreepy（70）、Drakloak（90）、Budew（30）、Munkidori（110），Trifrost 110 每只都能一下击倒。
- Dragapult ex 的 Phantom Dive 200 一击击倒任何 Slowking（120），同时在后备区放 6 个指示物；再加 Munkidori 挪 3 个，就是 90，能收掉 80 HP 的 Slowpoke（SCR 57）。对手理想节奏是每回合 2 张。
- 你的 Slowking 只给 1 张；你送出 2 奖以上的只有 Lillie's Clefairy ex（190）、Latias ex（210）、Fezandipiti ex（210）、Meowth ex（170）和 3 奖的 Mega Kangaskhan ex（300）。不放多余的 ex，对手就得击倒 6 次。
- 你的奖赏卡来源：前期 Trifrost 收进化前宝可梦（每只 1 张），中期击倒 1 只 Dragapult ex 或后备区的 Fezandipiti ex / Meowth ex（各 2 张）。

**开局与先后攻**
- 选先攻（推断）：你第 2 回合是整局第 3 回合，对手在第 2 回合放下的 Dreepy 还没法进化，Trifrost 能打到 3 只进化前宝可梦。
- 战斗场放 Slowpoke 或 Mega Kangaskhan ex。对手前期招式（Dreepy 的 Bite 40、Drakloak 的 Dragon Headbutt 70）打不穿 300 HP，Kangaskhan 在战斗场每回合 Run Errand 抽 2。Latias ex 在场时基础宝可梦撤退费为 0，Kangaskhan 可以随时退下来。
- 第 1 回合给战斗场的 Slowpoke 手贴 Telepathic Psychic Energy，从牌库拿 2 只基础超属性宝可梦（通常 2 只 Slowpoke）。
- Lillie's Clefairy ex 的 Fairy Zone 让对手所有龙属性宝可梦弱超能（×2）。它 190 HP，Phantom Dive 200 能一击。在你要打 Dragapult ex 的那个回合再放（Telepathic Psychic Energy 或 Ultra Ball 都能拿它，它是基础超属性），不要提前几回合摆在后备区当靶子（推断）。

**奖赏卡路线**
- 你第 1 回合：Slowpoke + 2 只 Slowpoke 上场，Poké Pad 拿 Kyurem 留在手上，打出 Academy at Night。
- 你第 2 回合（取 3）：进化 Slowking，贴第 2 个能量，用 Academy at Night 把 Kyurem 放到牌库顶，Seek Inspiration → Trifrost。目标优先级：Munkidori（110，正好击倒，它是对手收你后备区 Slowpoke 的关键）、Drakloak（90）、Dreepy（70）、Budew（30）。Fairy Zone 在场时战斗场的龙属性吃 220。
- 你第 3 回合（取 2）：对手若把 Fezandipiti ex 或 Meowth ex 放在后备区，Thunder Raid 210 直接击倒（Fezandipiti ex 210、Meowth ex 170）。若战斗场是新上来的 Dragapult ex（320）：Fairy Zone 在场时 Metallic Hammer 300 × 2 = 600，一击；没有 Clefairy 时 300 还差 20，需要 Munkidori 的 3 个指示物或之前 Ghostly Blow 放的 5 个指示物。Pawmot 的 Voltaic Fist 130 × 2 = 260 并可让它麻痹（推断：对手核心卡表里没有 Switch，麻痹的 Dragapult ex 下回合既打不了也撤不了），下回合补刀。
- 你第 4 回合（取最后 1 到 2 张）：Trifrost 或 Metallic Hammer 收残血。
- 没有 Fairy Zone 时，满血 Dragapult ex 吃 Metallic Hammer 剩 20，先用 Ghostly Blow 或 Munkidori 放好 20 以上就是一击；否则用 SSP 100 版 Annihilape 的 Destined Fight 双方战斗场同归于尽：你送 1 张，拿 2 张。
- 不要用 Trifrost 或 Thunder Raid 去打后备区的 Dragapult ex（Tera 规则：在后备区时不受招式伤害）。想提前削它只能放指示物：Ghostly Blow 的 5 个指示物可以放在后备区的 Dragapult ex 上。

**对手的套路，怎么防**
- Phantom Dive 的 60 指示物 + Munkidori 30 收后备区 Slowpoke：Trifrost 优先击倒 Munkidori（110）。
- Risky Ruins（核心 2 张）：你在自己回合把基础非恶属性宝可梦放到后备区时放 2 个指示物，Slowpoke 一上场就只剩 60，Phantom Dive 一下收掉。先打出 Academy at Night 换掉 Risky Ruins，再铺 Slowpoke（推断）。
- Crushing Hammer ×4：抛硬币弃你 1 个能量。后备区始终多备一只有能量的 Slowking（Wondrous Patch 从弃牌区补超能量）。
- Fezandipiti ex 的 Cruel Arrow（3 无色）对战斗场 Slowking 是恶属性 100 × 2 = 200，也能击倒；它在后备区时正是你 Thunder Raid 的目标。
- Judge（洗手牌再各抽 4）：会洗掉 Codebreaking 叠好的牌库顶。被 Judge 后用 Poké Pad 重新找 Kyurem 再用 Academy at Night。
- Boss's Orders 拉你的 2 奖或 3 奖宝可梦：不用的 ex 别放；Kangaskhan 在后备区挨 60 指示物不会倒，但在战斗场挨过一次 Phantom Dive 后剩 100，要靠 Latias ex 的 Skyliner 零撤退换下来。

**关键卡与构筑**
- 本对局你方带牌对比（n 均 ≥ 15）：带 Mew ex 的卡表胜率高 12.2 个百分点（41 对 214 局）；Pawmot 高 9.4 个百分点（40 对 215）；带 Budew 低 8.9（55 对 200）；Brave Bangle 低 7.3（50 对 205）；Drapion 低 6.3（46 对 209）；Lucky Helmet 低 4.2（126 对 129）。
- Pawmot 的正面效果与卡牌文字吻合：Fairy Zone 下 260 加麻痹，两回合内击倒 Dragapult ex（推断）。Mew ex（160 HP，撤退 0）的 Memory Helix 能使用后备区 Slowking 的 Seek Inspiration，相当于多一个零撤退的攻击位（推断）。
- 对手方：带 Judge 的 Dragapult ex 卡表对你胜率高 8.9 个百分点（194 对 43 局），说明打乱手牌和牌库顶确实有效；带 Team Rocket's Watchtower 高 4.1（57 对 180），它会关掉你 Mega Kangaskhan ex 和 Meowth ex 的特性。
- 建议：此对局 Pawmot 或 Mew ex 值得占一个位置（数据支持）；没有 Clefairy 时，Munkidori + Darkness Energy 能补 Metallic Hammer 300 打 Dragapult ex 差的 20（推断，本对局无足量数据）。

**常见失误**
- Trifrost 的三个目标里选了后备区的 Dragapult ex，伤害全部被 Tera 规则挡掉。
- 在 Risky Ruins 还在场时铺 Slowpoke，被 Phantom Dive 的 60 指示物一回合收掉两只。
- 提前好几回合把 Lillie's Clefairy ex 放在后备区，被 Boss's Orders + Phantom Dive 白拿 2 张。
- 用 Academy at Night 放好 Kyurem 后才用 Run Errand 或 Poké Pad，把 Kyurem 抽走或洗掉。
- 对手连着几回合只放指示物不击倒时，以为安全，后备区同时留着 Latias ex 和 Mega Kangaskhan ex。录像：Baltimore 2026 第 1 天第 4 轮第 1 局，Hedrick 不击倒是为了不让 Fezandipiti ex 抽牌，最后一发 Phantom Dive 击倒战斗场 Slowking 加后备区这两只，一回合拿 6 张（[0:51:00](https://www.youtube.com/watch?v=Gq_tjemCPs8&t=3060s)）。被铺过指示物的 ex 要算进对手下回合的奖赏卡里。
- 用 Drapion 麻痹对手后，后备区留着能量不够、撤退 3 的 Slowking：对手用 Boss's Orders 把它拉到战斗场，麻痹换来的一回合就抵消了（同一局）。

---

## vs N's Zoroark（胜率 42.4%，317 局）

**对局性质**
- 对手更快，而且属性克你。N's Zoroark ex（280 HP，恶属性）的 Night Joker（恶 × 2）复制后备区 N's 宝可梦的招式，伤害按恶属性算，Slowking 弱恶。复制 N's Zekrom 的 Shred 70 × 2 = 140 就击倒 Slowking，还没有"下回合不能攻击"的限制；N's Zorua 的 Scratch 20 × 2 = 40。
- 对手对你基本是每回合 1 张。对手想加速就 Boss's Orders 拉你的 ex：Mega Kangaskhan ex 300 HP 会被 Rampaging Thunder 250 + Binding Mochi 40 + Black Belt's Training 40 = 330 击倒（3 张）。
- 你要拿 6 张：N's Zoroark ex 2 张，Pecharunt ex（190）、Fezandipiti ex（210）、Meowth ex（170，27% 卡表）各 2 张，N's Zorua（70）、Tatsugiri（70）、Munkidori（110）、N's Zekrom / N's Reshiram（130）各 1 张。
- 战斗场的满血 N's Zoroark ex（280）吃不住 Metallic Hammer 300，一击拿 2 张。录像：Baltimore 2026 第 1 天第 4 轮 B 桌，Smith 复制 Metallic Hammer 一下打倒满血 Zoroark ex（[1:25:20](https://www.youtube.com/watch?v=Gq_tjemCPs8&t=5120s)）。Metagross 用完时改用 Destined Fight 一换一（你送 1 张，拿 2 张）。
- 对手有两种构筑（四场比赛 112 份卡表）：Watchtower 版带 3 到 4 张 Team Rocket's Watchtower（51 份），其中 33 份带 N's Purrloin，几乎不带 N's Castle 和 N's Darmanitan；Castle 版带 N's Castle（57 份），Watchtower 多是 0 到 1 张，31 份带 N's Darmanitan。前者专门锁你的手牌和特性，开局看到 Watchtower 或 Purrloin 就按下面"手牌锁"那条防。

**开局与先后攻**
- 强烈建议先攻（推断）：N's Zoroark ex 是 1 阶，对手第 2 回合就能进化。你先攻时，你第 2 回合（整局第 3 回合）对手的 Zorua 还没进化；你后攻时，对手第 2 回合（整局第 3 回合）Zoroark ex 已经上场并能先打你。
- 战斗场不要放 Mega Kangaskhan ex。它会成为 330 组合的目标；而且 Team Rocket's Watchtower（78% 卡表，3 张）在场时无色宝可梦没有特性，Run Errand 和 Meowth ex 的 Last-Ditch Catch 都会失效。放 Slowpoke。

**奖赏卡路线**
- 你第 2 回合（取 2 到 3）：Trifrost 打 3 只 70 到 110 HP 的基础宝可梦：N's Zorua、Tatsugiri、Munkidori 都一下击倒；N's Zekrom / N's Reshiram（130）会剩 20。
- 你第 3 回合（取 2）：后备区有 Pecharunt ex 或 Fezandipiti ex 就 Thunder Raid 210 击倒；若有 N's Zoroark ex 已经吃过 Trifrost 110，Thunder Raid 210 补到 320 也击倒（280 HP）。
- 你第 4 到 5 回合（取剩下的）：战斗场的满血 Zoroark ex 用 Metallic Hammer 300 一击；Metagross 用完了就用 Destined Fight 同归于尽。
- 处理复制来源（推断）：对手 Night Joker 的伤害全靠后备区的 N's Zekrom（Shred 70、Rampaging Thunder 250）和 N's Reshiram（Virtuous Flame 170）。它们各 130 HP，Trifrost 110 后再补一次就倒（或 Trifrost + Ghostly Blow 的 5 个指示物 = 160）。把后备区的 Zekrom / Reshiram 清掉，对手只剩 Zorua 的 Scratch 可复制（对 Slowking 40），要等 Night Stretcher 捡回来。

**对手的套路，怎么防**
- 每回合 Shred 140 一换一，耗你的 Slowking：后备区一直保持 1 到 2 只有能量的 Slowking/Slowpoke，Slowpoke 的 Dangle Tail 和 Night Stretcher 把被弃的 Kyurem、Slowking 捡回来。
- Pecharunt ex 的 Irritated Outburst 按你已拿的奖赏卡数每张 60，打 Slowking 还要 × 2：你拿得越多它越痛。它在后备区时（190 HP）是 Thunder Raid 的一击目标。
- Team Rocket's Watchtower、N's Castle 会把你的 Academy at Night 盖掉：手里常备 Academy at Night，在自己回合重新打出再用。
- Xerosic's Machinations（让你弃到 3 张手牌）和 Judge 打乱手牌：Kyurem 不要只靠手上那一张，Codebreaking 可以直接从牌库叠到顶。
- 手牌锁（Watchtower 版）：N's Purrloin（JTG 96，70 HP，31% 卡表）的 Thieving Swipe 被 Night Joker 复制后，对手看你的手牌，挑 1 张放到你牌库底；再加 Watchtower 盖掉 Academy at Night、关掉 Run Errand，加 Judge 洗掉叠好的牌库顶。要用的复制目标别只放手上等 Academy，能用 Codebreaking 就直接从牌库叠；后备区的 Purrloin 用 Trifrost 顺手收掉（推断）。录像：Baltimore 2026 第 1 天第 4 轮 B 桌第 2 局，Osterkatz 重新打出 Watchtower，再用 Thieving Swipe 和 Judge，Smith 之后再没打出攻击，只盲翻过一次 Seek Inspiration（[1:25:30](https://www.youtube.com/watch?v=Gq_tjemCPs8&t=5130s)），Kyurem 被放到了牌库底。
- Boss's Orders 拉 Kangaskhan、Latias ex（210，恶弱点，Shred 就 140，Rampaging Thunder 必倒）：这两只在此对局尽量不上场。录像：同一局 Osterkatz 没打战斗场带 Lucky Helmet 的 Kangaskhan（打了你就抽 2 张），而是用 Boss's Orders 拉后备区的 Fezandipiti ex 拿 2 张，顺便去掉你一个抽牌来源（[1:23:00](https://www.youtube.com/watch?v=Gq_tjemCPs8&t=4980s)）；最后也是 Boss's Orders 拉 Latias ex 收尾。

**关键卡与构筑**
- 你方（n 均 ≥ 15）：带 Mew ex 高 16.0 个百分点（19 对 98 局）；Unown 高 11.1（17 对 100）；Pawmot 高 10.7（16 对 101）；Cofagrigus 低 11.5（22 对 95）；Brave Bangle 低 10.4（30 对 87）；Munkidori 低 7.4（30 对 87）；Crispin 低 5.0（25 对 92）；Zeraora 低 4.9（59 对 58，样本最大，差距小）。
- 对手方：带 Tatsugiri 的卡表对你高 17.2 个百分点（99 对 32）；带 Team Rocket's Watchtower 高 10.9（101 对 30）；Air Balloon 高 10.4（72 对 59）；Xerosic's Machinations 高 7.9（30 对 101）；Judge 高 7.1（104 对 27）；带 Meowth ex 的反而低 11.5（33 对 98），可能因为它是你 Thunder Raid 的 2 奖目标（推断）。
- Cofagrigus 负面的可能原因：Law of the Underworld 也会在你自己的 Mega Kangaskhan ex、Latias ex、Meowth ex、Fezandipiti ex 身上各放 6 个指示物（推断）。
- 建议：Mew ex、Unown、Pawmot 三张小样本都为正，可选其一；Unown 的 Mysterious Signal 40 收残血 ex 时多拿 1 张（推断）。

**常见失误**
- 后攻却按常规节奏铺场，Zoroark ex 已经上场时 Trifrost 只能打到 Zorua 以外的东西。
- 只盯着打 Zoroark ex，放着后备区的 N's Zekrom 不管，对手每回合都能复制 Shred 或 Rampaging Thunder。
- 把 Mega Kangaskhan ex 放在战斗场抽牌，被 330 一击送 3 张；或 Watchtower 在场还指望 Run Errand。
- 打出 Thunder Raid 去打满血 Zoroark ex（210 打不倒 280）。

---

## vs Dragapult Dusknoir（胜率 54.0%，239 局）

**对局性质**
- 和 Dragapult ex 同一骨架，多了 Duskull（60）→ Dusclops（90）→ Dusknoir（160）。Dusclops 的 Cursed Blast 放 5 个指示物，Dusknoir 放 13 个，放完自己被击倒（送你 1 张）。13 个指示物能直接击倒你任何位置的 Slowking（120）或 Slowpoke。
- 对手常见组合：Phantom Dive 200 打战斗场 + 60 指示物 + Dusknoir 130 = 一回合击倒 190 HP 以内的后备区 ex（Lillie's Clefairy ex、Meowth ex）或两只单奖。
- 每次 Cursed Blast 都送你 1 张，所以对手的有效奖赏差没有看上去那么大；你的优势是 Trifrost 对这副牌几乎每只基础和 1 阶宝可梦都是一击（推断）。

**开局与先后攻**
- 先攻（推断），理由同 Dragapult ex。对手 26% 卡表带 2 张 Rare Candy，可以在第 2 回合让 Duskull 直接变 Dusknoir，所以第 1 回合对手后备区的 Duskull 就是你第 2 回合 Trifrost 的首选目标之一。
- 战斗场 Slowpoke 或 Mega Kangaskhan ex 都可以；但后备区不要摆 Meowth ex、Fezandipiti ex、Lillie's Clefairy ex 过夜，60 + 130 = 190 正好够它们（Fezandipiti ex 210 需要再多 20，Munkidori 能补）。

**奖赏卡路线**
- 你第 2 回合（取 3）：Trifrost 击倒 Duskull（60）、Dusclops（90）、Dreepy（70）、Drakloak（90）、Munkidori（110）、Patrat（70）中的 3 只。先打已经进化的 Dusclops（下回合就能自爆）和 Munkidori。
- 你第 3 回合（取 2）：Thunder Raid 击倒后备区的 Fezandipiti ex（210）或 Meowth ex（170）；Dusknoir（160）在后备区时用 Trifrost 110 + Ghostly Blow 5 指示物 = 160 正好击倒（两回合）。
- 你第 4 回合（取最后 1 到 2 张）：Dragapult ex 在战斗场时按 Dragapult ex 章节：Fairy Zone 下 Metallic Hammer 600 一击；没有 Clefairy 时 300 + 指示物 20 以上，或 Destined Fight。对手自爆送的奖赏卡常常让你提前一回合拿完。

**对手的套路，怎么防**
- Dusknoir 13 个指示物狙后备区：不让 2 奖 ex 在后备区停留；Slowking 被狙也只送 1 张，换掉的是对手一张 Dusknoir（也送你 1 张）。
- Jamming Tower（76% 卡表）：所有道具无效（你的 Lucky Helmet、Brave Bangle），而且把 Academy at Night 盖掉。重新打出 Academy at Night 同时恢复道具。
- Patrat（45% 卡表，Watchful Eye）：双方都不能挪动指示物，你的 Munkidori 失效。Patrat 70 HP，Trifrost 顺手击倒。
- Duskull 的 Come and Get You 从弃牌区拉回最多 3 只 Duskull：Trifrost 收掉的 Duskull 会回来，后期仍要留一次 Trifrost 清场（推断）。
- Moltres（PFL 14）的 Fighting Wings 对战斗场宝可梦 ex 打 110，对 Slowking 只有 20：它是用来打你战斗场的 Kangaskhan、Latias ex 的。

**录像：Frankfurt 区域赛八强 Malaca（Slowking）0-2 Conti（Dragapult Dusknoir）**
- **Budew 锁物品就是锁能量**：第 1 局 Conti 先攻，Budew 连续 5 回合 Itchy Pollen（[5:05](https://www.youtube.com/watch?v=NOi0qAFjnME&t=18300s)）。Wondrous Patch 是物品，用不了，Slowking 线一直接不上能量。对手有 Budew 时，每回合的手贴能量优先给下一只 Slowking（推断）。
- **Trifrost 收 3 只**：第 2 局 Trifrost 一次击倒两只 Drakloak 和一只 Dusclops，拿 3 张（[5:23:44](https://www.youtube.com/watch?v=NOi0qAFjnME&t=19424s)），和上面的路线一致。但 Trifrost 弃光了能量，下一回合接不上攻击，对手趁机用 Crispin、Dusknoir、Jamming Tower 重建。打 Trifrost 之前，后备区要有一只已经有能量的 Slowking。
- **对手先铺指示物不收**：Conti 用 Boss's Orders 拉出 Latias ex，Phantom Dive 的指示物分散放（[5:28](https://www.youtube.com/watch?v=NOi0qAFjnME&t=19680s)）。你的核心构筑里没有回复卡，这些指示物会一直留着，是在准备一回合多收。
- **Kangaskhan 别在对手有 Dusknoir 时站战斗场**：Malaca 为了用 Run Errand（只在战斗场能用）把 Mega Kangaskhan ex 放到战斗场，Conti 用 Cursed Blast 130 加 Phantom Dive 200（合计 330，超过 300）击倒它，指示物收掉铺过伤害的 Latias ex 和 Slowking，一回合拿 6 张（[5:30](https://www.youtube.com/watch?v=NOi0qAFjnME&t=19800s)）。

**关键卡与构筑**
- 你方（n 均 ≥ 15）：带 Zeraora 高 16.3 个百分点（52 对 27 局），与对手 Fezandipiti ex（全部卡表）、Meowth ex（95%）都是 Thunder Raid 的一击目标吻合；Lucky Helmet 高 13.6（38 对 41）；Annihilape 高 10.7（61 对 18）；Surfer 高 6.8（38 对 41）。
- 对手方：带 Rare Candy 的卡表对你低 12.4（25 对 48）；Moltres 高 7.6（37 对 36）；Dawn 低 6.8（50 对 23）；Judge 高 6.3（48 对 25）；Patrat 高 5.3（24 对 49）；Jamming Tower 低 4.0（51 对 22）。
- 建议：此对局 Zeraora 必带（数据支持）。

**常见失误**
- 把 Trifrost 打在 Dragapult ex 上而不是 Dusclops，下回合被 Cursed Blast 补刀。
- 后备区留着 Meowth ex，被 Phantom Dive 60 + Dusknoir 130 一回合收 2 张。
- 以为对手自爆是好事而放任 Dusclops 留在后备区：它自爆收掉的是你的 Slowpoke 或残血 Slowking，奖赏数打平，但你的攻击线断了（推断）。
- 对手场上有 Dusknoir 时让 Mega Kangaskhan ex 站战斗场用 Run Errand，被 Phantom Dive 加 Cursed Blast 一次收 3 张（录像）。

---

## vs Basic Box（Mega Kangaskhan，胜率 44.6%，254 局）

**对局性质**
- 对手全是基础宝可梦，第 2 回合就能打出 120 以上伤害：Mega Kangaskhan ex 200 起、Latias ex 200、Iron Leaves ex 180、Raging Bolt ex 每弃 1 个能量 70、Teal Mask Ogerpon ex 30 + 双方战斗场每个能量 30、Fezandipiti ex 的 Cruel Arrow 对战斗场 Slowking 200（恶属性 × 2）。每回合都能击倒你一只 Slowking。
- 对手几乎全是 2 奖，Kangaskhan 3 奖。理论上你只需击倒 3 只 2 奖（或 Kangaskhan + 1 只 2 奖 + 1 只单奖），对手需要 6 次。对手 HP 在 170 到 300 之间，战斗场上的任何一只都吃不住 Metallic Hammer 300（挂 Hero's Cape 的 +100 除外）；后备区的要两步。胜率仍低于奖赏卡算账，原因没有从卡牌文字推出：Metagross 只有 2 张，每次攻击都要先把复制目标放到牌库顶，而对手的 Unfair Stamp、Chien-Pao 专门打断这一步（推断）。
- 后备区的 Teal Mask Ogerpon ex 和 Wellspring Mask Ogerpon ex 是 Tera，后备区时不吃 Trifrost 和 Thunder Raid。可以稳定两步收的是非 Tera ex：Meowth ex（170，3 张）、Lillie's Clefairy ex（190）、Latias ex、Fezandipiti ex（210）、Iron Leaves ex、Iron Crown ex（220）、Raging Bolt ex（240）、Mega Kangaskhan ex（300）。

**开局与先后攻**
- 先攻（推断）。对手先攻也不能在第 1 回合攻击；你后攻时对手第 2 回合就能打你的 Slowpoke。
- 不要让 Mega Kangaskhan ex 站在战斗场：对手 Raging Bolt ex 弃 5 个能量 350、Kangaskhan 抛 2 次正面 300，都能一击送你 3 张。
- 第 1 回合 Slowpoke 战斗场 + Telepathic Psychic Energy 拿 2 只 Slowpoke；Lillie's Clefairy ex 在此对局只对 Raging Bolt ex 有用（它是龙属性），按需放。

**奖赏卡路线**
- 你第 2 回合（取 2 到 3）：Metallic Hammer 300 击倒战斗场的 ex，战斗场是 Mega Kangaskhan ex 就拿 3 张。战斗场是单奖宝可梦（如 Chien-Pao）或 Metagross 放不到牌库顶时，改用 Trifrost 打战斗场 + 2 只非 Tera 后备区 ex，优先后备区的 Mega Kangaskhan ex 和 Meowth ex（推断）。
- 你第 3 回合（取 2 到 3）：战斗场的 ex 接着用 Metallic Hammer。打过 Trifrost 的话，Thunder Raid 收后备区吃过 110 的 ex（110 + 210 = 320，所有非 Tera ex 都够，Mega Kangaskhan ex 拿 3 张）；满血的 Meowth ex（170）、Lillie's Clefairy ex（190）、Latias ex、Fezandipiti ex（210）Thunder Raid 一下就倒。
- 你第 4 回合（取 2）：两张 Metagross 用完后用 Dangle Tail 或 Night Stretcher 捡回再用（推断）。Fairy Zone 下 Raging Bolt ex（240）满血也能被 Super Psy Bolt（需要 3 个能量）240 一击。
- 你第 5 回合（取最后 1 到 2 张）：Thunder Raid 收另一只后备区 ex。
- 战斗场的满血 Mega Kangaskhan ex：Metallic Hammer 300 正好击倒，拿 3 张；挂 Hero's Cape（400）时用 Destined Fight 一换一，你送 1 张拿 3 张（SSP 100 版 Annihilape）。

**对手的套路，怎么防**
- Area Zero Underdepths（全部卡表 3 张）：有 Tera 在场时后备区 8 格。用 Academy at Night 盖掉它时，双方后备区都要弃到 5 只，打出者（对手）先弃（推断，按卡牌文字"the player who played this card discards first"）。在对手铺满 8 格后再换场地，收益最大。
- Chien-Pao（SSP 56，97% 卡表）放到后备区时可以弃掉场上的场地，专门拆 Academy at Night：多备一张。
- Wellspring Mask Ogerpon ex 的 Torrential Pump 打战斗场 100，再对后备区 120：能同时收后备区的 Slowking（120）或 Slowpoke。后备区备用的 Slowking 只放一只。
- Unfair Stamp（你上回合击倒了它的宝可梦才可用）：你洗手牌只抽 2。Kyurem 和 Academy at Night 别都押在手上；击倒对手后的那个回合预期会被 Stamp。
- Boss's Orders、Prime Catcher 拉你的 2 奖 ex：后备区只放用得上的 ex。

**关键卡与构筑**
- 你方（n 均 ≥ 15）：带 Smoochum 高 23.8 个百分点（18 对 89）；Cofagrigus 高 17.5（17 对 90）；Prime Catcher 高 8.3（32 对 75）；Drapion 高 7.0（24 对 83）；Munkidori 高 6.4（30 对 77）；Crispin 高 5.9（27 对 80）；Annihilape 低 22.9（67 对 40）；Brave Bangle 低 19.4（19 对 88）。
- Cofagrigus 的正面与卡牌文字吻合：对手几乎每只都有特性（Kangaskhan、Meowth ex、Teal Mask Ogerpon ex、Latias ex、Clefairy ex、Fezandipiti ex、Iron Leaves ex、Iron Crown ex、Chien-Pao），Law of the Underworld 各放 60，后备区的 Tera Ogerpon 也吃（放置不是伤害）。代价是你自己的 Kangaskhan、Latias ex、Meowth ex、Fezandipiti ex、Clefairy ex、Munkidori 也各吃 60（推断：所以只在你场上有特性的宝可梦少时用）。
- Smoochum 正面的原因没有从卡牌文字直接推出；可能是 Delightful Kiss 给后备区一次贴 2 个超能量，让 Latias ex 的 Eon Blade 200 提前可用（推断）。
- Annihilape 负面与 Destined Fight 的账面价值相矛盾，数据里两种版本混在一起，原因未明。
- 对手方：带 Glass Trumpet 的卡表对你低 24.0 个百分点（80 对 26）；带 Raging Bolt ex 低 20.5（79 对 27）；带 Unfair Stamp 高 16.5（59 对 47）。
- 建议：此对局 Cofagrigus、Prime Catcher 值得考虑（数据支持）；Prime Catcher 能把后备区的 Tera Ogerpon 或 Mega Kangaskhan ex 拉到战斗场，让 Metallic Hammer 一击（推断）。

**常见失误**
- Trifrost 打后备区的 Teal Mask Ogerpon ex，伤害无效。
- Thunder Raid 打满血的 Kangaskhan（300）、Raging Bolt ex（240）、Iron Leaves ex（220），一下打不倒白白弃光能量。
- 让自己的 Mega Kangaskhan ex 留在战斗场抽牌，被一击送 3 张。
- 在对手铺满 8 格前就用 Academy at Night 换掉 Area Zero Underdepths，失去让对手弃后备区的机会（推断）。

---

## vs Alakazam Dudunsparce（胜率 28.4%，228 局）

**对局性质**
- 双方都以单奖宝可梦为主。对手 Alakazam（MEG 56，140 HP）的 Powerful Hand 只要 1 个超能量，按手牌数每张放 2 个指示物：手牌 6 张就击倒 Slowking，11 张击倒 Latias ex，15 张击倒 Mega Kangaskhan ex。Kadabra、Alakazam 进化时抽牌，Dudunsparce 抽 3 后洗回牌库，手牌很容易维持在 6 张以上。
- 你的 Metallic Hammer 一击击倒 Alakazam（140）和 Dudunsparce（140），所以正面是一换一。差距来自对手的防守工具（推断）：Shaymin（DRI 10）让后备区无规则宝可梦不受招式伤害，Trifrost 只剩战斗场一份；Battle Cage 挡住你的招式放在后备区的指示物（Ghostly Blow、Cofagrigus）；Genesect（SFA 40）带道具时你不能打 ACE SPEC（Secret Box、Prime Catcher）；Enhanced Hammer 弃掉你的 Telepathic Psychic Energy 和 Boomerang Energy（都是特殊能量）。
- 对手唯一常见的 2 奖目标是 Fezandipiti ex（210），36% 卡表还有 Lillie's Clefairy ex（190）。两只都能被 Thunder Raid 一击。

**开局与先后攻**
- 先攻（推断）：对手要靠 Rare Candy 跳阶，而 Rare Candy 不能在自己第 1 回合用，Alakazam 最早在对手第 2 回合上场。你先攻，第 2 回合（整局第 3 回合）的 Trifrost 先于 Alakazam 出场，能打 Abra（50）、Dunsparce（60 或 70）。
- 不放 Mega Kangaskhan ex、Latias ex、Meowth ex 到场上，除非马上要用：它们只是给 Powerful Hand 的 2 到 3 奖目标。战斗场 Slowpoke。

**奖赏卡路线**
- 你第 2 回合（取 1 到 3）：对手后备区没有 Shaymin 时，Trifrost 击倒 3 只 Abra / Dunsparce / Kadabra（80）；有 Shaymin 时只有战斗场会受伤，改用 Metallic Hammer 打战斗场。
- 之后每回合（各取 1）：Metallic Hammer 击倒战斗场的 Alakazam 或 Dudunsparce。
- 对手放下 Fezandipiti ex（它要在自己宝可梦被击倒后才能抽 3，所以你击倒东西后它很可能出现）：下个回合 Thunder Raid 210 击倒，取 2。Lillie's Clefairy ex 同理。
- 一条现实的路线：Trifrost 或 Hammer 2 张 + Fezandipiti ex 2 张 + Hammer 2 张，共 5 到 6 个攻击回合；对手同样要击倒你 6 次，比拼的是谁的攻击手先断（推断）。
- Shaymin 的处理（推断）：它 80 HP、有特性，Cofagrigus 的 Law of the Underworld 能放 60；Battle Cage 在场时后备区的指示物会被挡，先用 Academy at Night 把 Battle Cage 换掉。

**对手的套路，怎么防**
- Powerful Hand 放的是指示物不是伤害：你的 Lucky Helmet 的条件是"受到招式伤害"，被 Powerful Hand 击倒时不会抽 2（推断，按卡牌文字）。
- Battle Cage 是对手的场地，Academy at Night 盖掉它就恢复你后备区指示物的效果；对手会再打 Battle Cage，你也要多备一张。
- Eri（看你手牌，弃 2 张物品）：Poké Pad、Wondrous Patch 会被弃。关键目标宝可梦尽量放在牌库里，用 Codebreaking 在当回合叠到顶（推断）。
- Enhanced Hammer：你的 Telepathic Psychic Energy 和 Boomerang Energy 会被弃。轮到 Slowking 时尽量贴基本 Psychic Energy，Wondrous Patch 从弃牌区补（只补后备区）。
- 对手在你剩 3 张以下时才会用 Special Red Card 打乱你的手牌，你也可以反过来用：你方有 10 份卡表带 Special Red Card，对手剩 3 张以下时让对手手牌放到牌库底再抽 3，对手下个回合的手牌要从 3 张重新抽起，Powerful Hand 的伤害会明显下降（推断，本对局无数据）。

**关键卡与构筑**
- 你方（n 均 ≥ 15）：带 Lana's Aid 高 20.0 个百分点（16 对 55）；带 Annihilape 高 19.9（48 对 23）。Lana's Aid 一次捡回最多 3 张无规则宝可梦或基本能量，契合一换六的消耗战（推断）。
- 对手方：带 Shaymin 的卡表对你高 27.3 个百分点（49 对 19），与"Shaymin 挡住 Trifrost 后备区伤害"的推断一致；带 Lucky Helmet 高 19.4（23 对 45，对手被你打时抽 2，手牌更大）；Dedenne 高 16.7（32 对 36）；Enhanced Hammer 高 13.3（40 对 28）；带 Night Stretcher 低 24.3（48 对 20）；Handheld Fan 低 19.9（39 对 29）；Psyduck 低 15.8（20 对 48）；Lillie's Clefairy ex 低 9.4（18 对 50，它是你 Thunder Raid 的 2 奖目标）。
- 建议：此对局 Lana's Aid 值得带（数据支持）。若环境里 Alakazam 多，Special Red Card 或 Cofagrigus 可作测试（推断）。

**常见失误**
- 对手后备区有 Shaymin 时仍用 Trifrost，只打出战斗场的 110。
- Battle Cage 在场时用 Ghostly Blow 指望后备区 5 个指示物。
- 把 Mega Kangaskhan ex、Latias ex 放上场抽牌或撤退，被 Powerful Hand 白拿 2 到 3 张。
- Fezandipiti ex 在对手后备区停了一回合都没去收（Thunder Raid 正好 210）。

---

## vs Mega Excadrill ex（胜率 64.0%，173 局）

**对局性质**
- 对手的主攻都是 Mega：Mega Excadrill ex（340 HP）、Mega Skarmory ex（260 HP），被击倒各给 3 张；Genesect ex（220）给 2 张。你击倒两只 Mega 就赢了。
- 对手 Maximum Drilling 200（3 个钢能量）击倒 Slowking；Undermine 90 打不倒 Slowking（120），但会弃你牌库顶 2 张。对手要击倒 6 只单奖的 Slowking，一般需要 6 个攻击回合（推断）。
- 能量引擎是 Metang（TEF 114，100 HP）的 Metal Maker，进化前 Beldum 和 Drilbur 都是 70 HP。

**开局与先后攻**
- 先攻（推断），让第 2 回合的 Trifrost 赶在 Metang 和 Mega Excadrill ex 进化之前。
- 不要把 Mega Kangaskhan ex 留在战斗场：Maximum Drilling 加满 5 个能量打 330，击倒 300 HP 的 Kangaskhan 送 3 张。

**奖赏卡路线**
- 你第 2 回合（取 3）：Trifrost 击倒 Beldum（70）、Drilbur（70）、Metang（100）中的 3 只（对手后备区有 Shaymin 时只有战斗场受伤）。
- 你第 3 回合（取 3）：后备区的 Mega Skarmory ex（260）吃过 Trifrost 后，Thunder Raid 210 补到 320，击倒拿 3 张。战斗场的 Mega Excadrill ex：SSP 100 版 Annihilape 的 Destined Fight 直接同归于尽，你送 1 张，拿 3 张。
- 你第 4 回合（取最后 1 到 3 张）：剩下的 Genesect ex（220）后备区时 Trifrost 110 + Thunder Raid 210 = 320 击倒；残血小怪 Trifrost 收。
- 不带 Destined Fight 时，满血 Mega Excadrill ex 要三步：Trifrost 110 + Thunder Raid 210（它在后备区时）= 320，还差 20；加 Munkidori 30 或 Ghostly Blow 的 5 个指示物。Hero's Cape（58% 卡表）再 +100 到 440 时更难，优先打别的目标。

**对手的套路，怎么防**
- Undermine 弃你牌库顶 2 张：会弃掉 Codebreaking 留给下回合的那张。下回合的目标靠 Poké Pad + Academy at Night 在当回合放，不提前叠（推断）。
- Mega Skarmory ex 的 Sonic Ripper 对任一宝可梦 220：能狙你后备区的 Latias ex、Clefairy ex、Fezandipiti ex（各 2 张）和任何 Slowking。这些 ex 尽量不上场。
- Genesect ex 每回合找 2 只钢属性进化宝可梦，拖久了对手两条线都会起来：它在后备区时（非 Tera）是 Trifrost + Thunder Raid 的目标。
- Team Rocket's Petrel 能找任何训练家，包括场地卡（Gravity Mountain）盖掉 Academy at Night；Gravity Mountain 只影响 2 阶，对 Slowking 无影响。
- Jumbo Ice Cream（身上 3 个以上能量时回 80）：Excadrill 吃了 110 后回到 310。要么一回合打到位，要么在它能量不足 3 个时打（推断）。

**关键卡与构筑**
- 你方（n 均 ≥ 15）：带 Zeraora 低 9.6 个百分点（36 对 15）；Lucky Helmet 高 8.6（24 对 27）；Secret Box 高 8.0（31 对 20）；Surfer 和 Prime Catcher 差别不到 2 个百分点。Annihilape 不带的样本只有 10 局，不引用。
- 对手方：带 Shaymin 的卡表对你高 29.5 个百分点（24 对 23），与"Shaymin 挡住 Trifrost 后备区伤害"一致；Fezandipiti ex 高 19.2（32 对 15）；Hero's Cape 高 15.0（20 对 27）；Pokégear 3.0 高 14.4（26 对 21）；Team Rocket's Transceiver 低 22.4（15 对 32）；Precious Trolley 低 10.3（18 对 29）。
- 建议：这是优势对局，不必为它改卡表；SSP 100 版 Annihilape 的 Destined Fight 在此对局账面价值最高（3 换 1）（推断，数据样本不足）。

**常见失误**
- Thunder Raid 打满血的 Mega Excadrill ex（210 对 340）。
- Shaymin 在对手后备区时还用 Trifrost 打后备区小怪。
- 用 Codebreaking 叠下回合的目标，被 Undermine 弃掉。
- Kangaskhan 留在战斗场，被 330 一击送 3 张。

---

## vs Dragapult Blaziken（胜率 47.9%，208 局）

**对局性质**
- Dragapult 骨架（Dreepy 4、Drakloak 4、Dragapult ex 2）加 Torchic（70）→ Combusken（100）→ Blaziken ex（320，2 张 Rare Candy）。Blaziken ex 的 Smolder-sault 200 击倒 Slowking，Seething Spirit 每回合从弃牌区补能量。
- Blaziken ex 不是 Tera，在后备区也吃招式伤害：Trifrost 110 + Thunder Raid 210 = 320，正好击倒。
- 对手两只主攻各 2 张，加上 Munkidori ×2（110）、Budew（30）。你的拿奖思路和 Dragapult ex 相同：前期 Trifrost 收小怪，中期两步收一只 Blaziken ex。

**开局与先后攻**
- 先攻（推断）。对手有 Rare Candy，Blaziken ex 最早在对手第 2 回合上场；Dragapult ex 仍要第 3 回合。
- 51% 的对手卡表带 Lillie's Clefairy ex，它的 Fairy Zone 只影响你的龙属性（Kyurem），而 Kyurem 平时不上场，影响很小。

**奖赏卡路线**
- 你第 2 回合（取 3）：Trifrost 击倒 Torchic（70）、Combusken（100）、Dreepy（70）、Drakloak（90）、Munkidori（110）中的 3 只，优先 Torchic/Combusken（断 Blaziken ex）和 Munkidori。
- 你第 3 回合（铺伤害或取 2）：后备区已有 Blaziken ex 就 Trifrost 打它 110（加另外两只小怪），下回合 Thunder Raid 210 收；后备区有 Fezandipiti ex、Meowth ex 就直接 Thunder Raid。
- 你第 4 回合（取 2）：Thunder Raid 收后备区的 Blaziken ex（110 + 210 = 320）。
- 战斗场的 Dragapult ex 按 Dragapult ex 章节处理（Fairy Zone 下 Metallic Hammer 600 一击，没有 Clefairy 时 300 + 补 20）；战斗场满血 Blaziken ex（320）吃 Metallic Hammer 也剩 20，同样要补 20，或用 Destined Fight。

**对手的套路，怎么防**
- Chi-Yu（TWM 39）的 Ground Melter：有场地时 120 并弃掉场地，正好击倒 Slowking 还拆掉 Academy at Night。多备一张 Academy at Night。
- Blaziken ex 打完 Smolder-sault 下回合不能攻击，对手会和 Dragapult ex 轮流打：在 Blaziken ex 刚攻击完的回合优先处理 Dragapult 线（推断）。
- Phantom Dive + Munkidori 收后备区 Slowpoke、Risky Ruins：同 Dragapult ex 章节。

**关键卡与构筑**
- 你方（n 均 ≥ 15）：带 Annihilape 高 20.3 个百分点（47 对 21）；Lucky Helmet 高 13.0（35 对 33）；Brave Bangle 高 4.7（18 对 50）；Prime Catcher 低 15.6（15 对 53）；Crispin 低 11.9（16 对 52）；Cofagrigus 低 9.1（16 对 52）；Munkidori 低 8.5（17 对 51）。
- 对手方：带 Lillie's Clefairy ex 的卡表对你高 27.3 个百分点（29 对 38），原因没有从卡牌文字推出（Fairy Zone 对你几乎无影响；Full Moon Rondo 按双方后备区数加伤害或是原因之一，推断）；Shaymin 高 24.3（21 对 46）；Area Zero Underdepths 高 5.4（18 对 49）；带 Judge 低 24.4（51 对 16）；Special Red Card 低 8.0（48 对 19）；Chi-Yu 低 7.2（37 对 30）；Risky Ruins 低 6.3（32 对 35）。
- 建议：此对局 Annihilape 值得保留（数据支持）。

**常见失误**
- Thunder Raid 打满血 Blaziken ex（210 对 320）。
- 让 Torchic/Combusken 活过你的第 2 回合，Blaziken ex 上场后对手每回合都有能量补给。
- 场上只剩一张 Academy at Night 时被 Chi-Yu 拆掉，下回合放不了目标。

---

## vs Festival Lead（胜率 49.0%，128 局）

**对局性质**
- 对手全是单奖、低 HP：Grookey 70、Thwackey 100、Applin 40、Dipplin 80、Goldeen 50、Seaking 110、Rellor 50、Rabsca 70、Shaymin 80。Trifrost 110 能一击击倒对手卡表里每一只宝可梦。
- Festival Grounds 在场时，带 Festival Lead 的 Dipplin（TWM 18）可以攻击两次：Do the Wave 每只后备区宝可梦 20，后备区 5 只就是 100 + 100 = 200，击倒 Slowking；第一下击倒的话第二下打新上来的。
- 对手挡 Trifrost 的手段：Rabsca（TEF 24，98% 卡表）让后备区不受招式伤害和效果；Shaymin（DRI 10，82%）让后备区无规则宝可梦不受招式伤害。它们在场时，Trifrost 只打得到战斗场。
- 所以这一局的核心是两件事：用 Academy at Night 盖掉 Festival Grounds，和先拆掉 Rabsca / Shaymin（推断）。

**开局与先后攻**
- 先攻（推断）：你第 2 回合时对手的 Rellor 可能还没进化成 Rabsca。
- 战斗场 Slowpoke。Mega Kangaskhan ex 不怕单次 Do the Wave，但 Gladion's Final Battle（非规则宝可梦 +80）+ Brave Bangle（对 ex +30）让 Dipplin 一下 210、两下 420，会被一回合击倒送 3 张；没有 Gladion 时，Kieran（94% 卡表）+ Brave Bangle 在对手后备区 5 只时也有 160×2 = 320。

**奖赏卡路线**
- 你第 2 回合（取 1 到 3）：如果对手后备区还没有 Rabsca 和 Shaymin，Trifrost 打战斗场 + 2 只后备区（优先 Rellor、Thwackey、Dipplin），最多 3 张。
- 有 Rabsca 或 Shaymin 时（取 1）：先拆防护。Prime Catcher（28% 卡表）把 Rabsca 或 Shaymin 拉到战斗场击倒；注意 Rabsca 在战斗场时特性仍然保护后备区，所以这一回合只能拿 1 张（推断）。没有 Prime Catcher 就每回合 Trifrost 打战斗场 110（任何战斗场宝可梦一击），等对手换上防护宝可梦。
- 防护拆掉后（每回合取 3）：Trifrost 一次 3 张。
- 每回合都用 Academy at Night 盖掉 Festival Grounds：Dipplin 只能打一次，后备区满 5 只是 100，打不倒 Slowking（120）。例外是对手打出 Gladion's Final Battle（最后一张手牌时，非规则宝可梦 +80），单次也有 180，所以对手手牌只剩 1 张时要预期这一下。

**对手的套路，怎么防**
- Festival Grounds ×4 与你的 Academy at Night ×4 拉锯。对手在自己回合打出 Festival Grounds 就能当回合连击，你挡不住当回合；但你在自己回合换掉它，对手下回合就得再用一张。
- Thwackey（战斗场有 Festival Lead 宝可梦时每回合从牌库任找 1 张）：3 只 Thwackey 是对手的引擎，Trifrost 优先。
- Festival Grounds 让身上有能量的宝可梦不受特殊状态影响：Pawmot、Drapion 的麻痹，SSP 100 Annihilape 的 Tantrum 自身混乱都受影响（对你有利的是 Tantrum 的混乱也不生效）。
- Tool Scrapper（69% 卡表）会弃掉你的 Lucky Helmet、Brave Bangle。
- Psyduck（35% 卡表）的 Damp 只关自爆类特性，对你没影响。

**关键卡与构筑**
- 你方（n 均 ≥ 15）：带 Surfer 高 18.1 个百分点（33 对 27）。其余你方卡（Unown、Pawmot、Budew、Lana's Aid、Switch 不带的一组）样本都不足 15。
- 对手方：带 Lana's Aid 高 12.3（18 对 35）；Psyduck 高 9.5（18 对 35）；Tool Scrapper 高 8.0（36 对 17）；Forest of Vitality 低 5.1（17 对 36）。Shaymin 不带的只有 11 局，不引用，但它挡 Trifrost 的作用是卡牌文字直接给出的。
- Unown 的 Mysterious Signal 40 可以击倒战斗场的 Applin（40 HP）并多拿 1 张（推断）。
- 建议：此对局 Prime Catcher 比 Secret Box 更有用，因为要把 Rabsca / Shaymin 拉出来（推断）。

**常见失误**
- Rabsca 或 Shaymin 在场时用 Trifrost 打后备区，伤害全被挡。
- 手上没有 Academy at Night，让 Festival Grounds 留在场上，被 200 连击。
- 指望 Pawmot / Drapion 的麻痹，而 Festival Grounds 在场时有能量的宝可梦免疫。

---

## vs Dhelmise（胜率 31.3%，114 局）

**对局性质**
- Dhelmise（PBL 39，140 HP，超属性，撤退 3）的 Vengeful Anchor 只要 1 个超能量，弃牌区有 4 只带 Hide 'n' Sneak 的宝可梦时打 170，一击击倒 Slowking。Gwynn、Ultra Ball、Prism Tower、Explorer's Guidance 让对手第 2 回合就凑够 4 只。
- Hide 'n' Sneak（Shuppet、Banette、Poltchageist、Sinistcha）挡住你招式和特性的效果：Ghostly Blow 的指示物、Cofagrigus、Munkidori 的挪指示物对它们无效。招式伤害不是效果，Trifrost 照样打得到。
- Dhelmise 本身没有 Hide 'n' Sneak，指示物和 Munkidori 都能作用在它身上。
- 对手 4 只 Dhelmise 是主要攻击手，Banette（PBL 34）的 Puppet Pull 只有 80，打不倒 Slowking，但正好击倒 80 HP 的 Slowpoke，还能从牌库任找 1 张。录像：Frankfurt 2026 第 1 天第 6 轮第 1 局，Launay 用 Boss's Orders 拉出 Gnoli 唯一贴了能量的 Slowpoke，Puppet Pull 击倒（[4:19:50](https://www.youtube.com/watch?v=8TMRgaIe7LQ&t=15590s)）。
- 对手 58% 的卡表（22/38）带 Shaymin（DRI 10，80 HP）：Flower Curtain 让后备区没有规则框的宝可梦不受招式伤害，对手除了 Lillie's Clefairy ex、Latias ex 全是无规则宝可梦，Trifrost 就只打得到战斗场和后备区的 ex。录像：同一局 Launay 放下 Shaymin 后，Gnoli 的 Trifrost 打不到后备区，只能靠复制 Annihilape 一只一只换。

**开局与先后攻**
- 先攻（推断），你要在对手 Dhelmise 打出 170 之前就开始换。
- 先攻也挡不住第一击：录像第 2 局 Launay 后攻，第 1 回合就用 Explorer's Guidance、Ultra Ball、Prism Tower 凑够 4 只打出 170。先攻只是逼对手第 1 回合就凑齐（推断）。
- 后备区少放 2 奖 ex：对手 Bloodmoon Ursaluna ex 后期 240，Boss's Orders ×3。

**奖赏卡路线**
- 关键算式：Dhelmise 140 = Trifrost 110 + Munkidori 30（Adrena-Brain 挪 3 个指示物）；在战斗场时 Metallic Hammer 一击。
- 你第 2 回合（取 1）：战斗场是 Dhelmise 就 Metallic Hammer 击倒；否则 Trifrost 打战斗场 + 后备区 Dhelmise + 1 只小怪，让后备区的 Dhelmise 提前吃 110。
- 对手后备区有 Shaymin 时先清它（推断）：Prime Catcher（28% 卡表）拉上来，Ghostly Blow 100 击倒，5 个指示物顺手放到后备区 Dhelmise 上；或者 Ghostly Blow 的 5 个指示物 + Munkidori 3 个 = 80 直接在后备区收掉。指示物不是伤害，Flower Curtain 挡不住，Shaymin 也没有 Hide 'n' Sneak。对手 Patrat 在场时 Munkidori 挪不了指示物，就要两次 Ghostly Blow。
- 麻痹换一回合：Pawmot 的 Voltaic Fist 130 打战斗场 Dhelmise 并让它麻痹（Dhelmise 没有 Hide 'n' Sneak，麻痹有效；Banette、Sinistcha 身上无效）。Dhelmise 撤退 3，对手 79% 的卡表（30/38）没有 Switch，下回合它打不了也撤不了；你再用 Unown 的 Mysterious Signal 40 收掉它，多拿 1 张。录像：第 2 局 Gnoli 这样追到 4 比 4（[4:43:55](https://www.youtube.com/watch?v=8TMRgaIe7LQ&t=17035s)）。
- 你第 3 回合起（每回合 1 到 2 张）：Munkidori 给吃过 110 的 Dhelmise 补 30 击倒，同时 Seek Inspiration 打新的战斗场。
- 2 奖目标：Lillie's Clefairy ex（190）、Latias ex（210，53% 卡表）在后备区时 Thunder Raid 一击；Bloodmoon Ursaluna ex（260）在后备区要 Trifrost 110 + Thunder Raid 210，在战斗场时 Metallic Hammer 300 一击。
- Trifrost 收 Shuppet（50）、Poltchageist（30）、Sinistcha（60）也算奖赏卡，但它们进弃牌区会帮对手凑 Sinistcha 的 Matcha Spin（6 只）和 Spiritomb（13 只）的条件。先打 Dhelmise，小怪是顺带的（推断）。

**对手的套路，怎么防**
- 每回合 170 击倒一只 Slowking：你也只能一回合一张地换，因此要让每只 Slowking 都确实拿到奖赏卡（推断）。
- Patrat（CRI 70，47% 卡表）的 Watchful Eye 让双方都不能挪指示物，Munkidori 失效。Patrat 70 HP，Trifrost 第一时间击倒。
- Sinistcha 的 Matcha Spin 给你全场每只放 4 个指示物：Slowpoke 80 会剩 40；之后 Dhelmise 打战斗场，再来一次 Matcha Spin 就收掉后备区的 Slowpoke。备用的 Slowpoke 尽早进化成 Slowking（120）。录像：第 2 局 4 比 4 时，Launay 用 Boss's Orders 和 Matcha Spin 一回合拿 4 张（其中 Lillie's Clefairy ex 2 张）结束比赛（[4:46:30](https://www.youtube.com/watch?v=8TMRgaIe7LQ&t=17190s)）。
- Legacy Energy（61% 卡表）：贴着它的宝可梦被击倒时你少拿 1 张，一局一次。击倒贴 Legacy Energy 的 Dhelmise 只拿 0 张，记得把这一张算进奖赏卡路线。录像：第 1 局 Gnoli 复制 Metagross 击倒一只 Dhelmise，因为 Legacy Energy 一张没拿（[4:30:35](https://www.youtube.com/watch?v=8TMRgaIe7LQ&t=16235s)）。

**关键卡与构筑**
- 你方（n 均 ≥ 15）：带 Munkidori（和 Darkness Energy）高 43.0 个百分点（18 对 20 局），是整份数据里最大的差值之一，与"Trifrost 110 + 30 = Dhelmise 140"的算式吻合；带 Crispin 高 34.7（16 对 22），Crispin 能一次找 Psychic + Darkness 两种基本能量，正好给 Munkidori 和 Slowking；Lucky Helmet 高 4.3（18 对 20）；带 Zeraora 低 14.5（17 对 21）。
- 对手方：带 Bloodmoon Ursaluna ex 的卡表对你低 11.3（18 对 17，它是 2 奖靶子）；Explorer's Guidance 低 3.9（17 对 18）；Spiritomb 高 3.3（15 对 20）。
- 建议：此对局必须带 Munkidori + 2 Darkness Energy + Crispin（数据支持，样本小但差值很大）。
- 录像：Frankfurt 第 46 名 Gnoli 的卡表三样都没带（带了 Pawmot、Unown 各 1），第 6 轮 0-2 输给 Launay。只是一场；没有 Munkidori，后备区的 Shaymin 和 Dhelmise 只能靠 Ghostly Blow 慢慢磨（推断）。

**常见失误**
- Ghostly Blow 的 5 个指示物或 Munkidori 的 3 个指示物放到 Hide 'n' Sneak 宝可梦身上（无效）；目标应该是 Dhelmise。
- Trifrost 只顾收后备区小怪，帮对手填弃牌区，Dhelmise 却一只没倒。
- 让 Patrat 留在场上，Munkidori 整局不能用。
- 对手后备区有 Shaymin 还按"Trifrost 先铺后备区 110"的路线打，后备区一点伤害都没有。

---

## vs Ogerpon Meganium Hydrapple（胜率 41.7%，92 局）

**对局性质**
- 对手是能量堆叠：Meganium（MEG 10，160 HP，1 张）的 Wild Growth 让每个基本草能量当 2 个草能量，Teal Mask Ogerpon ex（210，Tera）和 Hydrapple ex（330，非 Tera）每回合用特性额外贴能量。Teal Mask Ogerpon ex 的 Myriad Leaf Shower 30 + 双方战斗场每个能量 30，你的 Slowking 身上有 2 个能量也算进去，很容易打到 120 以上。
- Meganium 是引擎，倒了对手伤害就掉；它的进化线 Chikorita 70、Bayleef（MEG 9）110，都在 Trifrost 一击范围内。
- 对手 Forest of Vitality ×4 让草宝可梦放下当回合就能进化（第 1 回合除外），所以 Meganium 最早对手第 2 回合上场。

**开局与先后攻**
- 先攻（推断）：你第 2 回合（整局第 3 回合）早于对手第 2 回合，可以在 Meganium 进化前击倒 Chikorita。
- Forest of Vitality 会盖掉你的 Academy at Night，反之亦然：你换掉它，对手当回合就不能一口气进化到 2 阶。

**奖赏卡路线**
- 你第 2 回合（取 2 到 3）：Trifrost 击倒 Chikorita（70）、Bayleef（110）、Applin（40）、Dipplin（80 或 90）、Celebi（80）中的 3 只，优先 Meganium 线。
- Meganium 已上场（160）：在后备区时 Trifrost 110 + Ghostly Blow 5 指示物 = 160 击倒（两回合）；在战斗场时 Metallic Hammer 一击。
- 2 奖目标：后备区的 Meowth ex（170）、Fezandipiti ex（210）Thunder Raid 一击。Hydrapple ex（330）在战斗场时 Metallic Hammer 300 + Brave Bangle 30 = 330 一击；在后备区要 Trifrost 110 + Thunder Raid 210 = 320，还差 10，再加任何指示物；它的 Ripening Charge 贴能量时回 30，所以最好一回合补到位（推断）。录像：Baltimore 2026 四强 Dreitzler 用 Brave Bangle 加 Metallic Hammer 一下打倒满血 Hydrapple ex（[6:14:06](https://www.youtube.com/watch?v=nLkFmtXdXGE&t=22446s)），解说也把这当作这个对局的关键。
- Teal Mask Ogerpon ex（210）在后备区打不动（Tera），在战斗场时 Metallic Hammer 一击，或 Destined Fight。

**对手的套路，怎么防**
- Myriad Leaf Shower 吃你战斗场的能量数：Slowking 只贴 2 个能量，不要多贴（推断）。
- Tapu Bulu（SFA 6）220 单奖攻击手；Briar（你剩 2 张时，对手太晶宝可梦击倒战斗场多拿 1 张）。
- Judge、Unfair Stamp 打乱手牌，影响同前。

**关键卡与构筑**
- 本对局双方各卡的样本都不足 15（你方 Surfer 13 对 12），不引用。
- 建议：按卡牌文字，Brave Bangle 让 Metallic Hammer 一击 Hydrapple ex；Munkidori 和 Ghostly Blow 对后备区 Meganium 160 的两步击倒有帮助（推断）。

**常见失误**
- Trifrost 打后备区的 Teal Mask Ogerpon ex。
- 放着 Chikorita/Bayleef 不打，让 Meganium 上场。
- Thunder Raid 打满血 Hydrapple ex（210 对 330）。

---

## vs Crustle（胜率 68.0%，129 局）

**对局性质**
- Crustle（DRI 12，150 HP，带 Growing Grass Energy 170，带 Hero's Cape 再 +100）的 Mysterious Rock Inn 只挡宝可梦 ex 的招式伤害。Slowking 不是 ex，所有复制招式全额生效；你的 Mega Kangaskhan ex、Latias ex 打它是 0。
- 对手 Superb Scissors 120 正好击倒 Slowking；对手的 Mega Kangaskhan ex（4 张）打 200 起，但被击倒给你 3 张。
- 你有 Trifrost：一次打 3 只 Crustle 各 110，第二次 Trifrost 就把三只都打到 220（超过 170）。这是 Slowking 胜率最高的对局之一。

**开局与先后攻**
- 先攻（推断）。Dwebble（DRI 11，70 HP）的 Ascension 要在战斗场用 1 个无色才能进化，你第 2 回合的 Trifrost 能直接收后备区的 Dwebble。
- 战斗场 Slowpoke；自己的 Kangaskhan 只当抽牌用，别在对手 Kangaskhan 能打的时候放战斗场。

**奖赏卡路线**
- 你第 2 回合（取 1 到 3）：Trifrost 打 Dwebble（70，一击）和 Crustle（150/170，剩 40/60）。
- 你第 3 回合（取 2 到 3）：再一次 Trifrost，三只吃过 110 的 Crustle 全倒（Hero's Cape 那只 250 或 270 除外，留给 Metallic Hammer）。
- 对手的 Mega Kangaskhan ex：在后备区时 Trifrost 110 + Thunder Raid 210 = 320 ≥ 300，拿 3 张；在战斗场时 Destined Fight 一换一（送 1 拿 3），或 Brave Bangle 让 Slowking 对战斗场 ex 多 30。
- 收尾：Metallic Hammer 300 一击任何满血 Crustle（最高是 Hero's Cape 加 2 个 Growing Grass Energy 的 290）。

**对手的套路，怎么防**
- 回复：Jumbo Ice Cream（身上 3 个以上能量时回 80）、Pokémon Center Lady 回 60、Bianca's Devotion 只能回剩余 HP 30 以下的宝可梦。Trifrost 后 Crustle 剩 40（150 HP）或 60（170 HP），Bianca's Devotion 用不了（推断，按卡牌文字）；所以 Trifrost 后下回合尽快补刀，别给 Jumbo Ice Cream 时间。
- Spiky Energy：贴着它的 Crustle 在战斗场受伤时给你的攻击手放 2 个指示物，Slowking 打两次就掉 40。
- Mist Energy：挡住招式效果，Ghostly Blow 的后备区指示物、Pawmot 的麻痹对贴了它的 Crustle 无效；伤害照算。
- Eri、Xerosic's Machinations 打手牌：Kyurem 放在牌库里，用 Codebreaking 当回合叠到顶（推断）。
- 对手的场地卡（Lumiose City、Team Rocket's Factory、Prism Tower、Festival Grounds）会盖掉 Academy at Night。

**关键卡与构筑**
- 你方（n 均 ≥ 15）：带 Secret Box 高 28.4 个百分点（35 对 18），带 Prime Catcher 低 28.4（18 对 35），两者是同一个 ACE SPEC 位置的取舍；Brave Bangle 高 25.6（16 对 37），与对付对手 Kangaskhan 吻合；Lucky Helmet 高 13.3（23 对 30）；Munkidori / Crispin / Darkness Energy 低 17.1（18 对 35）。
- 对手方：带 Bianca's Devotion 的卡表对你低 34.1（23 对 15），与上面的推断一致；Festival Grounds 高 28.3（23 对 15）；Prism Tower 低 13.8（22 对 16）。
- 建议：此对局 ACE SPEC 用 Secret Box（数据支持）。

**常见失误**
- 让 Mega Kangaskhan ex 或 Latias ex 攻击 Crustle（伤害为 0）。
- Trifrost 之后不补刀，让对手用 Jumbo Ice Cream 或 Pokémon Center Lady 回满。
- 放过对手后备区的 Kangaskhan，没有用 Trifrost + Thunder Raid 拿 3 张。

---

## vs Alakazam Dusknoir（胜率 29.4%，34 局）

**对局性质**
- 样本只有 34 局，带牌对比没有可用数据。对手是 Alakazam（MEG 56）+ Dusknoir（PRE 37）：Powerful Hand 手牌 6 张就击倒 Slowking，Dusknoir 的 Cursed Blast 13 个指示物能直接收你后备区任何一只 Slowking。
- 对手还有 Shaymin（DRI 10，挡 Trifrost 的后备区伤害）、Budew（锁物品）、Strange Timepiece（把自己的超属性进化宝可梦退化，重复用进化抽牌和 Dusclops/Dusknoir）、Prime Catcher、Special Red Card ×2。

**开局与先后攻**
- 先攻（推断），理由同 Alakazam Dudunsparce。第 1 回合先把 Kyurem 拿在手上，防 Budew 锁物品。

**奖赏卡路线**
- 你第 2 回合：对手后备区无 Shaymin 时 Trifrost 收 Duskull（60）、Abra（50 或 40）、Kadabra（80）；有 Shaymin 时 Metallic Hammer 打战斗场。
- 之后：Metallic Hammer 一击 Alakazam（140）和 Dusknoir（160）。
- 2 奖目标：Fezandipiti ex（95% 卡表）在后备区时 Thunder Raid 210 一击。

**对手的套路，怎么防**
- Cursed Blast 每次送你 1 张：对手 6 张里有几张是用自爆换的，算清楚你还差几张（推断）。
- 后备区的 2 奖 ex 会被 Dusknoir 130 + 其他指示物收掉，只放必要的。

**关键卡与构筑**
- 无可用数据。按卡牌文字，Alakazam Dudunsparce 章节里的建议（Lana's Aid、Special Red Card）同样适用（推断）。

**常见失误**
- 有 Shaymin 时 Trifrost 打后备区。
- 后备区摆 Mega Kangaskhan ex 或 Latias ex，被 Prime Catcher 拉出来用 Powerful Hand 收。
