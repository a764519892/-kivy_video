请使用 Kivy 框架开发一个 Android 应用程序（并打包成 APK）。该应用程序包含两个主要功能：首页内容展示和检查更新。使用 KV 语言进行界面布局。

**1. 首页 (Home Screen)**

*   **布局 (Layout)：**
    *   **底部导航栏 (Bottom Navigation):** 使用 `BoxLayout` 水平排列两个 `Button`：
        *   左侧按钮：`id: home_button`, `text: '首页'`，点击显示首页内容（若已显示则不刷新）。
        *   右侧按钮：`id: update_button`, `text: '检查更新'`，点击切换到更新界面 (Update Screen)。
    *   **内容区域 (Content Area):** 位于底部导航栏上方，使用 `ScrollView` 包含一个 `GridLayout`，用于动态显示图片。初始状态为空。
    *   **API 数据源选择器 (API Data Source Selector):** 位于内容区域上方，使用两个并排的 `Spinner`：
        *   左侧 `Spinner` (`id: api_source_spinner`)：用于选择 API 源。
        *   右侧 `Spinner` (`id: api_data_spinner`)：根据左侧 `Spinner` 的选择动态加载数据。

*   **数据获取与展示 (Data Fetching and Display)：**
    *   **初始加载 (Initial Load):** 应用启动后，立即请求默认 API：`https://slapibf.com/api.php/provide/vod/?ac=list`。
        *   处理 API 请求失败或未获取到 JSON 的情况，尝试备用 API（请提供至少一个备用 API 地址）。
        *   JSON 格式：`[{"type_id": "数据源ID", "type_name": "数据源名称", "api_url": "该数据源对应的API地址"}, ...]`。
        *   解析 JSON 中的 "class" 数组（如果存在），提取每个对象的 "type_name" 和 "type_id" 字段，用于填充左侧 `api_source_spinner`。使用 "api_url" 字段存储在spinner的values里面。
        *   处理 JSON 解析失败的情况，显示错误信息（例如使用 `Label` 显示）。
    *   **下拉选择框交互 (Spinner Interaction):**
        *   左侧 `api_source_spinner` 选择改变时：
            *   获取选定项的 “type_id” 和 “api_url”。
            *   使用 “type_id” 和 “api_url” 构造新的 API 请求：例如 `api_url?ac=detail&t=<type_id>&pg=1`。
            *   JSON 格式：`{"list": [{"vod_pic": "图片URL", "vod_play_url": "视频URL"}, ...], "page_count": "总页数"}`。
            *   解析 JSON 中的 "list" 数组。提取每个对象的 "vod_pic" (图片 URL) 和 "vod_play_url" (视频 URL)。
            *   清空 `GridLayout` 中的现有图片。
            *   使用 `AsyncImage` 将图片以两列的 `GridLayout` 显示在内容区域，设置 `allow_stretch=True` 和 `keep_ratio=True` 以适应屏幕宽度。`GridLayout` 的 `cols` 属性设置为 2。
            *   处理 API 请求或 JSON 解析失败的情况，显示错误信息。
        *   右侧 `api_data_spinner` 根据左侧 `api_source_spinner` 的选择动态加载数据，并显示在界面上。
    *   **分页加载/无限滚动 (Pagination/Infinite Scrolling):**
        *   监听 `ScrollView` 的滚动事件。当用户滚动到接近底部时，自动加载下一页数据。
        *   使用 `pg` 参数请求 API 的下一页 (例如 `pg=2`、`pg=3` 等)。使用从api返回的page_count判断是否还有下一页。
        *   将新加载的图片添加到 `GridLayout` 中。

*   **图片和视频处理 (Image and Video Handling)：**
    *   **图片显示 (Image Display):** 使用 `AsyncImage` 异步加载图片。
    *   **视频播放 (Video Playback):** 点击图片后，切换到新的 `Screen` (Video Screen)。在新线程中使用视频播放器播放对应视频。视频地址从图片列表 JSON 中的 `vod_play_url` 字段获取。支持播放 m3u8 和 flv 格式的视频。推荐使用 `ffpyplayer` 或 `Pyjnius` 访问 Android 的 `MediaPlayer`。

**2. 检查更新 (Update Screen)**

*   **布局 (Layout):** 使用 `BoxLayout` 垂直排列：
    *   一个 `Label`，显示当前版本号（例如 "当前版本：1.0.0"）。版本号应从应用代码中动态获取。
    *   一个 `Hyperlink`（可以使用 `Label` 模拟），点击后使用系统默认浏览器打开指定的更新日志或下载页面 URL。

**技术要求 (Technical Requirements)**

*   使用 Kivy 框架。
*   使用 KV 语言进行界面布局。
*   图片异步加载 (`AsyncImage`)。
*   视频在新线程中播放，支持 m3u8 和 flv 格式（使用 `ffpyplayer` 或 `Pyjnius`）。
*   实现无限滚动/加载更多功能。
*   代码结构清晰、易于维护。
*   错误处理：在 API 请求和 JSON 解析过程中添加完善的错误处理机制，使用 `try-except` 语句块。
*   Android 权限：需要在 `buildozer.spec` 文件中添加 `INTERNET`、`READ_EXTERNAL_STORAGE` 和 `WRITE_EXTERNAL_STORAGE` 权限。
*   提供至少一个备用API地址。

**补充说明:**

请提供详细的 KV 代码和 Python 代码实现以上功能。请注意代码的可读性和注释。
