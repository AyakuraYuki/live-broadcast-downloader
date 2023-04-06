# ts_downloader

这是一个用来按 `m3u8` 文件提供的切片顺序下载切片文件的脚本，并不是用来按照 `m3u8` 链接自动合成视频文件的脚本。

这个脚本库利用了 Selenium 4 实现下载功能，主要是模拟浏览器访问下载来完成切片下载的任务。

目前默认提供了如下站点的支持：

- asobistage
- eplus
- NHK 音乐之声
- Zaiko

脚本支持自动下载 WebDriver 浏览器驱动二进制包，是利用了 `webdriver-manager` 工具实现的。

如果要使用这个脚本，下载本仓库，以 eplus 视频举例，在浏览器开发者工具拿到 eplus 视频流的 m3u8 地址后，打开 `dl_eplus.py`，在 `tasks` 数组按要求填写 `view_url` 和 `prefix`，然后直接运行 `__main__` 方法，等待下载完成即可。

如果要扩展其他站点，可以仿照 `dl_eplus.py` 自己实现一个新的脚本。
