# 项目共享文件夹备份

这里是 Claude 项目共享文件夹（云端 `/mnt/project-files/`）的备份，目录结构和共享文件夹一致。在电脑上 `git pull` 就能拿到最新的一份。

| 路径 | 内容 |
|---|---|
| `video-reviews/` | 每场看过的比赛视频一份复盘，`streams.md` 是各大赛的直播视频清单和复盘顺序 |
| `deck-selection/2026-10-04_TEF-30C.md` | 选卡组分析报告 |
| `feedback/feedback-template.md` | 随复盘发给玩家的英文反馈模板；玩家反馈原文（`feedback/raw/`）有名字，不放这里 |

## 没放进这里的内容

这个仓库是公开的，所以下面几样不放在这里：

- 对局手册的副本（共享文件夹的 `deck-selection/matchups/`）：和仓库里的 `data/matchups/` 完全相同，直接看那里。
- Sebastian 的 TCG Live 对局复盘（`2026-10-05_maxevil95.md`、`2026-10-06_maxevil95.md`，Maxevil95 是他的账号）和反馈机制方案（`feedback/反馈机制方案.md`）：里面有朋友的游戏账号和名字。
- 你上传的截图、项目记忆、项目对话记录：有个人信息。

这些都在项目里的备份压缩包 `backup/ptcg-project-backup-<日期>.zip` 里，压缩包也包含上面这些公开文件，从项目文件里下载。

## 怎么保持最新

以后哪个线程往共享文件夹写了可以公开的文件，就同时提交到这个目录的同一路径。含个人信息的文件只留在共享文件夹，需要时再打一次压缩包。
