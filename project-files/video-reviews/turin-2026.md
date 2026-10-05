# Turin 2026 特别赛复盘

比赛 2026-06-06，环境 TEF-CRI（比现在少 PBL 和 30C 两个系列），下面用到的关键卡现在都还合法。卡组和成绩对照 data/tournaments/2026-06-06_540_special-event-turin。八强：López（Hop's Trevenant，冠军）、Kamerman（Slowking，亚军）、Nebuloni（Dragapult Blaziken）、Clark（我们的数据里叫 Raging Bolt Ogerpon，实际是 Basic Box 的骨架）、Hagen（Lillie's Clefairy）、Gorgos（Alakazam Dudunsparce）、Schulze（Dragapult Blaziken）、Vicêncio（Dragapult ex）。直播播了 5 场决赛圈（两场八强、两场四强、决赛），都已看完。

做法：没有调用 API，在你电脑上逐张看截图、对照解说写成。Turin 用的是旧版侧边面板（Frankfurt 读法），奖赏卡读数和解说一致。字幕一度被 YouTube 限流（HTTP 429），改下 YouTube 对英文直播的原始语音识别字幕（en-orig）后马上就拿到了（工具的修正见 PR #26、#28）。括号里是剩余奖赏卡。

判断台账（data/judgments/）里还没有这几场对局的判断，没有要记的验证结果；这次写进手册的关键判断登记成了新判断，编号写在各场的"写进手册的"里。

## 决赛：López（Hop's Trevenant）2-0 Kamerman（Slowking）

视频：https://www.youtube.com/watch?v=P1gzE_BFuUA （496 帧读出 442 帧）。Brennan Kamerman 的 Slowking：2 只 Mega Kangaskhan ex、2 只 Latias ex、Smoochum、Secret Box、Lana's Aid、Surfer、Brave Bangle、Lucky Helmet，没有 Zeraora、Boss's Orders 和 Prime Catcher。Jose López 的 Hop's Trevenant：4 Hop's Phantump、3 Hop's Trevenant、2 Hop's Snorlax、Hop's Dubwool、Hop's Cramorant、Lillie's Clefairy ex、Shaymin，4 张 Hop's Choice Band、4 张 Postwick、4 张 Mist Energy、Secret Box。解说把这场看成 Kamerman 最差的对局，他赛前自己也说："Shaymin 一下来，我大概就赢不了。"括号里 Kamerman 在前。

### 第 1 局：López 胜

- López 第 1 回合就把 Shaymin 放到后备区。Flower Curtain 让后备区没有规则框的宝可梦不受招式伤害，Trifrost 和 Fezandipiti ex 的 Cruel Arrow 都打不到后备区。Kamerman 没有 Boss's Orders 和 Prime Catcher，也拉不出 Shaymin。
- Kamerman 的 Metagross 击倒一只 Phantump（5/6）。这正好打开了 Hop's Trevenant 的 Horrifying Revenge（上回合有 Hop's 宝可梦被招式击倒，多打 100）。
- López 用 Corner（90，对手下回合不能撤退）把 Fezandipiti ex 困在战斗场，再击倒它（5/3）；210 击倒 Latias ex（4/1）；最后 Dubwool 进化时的特性把 Kamerman 后备区的宝可梦换到战斗场，拿下最后一张。

### 第 2 局：López 胜

- 又是 Shaymin；Kamerman 的 Smoochum 在奖赏卡里。
- López 用 Team Rocket's Petrel 找 Secret Box，一回合凑齐 Hop's Bag、Postwick、Snorlax 和 Air Balloon。Phantump 的 Splashing Dodge 一再抛出正面（下回合不受招式伤害和效果），后备区的攻击手贴着 Mist Energy。Kamerman 战斗场打不动、后备区打不到，也没有拉人的卡。
- Hop's Cramorant 的 Fickle Spitting（对手剩 3 或 4 张时才有伤害）击倒 Slowking，Dubwool 收尾。

### 对照手册

Hop's Trevenant 不在我们的 12 套主流卡组里，现在的环境里也没有（TEF-30C 的份额表里没有它），所以手册没有这个对局。能用上的是 Shaymin：它在场时 Slowking 的后备区伤害打不出来，而 Slowking 的卡表几乎不带拉人的卡。

写进手册的（PR #30）：slowking-scr.md 的通用规则加了一条 Shaymin：它挡什么（Trifrost 和 Cruel Arrow 的后备区伤害）、不挡什么（Thunder Raid 打后备区的 ex，Ghostly Blow、Cofagrigus 放的指示物），Slowking 卡表 103 份里 Boss's Orders 只有 2 份、Prime Catcher 29 份（和 Secret Box 都是 ACE SPEC），以这场决赛为例。复盘建议"Slowking 至少带 1 张 Boss"，没有照写：Slowking 对 Alakazam Dudunsparce（另一个常带 Shaymin 的卡组）的数据里，带 Prime Catcher 的卡表还低 2.1 个百分点（19 对 52 局），看不出拉人的卡有帮助。

## 四强 A：Kamerman（Slowking）2-0 Clark（Basic Box）

视频：https://www.youtube.com/watch?v=-2gCfGeqBm8 （482 帧读出 445 帧）。Toby Clark 的卡组在我们的数据里叫 Raging Bolt Ogerpon，实际是 Basic Box 的骨架：3 只 Mega Kangaskhan ex、3 只 Meowth ex、3 只 Teal Mask Ogerpon ex、2 只 Raging Bolt ex、2 只 Latias ex、Lillie's Clefairy ex、Wellspring Mask Ogerpon ex、Iron Leaves ex、Fezandipiti ex、Passimian、Chien-Pao，2 张 Glass Trumpet、Unfair Stamp、4 张 Area Zero Underdepths。括号里 Kamerman 在前。

### 第 1 局：Kamerman 胜

- Clark 唯一的 Wellspring Ogerpon 和唯一的 Water Energy 都在奖赏卡里，没有一次多拿的路线。
- [6:45](https://www.youtube.com/watch?v=-2gCfGeqBm8&t=405s) Kamerman 用 Academy at Night 把 Metagross 放到牌库顶，Seek Inspiration 复制 Metallic Hammer 300 击倒战斗场的 Latias ex（4/6）。Clark 击倒一只 Slowking（4/5），又拿下一只 2 奖（4/3）。
- [16:26](https://www.youtube.com/watch?v=-2gCfGeqBm8&t=986s) Hammer 300 击倒战斗场的满血 Mega Kangaskhan ex，拿 3 张（1/3）。
- Clark 的 Raging Bolt ex 差 1 个能量打不出击倒，也没摸到 Unfair Stamp。Kamerman 找到场地，用 Metagross 收尾。

### 第 2 局：Kamerman 胜

- Clark 第 1 回合没贴上能量，战斗场的 Kangaskhan 撤不下来。
- Kamerman 弃掉 Brave Bangle（解说："他牌组里没有扛得住 300 的"），第 2 回合 Hammer 击倒 Kangaskhan，拿 3 张（3/6）。
- Clark 用 Codebreaking 找到 Unfair Stamp，Iron Leaves ex 击倒 Slowking，但 Kamerman 剩下的两张手牌够用。
- Lana's Aid 加两张 Night Stretcher 排好两回合的攻击（1/5），拿下。两局 12 张奖赏卡里 6 张来自两只 Kangaskhan。

### 对照手册

Slowking vs Basic Box（44.6%）说中的：战斗场的 ex（包括满血 Kangaskhan）吃 Metallic Hammer 300 一击，手册的路线本来就以 Hammer 打头。Basic Box vs Slowking（51.3%）说中的：Kangaskhan 别在对手回合留在战斗场；带 Raging Bolt ex 和 Glass Trumpet 的构筑对 Slowking 胜率低，Clark 正是这一类。

写进手册的（PR #30）：

1. slowking-scr.md vs Basic Box 加了这场的录像一节：两局 6 张来自 Kangaskhan；Brave Bangle 在这个对局没用（对手没有 HP 超过 300 的），Kamerman 主动弃掉，和数据（带 Bangle 低 19.4）一致；被 Stamp 打到 2 张手牌也接得上，Lana's Aid 加 Night Stretcher 排好最后两回合。
2. basic-box-m.md vs Slowking：Metallic Hammer 那条补了录像，并写明 Slowking 第 2 回合打 300 不需要支援者，所以对手第 2 回合之前，我们的战斗场就该换成 1 奖宝可梦，或者场上有 Latias ex 让 Kangaskhan 能零撤退换下（登记成判断 bbm-slk-01，信心 70%）；关键卡里 Raging Bolt / Glass Trumpet 那组数据加了这一场作旁证；常见失误的 Kangaskhan 那条补了录像。
3. 没采纳的：复盘建议把 slowking-scr.md 的路线改成"先用 Metallic Hammer 打战斗场"，但路线本来就以 Hammer 打头，Trifrost 是 Metagross 放不到牌库顶时的替代。"Lucky Helmet 挂在战斗场的 Slowking 上缓冲 Stamp"这一场看不出效果，没写。

slowking-scr.yaml 和 basic-box-m.yaml 也补了这一场的录像证据。

## 四强 B：López（Hop's Trevenant）2-1 Nebuloni（Dragapult Blaziken）

视频：https://www.youtube.com/watch?v=8vgD89uRQOg （687 帧读出 624 帧）。Lorenzo Nebuloni 的 Dragapult Blaziken 没有 Crushing Hammer。两个卡组都不是我们的五套推荐卡组，这里只简要记录。

### 第 1 局：López 胜

- Phantump 靠 Postwick、Snorlax 和 Choice Band，一个能量就打 100 以上。López 用 Boss's Orders 先收掉 Combusken，断掉 Blaziken 线；Nebuloni 打 Unfair Stamp 后，他用 Hassel 补回手牌。

### 第 2 局：Nebuloni 胜

- Risky Ruins 加 Munkidori，再用 Rare Candy 上 Blaziken ex（320 HP，不是龙属性，Fairy Zone 管不到它）。Seething Spirit 和 Crispin 让他每回合多出好几个能量，López 投降。

### 第 3 局：López 胜

- Dubwool 进化时把 Torchic 换到战斗场击倒。Nebuloni 的 Stamp 没起作用：López 剩下的两张是 Secret Box 和 Telepathic Psychic Energy。
- Fairy Zone 下，Horrifying Revenge 加 Choice Band 一击 Dragapult ex，随后拿下。

### 对照手册

都不是我们的推荐卡组，只留在复盘里。Mist Energy 挡 Phantom Dive 的指示物，dragapult-ex.md 里已经写了；"先断 Combusken / Torchic 这条能量引擎"只对 Blaziken 版有用。

## 八强 A：Kamerman（Slowking）2-1 Vicêncio（Dragapult ex）

视频：第 2 天直播 https://www.youtube.com/watch?v=WuXEbywON7g&t=10274s （2:51 到 3:56，786 帧读出 575 帧）。Pedro Vicêncio 的 Dragapult ex 是我们手册的主线：3 张 Crushing Hammer、Judge、Unfair Stamp、Special Red Card、2 张 Team Rocket's Watchtower、Risky Ruins。Kamerman 的卡表见决赛一节。括号里 Kamerman 在前。

### 第 1 局：Vicêncio 胜

- Kamerman 的 Secret Box 在奖赏卡里，起手战斗场是 Kyurem；Budew 锁住他的物品。
- Vicêncio 用 Boss's Orders 拉出场上唯一的 Slowking 击倒（6/5）。
- Kamerman 用 Wondrous Patch 补能量、Switch 换上 Lillie's Clefairy ex，Full Moon Rondo 击倒 Dragapult ex（4/5）。
- Vicêncio 回以 Unfair Stamp 和 Watchtower，击倒 Clefairy（4/3）。Kamerman 手里没有 Academy at Night 和 Codebreaking，只能盲翻 Seek Inspiration，随后投降。

### 第 2 局：Kamerman 胜

- 战斗场的 Slowpoke 挂着 Lucky Helmet，Budew 每次 Itchy Pollen 都让他抽 2 张。
- Trifrost 击倒两只 Drakloak 和一只 Dreepy，拿 3 张。之后用 Codebreaking 把 Slowpoke 放到牌库顶，Seek Inspiration 复制它的 Tackle（30）击倒 Budew，省下 Metagross；最后用 Metagross 收尾。
- 赛后他说自己以为还剩 3 张、其实只剩 2 张，所以多打了一回合。

### 第 3 局：Kamerman 胜

- Vicêncio 起手 Meowth ex，两只 Dragapult ex 在奖赏卡里。他后备区只放了少量 Dreepy 来躲 Trifrost，Trifrost 还是打到了 Meowth ex、Drakloak 和 Dreepy。
- Vicêncio 的 Crushing Hammer 是反面，Kamerman 拿下。

### 对照手册

两人都是两份手册的主线卡表。Slowking vs Dragapult ex（53.6%）和 Dragapult ex vs Slowking（40.1%）都说中的：Trifrost 收进化前宝可梦；Boss's Orders 拉唯一的 Slowking；Unfair Stamp、Watchtower、Judge、Crushing Hammer 拖慢 Slowking。

写进手册的（PR #30）：

1. slowking-scr.md vs Dragapult ex：对手用 Budew 锁物品时，战斗场的 Slowpoke 挂 Lucky Helmet，每次 Itchy Pollen 抽 2 张（登记成判断 slk-dpx-02，信心 55%，本对局带 Lucky Helmet 的卡表数据略差）；只剩 Budew 这类小目标时复制 Slowpoke 的 Tackle（30），省下 Metagross；唯一的 Slowking 被收掉时 Lillie's Clefairy ex 也能打（Full Moon Rondo，Fairy Zone 下对龙属性翻倍，按卡牌文字双方后备区合计 7 只就能一击 Dragapult ex），但它送 2 张。
2. dragapult-ex.md vs Slowking：对手战斗场挂 Lucky Helmet 时 Itchy Pollen 会让对手抽 2 张；后备区少放 Dreepy 也挡不住 Trifrost 打战斗场；Watchtower 那条加了第 1 局的 Stamp 加 Watchtower。
3. 没采纳的："Secret Box 在奖赏卡里时靠 Academy 和 Codebreaking 控制牌库顶"，通用规则里已经有。

slowking-scr.yaml 和 dragapult-ex.yaml 也补了这一场的录像证据。

## 八强 B：López（Hop's Trevenant）2-0 Hagen（Lillie's Clefairy）

视频：第 2 天直播 https://www.youtube.com/watch?v=WuXEbywON7g&t=14176s （3:56 起）。Emma Hagen 的卡组是 4 只 Mega Kangaskhan ex、4 只 Meowth ex、4 只 Lillie's Clefairy ex、3 只 Latias ex 的 Clefairy 盒子，带 Prime Catcher、2 张 Lillie's Pearl、4 张 Area Zero Underdepths、Prism Tower，没有手牌干扰，和 NAIC 冠军 Kowalski 是同一类。两边都不是我们的推荐卡组，只简要记录；两局中段的击倒对象和时间是粗略整理，胜负按解说和赛后采访。

### 第 1 局：López 胜（[3:59:30](https://www.youtube.com/watch?v=WuXEbywON7g&t=14370s) 起）

- Hagen 唯一的 Water Energy 卡在战斗场的 Kangaskhan 上，打不出 Torrential Pump。
- López 用 Hop's Cramorant 的 Fickle Spitting 和 Horrifying Revenge 把伤害叠在两只 Mega Kangaskhan ex 上，各拿 3 张，最后用 Boss's Orders 拉出后备区那只收尾。解说提到 Hagen 自己的 Prism Tower 帮 López 找到了 Night Stretcher。

### 第 2 局：López 胜（[4:14:00](https://www.youtube.com/watch?v=WuXEbywON7g&t=15240s) 到 4:34:30 投降）

- Hagen 给 Clefairy 挂 Lillie's Pearl（被击倒只送 1 张），用 Prime Catcher 先收掉加伤的 Snorlax；López 一度摸不到 Trevenant。
- Hagen 一直凑不齐 Area Zero 和 Chien-Pao，弃不掉受伤的 Kangaskhan。López 手里留着两张 Boss's Orders（对手没有手牌干扰），最后 Boss 加 Snorlax 加伤收掉，Hagen 投降。

### 对照手册

都不在我们的推荐卡组里，不改手册。备忘：Mega Kangaskhan ex 送 3 张，对高 HP 的单奖卡组是最大的靶子，受伤后要尽快处理掉（NAIC 青少年组决赛 Honchkrow 那场也是这样）。以后 Basic Box 手册加单奖卡组的对局时可以合并写。
