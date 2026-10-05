# Utrecht 2026 区域赛复盘

比赛 2026-05-16，环境 TEF-POR（比现在少 CRI、PBL、30C 三个系列），下面用到的关键卡现在都还合法。卡组和成绩对照 data/tournaments/2026-05-16_535_regional-utrecht。八强：Posledni（Mega Lopunny Dudunsparce，冠军）、Kunukcu（Dragapult ex，亚军）、Pobega、Mesman、Bonsee（都是 Dragapult ex）、Vanoverschelde（Team Rocket's Honchkrow）、Burke（Dragapult Dusknoir）、Battistella（Basic Box）。直播播了决赛、一场四强、一场八强，都已看完。

做法：没有调用 API，在你电脑上看截图、对照解说写成。三场都没有奖赏卡读数，按解说整理。

Mega Lopunny 和 Team Rocket's Honchkrow 都不在手册的对手里（世界赛之后的四场比赛里 Lopunny 约占 2%-5%，Honchkrow 约 2%），所以只把对现有对局也成立的部分写进手册。判断台账里这三个对局都没有登记判断。

## 决赛：Posledni（Mega Lopunny Dudunsparce）2-1 Kunukcu（Dragapult ex）

视频：https://www.youtube.com/watch?v=lLy0TaVIhvc （三局完整）。Hasan Kunukcu 是手册主线（4 张 Crushing Hammer）。Miloslav Posledni 的反 Dragapult 配置：4 张 Mist Energy（挡 Phantom Dive 的效果）、3 张 Battle Cage（挡后备区指示物）、4 张 Wally's Compassion（治好 Mega 宝可梦并收回能量）、Enriching Energy（ACE SPEC，贴上抽 4）、4 只 Dunsparce。解说："这些卡就是为了赢 Dragapult。"

### 第 1 局：Posledni 胜

- Kunukcu 起手 Fezandipiti ex 在战斗场，正好在 Mega Lopunny 的 Gale Thrust 范围里。Budew 锁物品几乎没用，对手靠 Hilda 找进化和能量。
- Kunukcu 的 Unfair Stamp 大回合（[11:00](https://www.youtube.com/watch?v=lLy0TaVIhvc&t=660s)）：Crushing Hammer 打 Enriching Energy 两次都是反面。对手用 Battle Cage 换掉 Risky Ruins，Wally's Compassion 治疗后再抽 4。
- Kunukcu 先收三只单奖宝可梦，剩 3 张（[18:00](https://www.youtube.com/watch?v=lLy0TaVIhvc&t=1080s)）。但他打 Judge 时对手场上有两只 Dunsparce，对手靠 Dudunsparce 的 Run Away Draw 把牌抽了回来。Posledni 用 Boss's Orders 拉出 Kunukcu 的 Meowth ex、Fezandipiti ex 这类 2 奖 ex 收掉（[23:00](https://www.youtube.com/watch?v=lLy0TaVIhvc&t=1380s)）。

### 第 2 局：Kunukcu 胜

- Crushing Hammer 正面，拆掉 Enriching Energy（[29:00](https://www.youtube.com/watch?v=lLy0TaVIhvc&t=1740s)）。
- 对手场上没有 Dunsparce 时才打 Judge（[39:30](https://www.youtube.com/watch?v=lLy0TaVIhvc&t=2370s)）。
- 对手的第三张 Battle Cage 在奖赏卡里。Kunukcu 用 Risky Ruins 换掉 Cage，Hammer 拆掉 Mist，一回合拿 4 张收尾（[45:00](https://www.youtube.com/watch?v=lLy0TaVIhvc&t=2700s)）。

### 第 3 局：Posledni 胜

- Battle Cage 一直在场，Hammer 用不上，Posledni 先拿 2 张。
- Kunukcu 打 Unfair Stamp 加 Judge，Phantom Dive 击倒 Mega Lopunny，Munkidori 挪指示物收掉 Dunsparce，又是 4 张，只剩 1 张（[1:03:30](https://www.youtube.com/watch?v=lLy0TaVIhvc&t=3810s)）。
- Posledni 先放 Battle Cage 拖慢对手，再找齐 Boss's Orders 和能量，Gale Thrust 收掉最后的奖赏卡夺冠（[1:05:30](https://www.youtube.com/watch?v=lLy0TaVIhvc&t=3930s)）。

### 对照手册

dragapult-ex.md 没有 Lopunny 一节，能对上的现有条目：vs Alakazam Dudunsparce 的"Risky Ruins 留给 Battle Cage"（第 2 局正是在 Ruins 换掉 Cage 的回合拿 4 张）；Hammer 打对手的关键特殊能量（这里是 Enriching 和 Mist）。

写进手册的（PR #31）：

1. vs Alakazam Dudunsparce 的"Judge 把对手打回 4 张，不代表下回合安全"那条加了这一场：Judge 之后，对手场上的 Dunsparce 只要进化成 Dudunsparce，就能用 Run Away Draw 再抽 3；第 1 局对手场上有两只 Dunsparce 时打 Judge 被抽了回来，第 2 局等对手场上没有 Dunsparce 才打。Alakazam Dudunsparce 也靠 Run Away Draw 抽牌，道理一样。
2. 没写进手册的：Lopunny 对局的打法（别起手 Fez 在战斗场；先收三只单奖，或者等 Ruins 换掉 Cage 时一次拿 4 张；Hammer 先打 Enriching Energy）。只有一场录像，Lopunny 份额也小，等它进了主流卡组再单开一节。

dragapult-ex.yaml 也补了这一场的录像证据。

## 四强：Kunukcu（Dragapult ex）2-0 Vanoverschelde（Team Rocket's Honchkrow）

视频：https://www.youtube.com/watch?v=o3XA-rOny8A

- 对手的 Team Rocket's Articuno 挡住招式效果，Phantom Dive 的指示物放不上 Team Rocket 的基础宝可梦。Kunukcu 把 6 个指示物放在进化后的 Honchkrow 和 Porygon2 上；第 1 局一发 Phantom Dive 同时击倒两只（[11:30](https://www.youtube.com/watch?v=o3XA-rOny8A&t=690s)）。Munkidori 的特性不受 Articuno 影响。
- 第 2 局：Boss's Orders 把 Articuno 拉到战斗场困住（对手只有 Giovanni 能换位）；尽量用 Drakloak 的 Dragon Headbutt 收单奖宝可梦，不让 Dragapult ex 上前送 2 张；对手拿牌后打 Unfair Stamp（[31:30](https://www.youtube.com/watch?v=o3XA-rOny8A&t=1890s)）。最后 Risky Ruins 加两只 Munkidori 加 Phantom Dive 收尾（[49:00](https://www.youtube.com/watch?v=o3XA-rOny8A&t=2940s)）。
- 对手用 Ignition Energy（用完自己回弃牌区），Crushing Hammer 价值低。

Honchkrow 不在手册的对手里，没有改手册。

## 八强：Vanoverschelde（Team Rocket's Honchkrow）2-0 Battistella（Basic Box）

视频：https://www.youtube.com/watch?v=8P1sYYaNX8A 。Fabio Battistella 的 Basic Box 和手册核心大体一致。

- 第 1 局：Battistella 的 Unfair Stamp 在奖赏卡里。对手剩 3 张时，场上的 Mega Kangaskhan ex 就成了致命目标。他想用 Iron Leaves ex 换下 Kangaskhan，但 Iron Leaves 被 Porygon2 收掉（[13:30](https://www.youtube.com/watch?v=8P1sYYaNX8A&t=810s)）。
- 第 2 局：单奖的 Honchkrow 一击收掉 Kangaskhan，一次拿 3 张（[23:00](https://www.youtube.com/watch?v=8P1sYYaNX8A&t=1380s)）。解说："对 Honchkrow 时，Kangaskhan 不是盾。"

写进手册的（PR #31）：basic-box-m.md 的奖赏卡负担那条加了一句：对手全是单奖宝可梦时，Kangaskhan 的 3 张是对手最划算的目标，用完 Run Errand 就撤下来（推断）。这是第三次在录像里看到：NAIC 2026 青少年组决赛（Honchkrow，见 naic-2026.md）、Turin 2026 八强 B（Hop's Trevenant，见 turin-2026.md）、这一场。

basic-box-m.yaml 也补了这一场的录像证据。
