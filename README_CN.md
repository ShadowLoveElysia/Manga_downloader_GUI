# 漫画下载器

<p align="right">
  <a href="README.md"><span style="color:blue">English</span></a> |
  <a href="README_CN.md">中文</a> |
  <a href="README_JP.md"><span style="color:blue">日本語</span></a>
</p>

## BW下载的新方法！

# 新版本
## v0.3.3（推荐更新）
- 更新到Chromium 112.0.5590.0
- 更好地支持BW书籍页码模式，支持小说。

在[发布页面](https://github.com/xuzhengyi1995/Manga_downloader/releases/tag/BW-downloader-chrome-v0.3.3)下载，或者直接下载：[Windows x64 发布构建 v0.3.3](https://github.com/xuzhengyi1995/Manga_downloader/releases/download/BW-downloader-chrome-v0.3.3/BW-downloader-chrome-v0.3.3.7z)

## GUI使用指南

本项目现已提供图形用户界面，大大简化了使用流程，强烈推荐使用GUI界面！

### 启动GUI

```bash
python app.py
```

### GUI功能

GUI界面包含多个标签页：

1. **下载设置**: 配置漫画下载参数
2. **控制台输出**: 查看下载过程的详细输出
3. **图片转PDF**: 将下载的图片合并成PDF文件

### 多语言支持

GUI支持多种语言：
- 中文
- 英文
- 日语

可以通过顶部菜单栏"语言"选项切换界面语言。

### Chrome设置

在菜单栏选择"文件 -> 设置"，可以配置：
- 项目根目录
- Chrome浏览器路径
- ChromeDriver路径

确保设置中的Chrome版本和ChromeDriver版本相匹配，否则可能导致下载失败。

---

## v0.3.2
此版本对BW有以下优良功能：
- 可以下载封面（如果封面图像是jpeg格式，请在分享前检查或最好转换为png，因为jpeg文件会包含您的BW账户信息）。
- 可以使用页码自动命名图像，您可以从任何您想要的页面开始，向前或向后移动！
- 可以使用BW uuid命名文件夹，而不再是随机命名。
- 不再跳过空白或重复页面，不再使用图像哈希检查重复页面，性能更好。

示例截图：
![1670681578(1)](https://user-images.githubusercontent.com/29002064/206859972-0c775ee2-02fd-4d62-8870-4cd262fc6116.jpg)

如果您发现在下载某些漫画时文件名都变成了"cover_or_extra_xxx"，请提交bug，BW可能有比我所见到的更多的URL模式，或者他们更改了模式，应该覆盖这些情况以使页码正常工作。

在[发布页面](https://github.com/xuzhengyi1995/Manga_downloader/releases/tag/BW-downloader-chrome-v0.3.2)下载，或者直接下载：[Windows x64 发布构建 v0.3.2](https://github.com/xuzhengyi1995/Manga_downloader/releases/download/BW-downloader-chrome-v0.3.2/BW-downloader-chrome-v0.3.2.7z)

## v0.3.1
此版本改进了保存快照的性能，如果您在下载过程中遇到浏览器变得非常慢的问题，请尝试新版本。

在[发布页面](https://github.com/xuzhengyi1995/Manga_downloader/releases/tag/BW-downloader-chrome-v0.3.1)下载，或者直接下载：[Windows x64 发布构建 v0.3.1](https://github.com/xuzhengyi1995/Manga_downloader/releases/download/BW-downloader-chrome-v0.3.1/BW-downloader-chrome-v0.3.1.7z)

## v0.3
修复了一些宽度小于800px的漫画无法下载的问题，请参见[#113](/../../issues/113)。

在[发布页面](https://github.com/xuzhengyi1995/Manga_downloader/releases/tag/BW-downloader-chrome-v0.3)下载，或者直接下载：[Windows x64 发布构建 v0.3](https://github.com/xuzhengyi1995/Manga_downloader/releases/download/BW-downloader-chrome-v0.3/BW-downloader-chrome-v0.3.7z)

## v0.2.1
将Chromium升级到109.0.5393，可能会修复一些问题。

在[发布页面](https://github.com/xuzhengyi1995/Manga_downloader/releases/tag/BW-downloader-chrome-v0.2.1)下载，或者直接下载：[Windows x64 发布构建 v0.2.1](https://github.com/xuzhengyi1995/Manga_downloader/releases/download/BW-downloader-chrome-v0.2.1/BW-downloader-chrome-v0.2.1.7z)

## v0.2
这个版本基于Chromium 106.0.5243.0，变更如下：
- 支持`https://ebook.tongli.com.tw`，下载的图像将保存在`C:\bw_export_data\TONGLI_URL_STRING`
- 支持`https://www.dlsite.com`，但这是保存缓存图像，所以最后3~4页应该按如下方式下载（例如我们有10页）：
  - 浏览第1页到第10页（确保当前页面完全加载后再进入下一页）。
  - 您会发现在第10页，可能只有第1-7页的图像。
  - 从第10页返回到第5页，您会发现最后的页面已保存。（但可能顺序相反）
  - 目前我们无法做得比这更好。
 - 可用于`https://book.dmm.com`，使用以下脚本移动页面：
 ```js
   window.i=0;setInterval(()=>{NFBR.a6G.Initializer.views_.menu.options.a6l.moveToPage(window.i);console.log(window.i);window.i++;},3000)
 ```
 上面的脚本适用于**DMM**，对于**BW**请使用以下脚本：
 ```js
   window.i=0;setInterval(()=>{NFBR.a6G.Initializer.L7v.menu.options.a6l.moveToPage(window.i);console.log(window.i);window.i++;},3000)
 ```
 - 对BW可能略快，并可能下载一些宽度>高度的图像。

在[发布页面](https://github.com/xuzhengyi1995/Manga_downloader/releases/tag/BW-downloader-chrome-v0.2)下载，或者直接下载：[Windows x64 发布构建 v0.2](https://github.com/xuzhengyi1995/Manga_downloader/releases/download/BW-downloader-chrome-v0.2/BW-downloader-chrome-v0.2.7z)

使用方法（与旧版本相同）：
1.  解压缩文件`BW-downloader-chrome-bin.zip`。
2.  打开`powsershell`或`cmd`，`cd`到解压缩的浏览器目录。
3.  使用命令行`.\chrome.exe --user-data-dir=c:\bw-downloader-profile --no-sandbox`打开浏览器。
4.  浏览漫画，漫画将保存到`C:\bw_export_data`

**不要将其用于其他网站，仅将其作为漫画下载器使用，它不如普通chrome浏览器安全！**

# 旧版本
在[发布页面](https://github.com/xuzhengyi1995/Manga_downloader/releases/tag/BW-downloader-chrome-v0.1)下载，或者直接下载：[Windows x64 发布构建 v0.1](https://github.com/xuzhengyi1995/Manga_downloader/releases/download/BW-downloader-chrome-v0.1/BW-downloader-chrome-v0.1.7z)

**如果您正在寻找下载BW的方法，请尝试这种方法，这真的是个值得尝试的好方法，您会喜欢的！**

**对于coma，请参见下文。**

现在有一种新方法，使用自定义的`chromium`浏览器，它可以非常轻松地以原始大小下载BW原始图像。它可以下载漫画和小说，并且可能用于每个使用canvas渲染页面的网站（现在只在BW上测试过）。

这只是一个开发版本，可能有bug并可能崩溃，但您现在可以下载自定义浏览器并尝试。

**不要将其用于其他网站，仅将其作为BW下载器使用，它不如普通chrome浏览器安全！**

克隆这个仓库或只下载[BW-downloader-chrome-bin.zip](https://github.com/xuzhengyi1995/Manga_downloader/raw/master/BW-downloader-chrome-bin.zip)

1.  解压缩文件`BW-downloader-chrome-bin.zip`。
2.  打开`powsershell`或`cmd`，`cd`到解压缩的浏览器目录。
3.  使用命令行`.\chrome.exe --user-data-dir=c:\bw-downloader-profile --no-sandbox`打开浏览器。
4.  调整浏览器窗口大小，使其变小并且只能显示一个漫画页面，如下例所示
    ![image](https://user-images.githubusercontent.com/29002064/139255318-95531cd9-c442-4a61-acb4-cef3d71b7190.png)


5.  现在您可以访问BW网站，登录并打开您想要下载的漫画，记得在打开前重置漫画的阅读状态。
6.  按`F12`，使其成为单独的窗口（见下图），然后运行以下脚本（只需进入`console`，复制粘贴代码，按回车）以自动移动页面，如果您的网络良好，可以将`3000`改为较小的数字，3000意味着3000ms -> 3s，每3s它将移到下一页。

    您也可以手动点击鼠标左键/使用键盘箭头键/使用键盘模拟软件来移动页面，您可以选择您喜欢的方式，只要确保页面在移动。
    ```js
    window.i=0;setInterval(()=>{NFBR.a6G.Initializer.L7v.menu.options.a6l.moveToPage(window.i);console.log(window.i);window.i++;},3000)
    ```
    
    如果这不起作用并显示'Uncaught TypeError: Cannot read properties of undefined (reading 'menu') at <anonymous>:1:54'，这意味着BW已更新js，您可以尝试在控制台中找到它，只需尝试`NFBR.a6G.Initializer.*.menu`不是`undefined`，*是新对象名称；或者您可以直接提交bug。

    ![image](https://user-images.githubusercontent.com/29002064/138590508-e7555a2d-1528-4e59-8a50-e08e407bc1be.png)


7.  现在您可以检查您的`C:\bw_export_data`，您可以找到一个随机uuid文件夹，其中包含所有漫画图像。
    ![image](https://user-images.githubusercontent.com/29002064/139255390-03b9191a-e90b-4572-9cde-b7e50ca9787c.png)

如果您想同时下载多个漫画，只需打开任意多个漫画，并执行步骤5到6。

这种方法非常易于使用，稳定，并且不需要找任何分辨率或cookie，并且它可以下载没有条形码的真正原始图像。

可能将来会为其添加新的浏览器UI，并可以点击下载。

现在可能无法下载封面页。

仅在Windows上构建，现在没有其他平台的程序。

如果您发现一些问题，请提交bug，谢谢！

# Manga_Downloader

一个使用`selenium`的漫画下载框架。

**现在支持以下网站：**

1.  [Bookwalker.jp](https://bookwalker.jp)
2.  [Bookwalker.com.tw](https://www.bookwalker.com.tw)
3.  [Cmoa.jp](https://www.cmoa.jp/)

**程序将自动检查给定URL的网站**

**如果您给出的网站不受支持，程序将引发错误。**

**现在支持仅登录一次的多漫画下载**

**现在支持批量下载**

**您应该准备以下信息：**

1.  漫画URL
2.  Cookies
3.  图像目录（放置图像的文件夹名称）
4.  某些网站您应该查看图像的大小并在`res`设置。[Cmoa.jp](https://www.cmoa.jp/)不需要这个。

# 如何使用

## 所有设置

所有设置都在`main.py`中。

```python
settings = {
    # 漫画URL，应该是相同的网站
    'manga_url': [
        'URL_1',
        'URL_2'
    ],
    # 您的cookies
    'cookies': 'YOUR_COOKIES_HERE',
    # 存储漫画的文件夹名称，与manga_url顺序相同
    'imgdir': [
        'IMGDIR_FOR_URL_1',
        'IMGDIR_FOR_URL_2'
    ],
    # 分辨率，（宽度，高度），对于cmoa.jp这无关紧要。
    'res': (1393, 2048),
    # 每页的睡眠时间（秒），通常无需更改。
    'sleep_time': 2,
    # 页面加载等待时间（秒），如果您的网络良好，可以减少此参数。
    'loading_wait_time': 20,
    # 剪切图像，（左，上，右，下）以像素为单位，None表示不剪切图像。这通常用于剪切边缘。
    # 像(0, 0, 0, 3)表示从图像底部剪切3像素。
    'cut_image': None,
    # 文件名前缀，如果您希望文件名像'klk_v1_001.jpg'，在这里写'klk_v1'。
    'file_name_prefix': '',
    # 文件名位数计数，如果您希望文件名像'001.jpg'，在这里写3。
    'number_of_digits': 3,
    # 开始页面，如果您想从第3页开始下载，将其设置为3，None表示从0开始
    'start_page': None,
    # 结束页面，如果您想下载到第10页，将其设置为10，None表示直到结束
    'end_page': None,
}
```

## 安装环境和如何获取URL/Cookies

**此程序现在适用于Chrome，如果您使用其他浏览器，请查看[此页面](https://selenium-python.readthedocs.io/installation.html)**

0.  安装Python包_selenium_和_pillow_并获取_Google Chrome驱动程序_。

    1.  对于_selenium_和_pillow_：

    ```shell
    pip install selenium
    pip install Pillow
    # 这个undetected_chromedriver是为了防止被BW检测到
    pip install undetected_chromedriver
    ```

    2.  对于Google Chrome驱动程序：

        1.  请检查您的Chrome版本，'帮助'->'关于Google Chrome'。

        2.  在[这里](https://sites.google.com/a/chromium.org/chromedriver/downloads)下载适合您Chrome版本的Chrome驱动程序。

        3.  将其放入任何文件夹并将该文件夹添加到PATH中。

    3.  有关更多信息，我建议您在[这里](https://selenium-python.readthedocs.io/installation.html)查看


1.  更改main.py中的`IMGDIR`以指示放置漫画的位置。

2.  在程序中添加您的cookies。

    **记得使用F12查看cookies！**

    **因为一些http only cookies无法通过javascript看到！**

    **记得访问以下链接获取cookies！**

    1.  对于[Bookwalker.jp]的cookies，请前往[这里](https://member.bookwalker.jp/app/03/my/profile)。
    2.  对于[Bookwalker.com.tw]的cookies，请前往[这里](https://www.bookwalker.com.tw/member)。
    3.  对于[www.cmoa.jp]的cookies，请前往[这里](https://www.cmoa.jp/)，并且您**必须**通过插件[EditThisCookie](http://www.editthiscookie.com/)获取cookies，在[这里](https://chrome.google.com/webstore/detail/edit-this-cookie/fngmhnnpilhplaeedifhccceomclgfbg)为chrome下载。

    -   对于`EditThisCookie`，这可以用于上述任何网站，但对于`cmoa`，您**必须**使用此方法

        1.  转到`EditThisCookie`的用户首选项(chrome-extension://fngmhnnpilhplaeedifhccceomclgfbg/options_pages/user_preferences.html)
        2.  将cookie导出格式设置为`Semicolon separated name=value pairs`
        3.  转到[cmoa](https://www.cmoa.jp/)，点击`EditThisCookie`，然后点击`导出`按钮
        4.  将文件中的cookies(**在`// Example: http://www.tutorialspoint.com/javascript/javascript_cookies.htm`之后**)复制到程序中

    -   对于传统方式

        > 1.  打开页面。
        > 2.  按F12。
        > 3.  点击_网络_。
        > 4.  刷新页面。
        > 5.  找到第一个_profile_请求，点击它。
        > 6.  在右侧，会有一个_请求头_，转到那里。
        > 7.  找到_cookie:...._，复制_cookie:_后面的字符串，粘贴到_main.py_，_YOUR_COOKIES_HERE_

3.  更改_main.py_中的_manga_url_。

    1.  对于[Bookwalker.jp]

        首先转到[購入済み書籍一覧](https://bookwalker.jp/holdBooks/)，您可以在这里找到所有您的漫画。

        这次URL是您漫画的**'この本を読む'**按钮的URL。

        右键点击此按钮，然后点击**'复制链接地址'**。

        URL以**member.bookwalker.jp**开头，而不是**viewer.bookwalker.jp**。这里我们使用漫画[【期間限定　無料お試し版】あつまれ！ふしぎ研究部　１](https://member.bookwalker.jp/app/03/webstore/cooperation?r=BROWSER_VIEWER/640c0ddd-896c-4881-945f-ad5ce9a070a6/https%3A%2F%2Fbookwalker.jp%2FholdBooks%2F)。

        这是**あつまれ！ふしぎ研究部　１**的URL：<https://member.bookwalker.jp/app/03/webstore/cooperation?r=BROWSER_VIEWER/640c0ddd-896c-4881-945f-ad5ce9a070a6/https%3A%2F%2Fbookwalker.jp%2FholdBooks%2F>

    2.  对于[Bookwalker.com.tw]

        请前往[线上阅读](https://www.bookwalker.com.tw/member/available_book_list)。

        漫画URL如下所示：<https://www.bookwalker.com.tw/browserViewer/56994/read>

    3.  对于[Cmoa.jp]

        打开漫画并复制浏览器上的URL。

        漫画URL如下所示：<https://www.cmoa.jp/bib/speedreader/speed.html?cid=0000156072_jp_0001&u0=0&u1=0&rurl=https%3A%2F%2Fwww.cmoa.jp%2Fmypage%2Fmypage_top%2F%3Ftitle%3D156072>

    只需将此URL复制到_main.py_中的`MANGA_URL`。

4.  编辑程序后，运行`python main.py`来运行它。

# 注意事项

1.  默认情况下，`SLEEP_TIME`是2秒，您可以根据自己的网络情况调整它，如果下载有重复的图像，您可以将其更改为5或更多。如果您认为太慢，尝试将其更改为1甚至0.5。

2.  `LOADING_WAIT_TIME = 20`，这是等待漫画查看器页面加载的时间，如果您的网络不好，您可以将其设置为30或50秒。

3.  分辨率，您可以根据需要更改它，但首先检查原始图像分辨率。

    ```python
    RES = (784, 1200)
    ```

    如果原始图像有更高的分辨率，您可以像这样更改它（分辨率只是一个例子）。

    ```python
    RES = (1568, 2400)
    ```

    **对于[Cmoa.jp]不需要这个，分辨率由[Cmoa.jp]固定。**

4.  有时我们应该注销并登录，这个网站非常严格，并采取了很多方法来防止滥用。

5.  现在您可以通过将`CUT_IMAGE`设置为（左，上，右，下）来剪切图像。

    例如，您想从图像底部剪切3px，您可以将其设置为：

    ```python
    CUT_IMAGE = (0, 0, 0, 3)
    ```

    此功能使用`Pillow`，如果您想使用它，您应该使用以下命令安装它：

    ```shell
    pip install Pillow
    ```

    默认情况下，它是`None`，表示不剪切图像。

6.  您现在可以通过更改`file_name_prefix`和`number_of_digits`来更改文件名前缀和位数。

    例如，如果您正在下载杀戮天使漫画第1卷，并且您希望文件名像：

    <pre>
        KLK_V1
        │--KLK_V1_001.jpg
        │--KLK_V1_002.jpg
        │--KLK_V1_003.jpg
    </pre>

    那么您可以像下面这样设置参数：

    ```python
    settings = {
        ...,
        'file_name_prefix': 'KLK_V1',
        # 文件名位数计数，如果您希望文件名像'001.jpg'，在这里写3。
        'number_of_digits': 3
    }
    ```

# 开发

0.  概念

    要下载漫画，通常我们这样做：

    <pre>
    +------------+     +-----------+      +------------+      +-------------------+      +--------------+
    |            |     |           |      |            |      |                   | OVER |              |
    |   登录     +-----+ 加载页面  +----->+ 保存图像   +----->+ 移动到下一页      +----->+   完成       |
    |            |     |           |      |            |      |                   |      |              |
    +------------+     +-----------+      +-----+------+      +---------+---------+      +--------------+
                                                ^                       |
                                                |                       |
                                                |      更多页面         |
                                                +-----------------------+
    </pre>

    所以我们可以创建一个框架来重用代码，对于新网站，通常我们只需要编写一些方法。

1.  文件结构

    <pre>
    |--main.py
    │--downloader.py
    │--README.MD
    └─website_actions
        │--abstract_website_actions.py
        │--bookwalker_jp_actions.py
        │--bookwalker_tw_actions.py
        │--cmoa_jp_actions.py
        │--__init__.py
    </pre>

2.  抽象`WebsiteActions`类的介绍。

    对于每个网站，类应该有以下方法/属性，这里我们以bookwalker.jp为例：

    ```python
    class BookwalkerJP(WebsiteActions):
        '''
        bookwalker.jp
        '''

        # login_url是我们首先加载并放置cookies的页面。
        login_url = 'https://member.bookwalker.jp/app/03/login'

        @staticmethod
        def check_url(manga_url):
            '''
            此方法返回一个布尔值，检查给定的漫画url是否属于这个类。
            '''
            return manga_url.find('bookwalker.jp') != -1

        def get_sum_page_count(self, driver):
            '''
            此方法返回一个整数，获取总页数。
            '''
            return int(str(driver.find_element_by_id('pageSliderCounter').text).split('/')[1])

        def move_to_page(self, driver, page):
            '''
            此方法不返回任何内容，移动到给定的页码。
            '''
            driver.execute_script(
                'NFBR.a6G.Initializer.B0U.menu.a6l.moveToPage(%d)' % page)

        def wait_loading(self, driver):
            '''
            此方法不返回任何内容，等待漫画加载。
            '''
            WebDriverWait(driver, 30).until_not(lambda x: self.check_is_loading(
                x.find_elements_by_css_selector(".loading")))

        def get_imgdata(self, driver, now_page):
            '''
            此方法返回String/可以写入文件或转换为BytesIO的内容，获取图像数据。
            '''
            canvas = driver.find_element_by_css_selector(".currentScreen canvas")
            img_base64 = driver.execute_script(
                "return arguments[0].toDataURL('image/jpeg').substring(22);", canvas)
            return base64.b64decode(img_base64)

        def get_now_page(self, driver):
            '''
            此方法返回一个整数，当前页面上的页码
            '''
            return int(str(driver.find_element_by_id('pageSliderCounter').text).split('/')[0])
    ```

      我们还有一个`before_download`方法，这个方法在我们开始下载之前运行，因为有些网站需要在我们开始下载之前关闭一些弹出组件。

    ```python
    def before_download(self, driver):
        '''
        此方法不返回任何内容，在下载前运行。
        '''
        driver.execute_script('parent.closeTips()')
    