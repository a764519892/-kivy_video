我需要使用 Kivy 库开发一个 Android 应用程序（打包成 APK）。应用程序包含两个主要功能：首页内容展示和检查更新。

**1. 首页：**

*   **布局：**
    *   底部有两个并排的按钮：
        *   左侧按钮：文字为“首页”，点击后显示首页内容。
        *   右侧按钮：文字为“检查更新”，点击后显示更新界面。
    *   首页内容区域：位于底部按钮的上方，用于动态显示内容。
    *   顶部有一个下拉选择框（Spinner），用于选择不同的API数据源。

*   **数据获取与展示：**
    *   初始状态：程序启动后，立即读取一个默认的API，该API返回一个JSON列表，用于填充下拉选择框。JSON 列表的格式为：`[{"name": "数据源1名称", "api_url": "数据源1的API地址"}, {"name": "数据源2名称", "api_url": "数据源2的API地址"}, ...]`。
    *   下拉选择框交互：
        *   用户选择下拉选择框中的一个选项后，程序使用该选项对应的 `api_url` 访问API，获取图片列表。
        *   图片列表的JSON格式为：`[{"image_url": "图片1地址", "video_url": "视频1地址"}, {"image_url": "图片2地址", "video_url": "视频2地址"}, ...]`。
        *   图片以两列网格布局（GridLayout）显示在首页内容区域，铺满屏幕宽度。
        *   实现无限滚动/加载更多：当用户滑动到图片列表底部时，程序自动访问API的下一页（如果API支持分页），并将新的图片添加到网格布局中。假设API分页使用 `page` 参数，例如 `api_url?page=2`。

*   **图片和视频处理：**
    *   图片加载：使用异步加载方式，避免阻塞主线程，提高用户体验。
    *   视频播放：点击图片后，在新界面（Screen）中使用视频播放器播放对应的视频。视频地址从图片列表JSON中的 `video_url` 字段获取。视频播放应在新线程中进行，防止阻塞主线程。支持播放 m3u8 和 flv 格式的视频。

**2. 检查更新：**

*   点击底部“检查更新”按钮后，切换到更新界面。
*   更新界面包含：
    *   一个 Label，显示当前版本号（例如 "当前版本：1.0.0"）。
    *   一个超链接（Hyperlink），指向更新日志或下载页面。

**技术要求：**

*   使用 Kivy 框架。
*   图片异步加载。
*   视频在新线程中播放，支持 m3u8 和 flv 格式。
*   实现无限滚动/加载更多功能。
*   代码结构清晰、易于维护。

请提供 Kivy 代码实现以上功能。
