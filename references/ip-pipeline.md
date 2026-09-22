# 游戏/影视 IP 主题流水线（区别于名画公有领域流水线）

名画主题（vangogh/monet/ukiyo）走 Wikimedia Commons 公有领域扫描画；游戏/影视
IP 主题（black-myth-wukong / ghost-of-tsushima / cyberpunk-2077 /
no-rest-for-the-wicked / starcraft）没有公有领域原画，壁纸来源完全不同。

## 先问清需求方向（v1 返工 4 轮的教训）

「做个 X 主题」有两种完全相反的解读，动手前必须确认：
- **官方素材路线**：直接收集该 IP 的官方重制版/宣传原画/高清截图（实测：某个 IP 主题在
  "官方 Remastered 原画"，AI 生成的
  "风格致敬"被否决："我要的是星际争霸重制版的高清壁纸"）
- **原创风格致敬路线**：AI 生成"XX 风格"场景（规避版权，不出现具体
  单位/Logo/角色）——只在用户明说"怕版权/要原创"时采用

同一句「星际争霸1主题」，两条路线产出完全不同的东西。猜错方向 = 多轮返工。

「官方素材」还要钉到**作品版本**，不只是 IP：SC2 时代的图（Nova、SC2 版
Kerrigan、SC2 界面截图）混在官方同源池里同样会被整批否决——用户要的是
SC1 Remastered。确认需求时连版本口径一起确认；续作素材不因「同 IP」自动
合格。跨界同人图同理（动漫少女/其他游戏角色/纯 logo 都混得进 "starcraft"
搜索结果）。

## 官方素材路线

素材来源分两级，从上往下用——跳过一级只搜壁纸站，用户会以「模糊不清」
整体打回（社区转传版再热门也是二手分辨率）：

### 一级来源：官网/官方 CDN（一手，优先）

- 游戏官网多为 JS 渲染 SPA，curl 只拿到骨架——但资产直链就写在 HTML 里
  （Blizzard 系走 ContentStack CDN，域名形如 blz-contentstack-images.akamaized.net）。
  做法：`curl -sL <官网URL>` → grep CDN 域名 → 提取全部资产 URL 批量下载
- **改 URL 抠高清**：CDN 路径里的数字常是尺寸档位（`…_background_1600` →
  `…_2600`），`_mobile` 后缀是小图变体。逐档试更大的数字，magick identify
  验证实际分辨率后再入库
- 官网 media gallery / carousel 截图本身就是官方壁纸级素材——单一大来源
  拿满整套（SC:R 实测：5 张 2600px 主题背景 + 8 张 gallery 截图全部可用）
- 一手官方图特征：文件名带官方语义（terran/zerg/protoss_background）、
  分辨率是整齐的设计档位（1600/2560/2600/3840），不是转传的随机尺寸
- 官网 CDN 批量下载照样要 montage + vision 目检一遍再进候选清单：剔掉
  _mobile 小图变体、纯 UI 截图、重复资源——来源官方不等于每张都适合做壁纸

### 二级来源：wallhaven.cc（官网拿不到时的 fallback）

- API 免费无 key：`q=<ip名>&categories=100&purity=100&sorting=favorites&atleast=2560x1440`
  按收藏数排序拉 3 页；社区收藏榜头部基本是该 IP 官方原画的高清传播版
- **必须逐张 vision 目检**：搜索结果混有大量动漫 crossover、其他游戏
  （Halo 光环风）、纯 logo、真人 cos——标签不可信，一例：
  "starcraft" 搜索里混进了金发少女骑兽图和多族跨界大乱斗图

### 通用规则

- 同一主题的壁纸来源要纯：一手官网图与转传图混排，清晰度落差会被整体质疑
- 裁切规整：`magick in.jpg -resize 3840x3840 -gravity center -crop 16:9 +repage -quality 90 out.jpg`
- 素材许可：README 标注 "Artwork © <厂商> — unofficial fan-theme
  distribution"（wukong 主题先例）；代码部分 MIT 不变
- AI 生图路线的硬伤（实测）：pollinations 免费档锁死 1024×576（所有
  width/height/model 参数被钳制），插值放大必糊——被用户"质量太差"否决，
  勿再走

## 主题 repo 的坑（都会咬人）

- **`omarchy-refresh-shell` 会把 bar.layout 重置为出厂默认**——所有第三方
  widget 位置全丢，且锁屏状态下它拒绝重启 shell。恢复：找最新的
  `shell.json.bak.<epoch>`（插件 enable/install 时自动生成），cp 回去后
  再 `omarchy plugin enable <id>` 补位置。**不要用 refresh-shell 来"应用"
  插件**——enable 本身已热加载
- **`git reset --hard origin/main` 不删 untracked 文件**：themes 目录里
  上一版的旧图若不在 git 索引里，reset 后依然残留——换壁纸集时用
  rsync --delete 或手动 rm，别只 reset
- 壁纸快照机制：`omarchy theme bg next` 只读
  `~/.local/state/omarchy/current/theme/backgrounds/` + 用户层
  `~/.config/omarchy/backgrounds/<name>/`，从不读 `themes/<name>/backgrounds/`。
  推新壁纸后要么 cp 到两处，要么重跑 `omarchy theme set <name>` 重建快照；
  壁纸选择器/切换 UI 读的也是快照+用户层——快照不重建时，用户在选择器里
  看到的依旧是旧图集
- 锁屏状态下 `omarchy theme set` / shell 重启被拒——改完配置必须
  `omarchy-theme-bg-set <壁纸绝对路径>` 手动推送显示层，否则桌面仍显示
  旧图（state 链接已更新但显示进程没刷新）
- agent 会话里 `grim` 截屏在 Omarchy 4.x 上直接挂死/超时（加 XDG_RUNTIME_DIR、加 -o 指定 monitor 都救不了），不要再用它做壁纸/主题验证——改用命令回读（`omarchy theme bg current` / `bg next` 走一整圈逐张回读）+ 让用户肉眼确认；「还是旧图」的反馈先查快照是否重建
- **"改完了"的完整验证链（少一步就会被"怎么还是旧图"打回）**：
  ① 壁纸文件进 themes/<name>/backgrounds/ → ② 重跑 `omarchy theme set <name>`
  重建快照 → ③ `readlink ~/.local/state/omarchy/current/background` 且目标
  文件**存在**（symlink 指向已删文件不报错，桌面永远停在旧图）→ ④ grim
  截屏亲眼看新图上屏。配置层全部正确但显示层没刷新 = 对用户来说就是没改
- **backgrounds 每次变更必须连带重做 preview.png 和 README 壁纸清单**——
  用户会逐项查 repo（"preview 还是老的"）。拼图一条流：
  `magick montage backgrounds/*.jpg -tile 3x3 -geometry 600x338+4+4 -background '#05070e' /tmp/p.png && magick /tmp/p.png -resize 1800x preview.png`
- **README 改版整文件重写**：用 str.replace 反复替换单节会留下重复的
  Icons/License 段和过时表述；重写后 `grep -c '^## '` 核对章节数
- **构建脚本不进主题 repo**：fetch_*/gen_*/sync_*/pool_* 等过程脚本和制作
  笔记留在 build 工作目录；发布物只有主题本体（red-line 清单 + colors.toml +
  preview/unlock + backgrounds/ + README/LICENSE）。发布前 `git ls-files` 过一遍
- **发布 repo 与本机已装主题是两份独立拷贝，已装目录（themes/<name>）没有
  .git**——commit/push 一律在 build 工作目录做，再同步到已装目录；在已装
  目录里跑 git 命令只会得到幽灵状态。同步用 rsync --delete（cp 会残留上一
  版已删的图）

## v6 定稿的审美结论（StarCraft 主题）

用户两轮反馈沉淀的偏好：**深色背景 + 单主体特写 + 冷色调**；排斥明亮
大乱战群像、高饱和彩色爆发。玩家对此类主题的验收标准是"是不是官方
Remastered 那种感觉"——AI 风格致敬图即使构图好也会因"不是官方原画"
被否。官方图单张文件 1-3MB（细节密度）是正常水位，400KB 的插值放大图
会被一眼识破。

定稿流程规则：**终选交用户**——把候选做成编号清单，让用户报编号增删
（官方同源图也会因风格不合被整批剔除），不替用户做审美终判。

用户用位置词点名删图（「后面四张」「前几张」）时，不要自己映射到文件名——
立即把当前集合排成编号清单发出去，让用户报编号；位置词到文件名的映射猜错
会差点删掉要保留的图。执行删除后必须 `ls | wc -l` 核对数量真的下降：
`rm -f` 对拼错的文件名静默成功，「已删」的回报可能是假象。
