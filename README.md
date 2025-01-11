2.0 Flash Experimental。有时可能无法按预期运作。
你需要使用 Kivy 框架开发一个 Android 应用程序（并打包成 APK）。该应用包含两个主要功能：首页内容展示和检查更新。

1. 首页 (Home Screen)

布局 (Layout)

底部导航栏 (Bottom Navigation): 包含两个并排的按钮：
左侧按钮：文本“首页”，点击显示首页内容（若已显示则不刷新）。
右侧按钮：文本“检查更新”，点击切换到更新界面 (Update Screen)。
内容区域 (Content Area): 位于底部导航栏上方，用于动态显示内容。初始状态为空。
API 数据源选择器 (API Data Source Selector): 位于内容区域上方，使用下拉选择框（Spinner）实现。
数据获取与展示 (Data Fetching and Display)

初始加载 (Initial Load):
应用启动后，立即请求默认 API：https://slapibf.com/api.php/provide/vod/?ac=list。
该 API 返回 JSON 列表。解析 JSON 中的 "class" 数组，提取每个对象的 "type_name" 字段，用于填充下拉选择框。
处理请求或解析失败的情况，显示错误信息。
下拉选择框交互 (Spinner Interaction):
用户选择下拉选择框中的选项后，获取该选项对应的 "type_id"。
使用 "type_id" 构造新的 API 请求：https://slapibf.com/api.php/provide/vod/?ac=detail&t=<type_id>&pg=1。
该 API 返回包含图片和视频信息的 JSON 列表。解析 JSON 中的 "list" 数组。
提取每个对象的 "vod_pic" (图片 URL) 和 "vod_play_url" (视频 URL)。
将图片以两列网格布局 (GridLayout) 显示在内容区域，铺满屏幕宽度。
处理请求或解析失败的情况，显示错误信息。
图片显示 (Image Display):
使用异步加载方式 (AsyncImage) 加载图片，设置 allow_stretch=True 和 keep_ratio=True 以适应屏幕宽度。
点击图片后，在新界面（Video Screen）中使用视频播放器播放对应视频。
分页加载/无限滚动 (Pagination/Infinite Scrolling):
当用户滚动到图片列表底部时，自动加载下一页数据。
通过递增 pg 参数（例如 pg=2、pg=3 等）请求 API 的下一页。
将新加载的图片添加到网格布局中。
图片和视频处理 (Image and Video Handling)

视频播放 (Video Playback):
点击图片后，切换到新的 Screen (Video Screen)。
在新线程中播放视频，防止阻塞主线程。
支持播放 m3u8 和 flv 格式的视频。（需要考虑 Android 平台对视频格式的支持以及可能的第三方库，例如 ExoPlayer）。
2. 检查更新 (Update Screen)

布局 (Layout):
一个 Label，显示当前版本号（例如 "当前版本：1.0.0"）。
一个超链接 (Hyperlink)，指向更新日志或下载页面。点击超链接应使用系统默认浏览器打开链接。
技术要求 (Technical Requirements)

使用 Kivy 框架。
图片异步加载。
视频在新线程中播放，支持 m3u8 和 flv 格式（需要考虑平台兼容性和第三方库）。
实现无限滚动/加载更多功能。
代码结构清晰、易于维护，使用 KV 语言进行界面布局。
错误处理：在 API 请求和 JSON 解析过程中添加错误处理机制。
Android 权限：需要申请 INTERNET、READ_EXTERNAL_STORAGE 和 WRITE_EXTERNAL_STORAGE 权限。
