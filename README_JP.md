# マンガダウンローダー

<p align="right">
  <a href="README.md">English</a> |
  <a href="README_CN.md"><span style="color:blue">中文</span></a> |
  <a href="README_JP.md">日本語</a>
</p>

## 新しいBWダウンロード方法!

# 新バージョン
## v0.3.3 (更新推奨)
- Chromium 112.0.5590.0にアップデート。
- BW書籍のページ番号パターンをより良くサポートし、小説にも対応。

[リリース](https://github.com/xuzhengyi1995/Manga_downloader/releases/tag/BW-downloader-chrome-v0.3.3)またはこちらからダウンロードしてください: [Windows x64 リリースビルド v0.3.3](https://github.com/xuzhengyi1995/Manga_downloader/releases/download/BW-downloader-chrome-v0.3.3/BW-downloader-chrome-v0.3.3.7z)

## GUI使用ガイド

このプロジェクトにはGUI（グラフィカルユーザーインターフェース）が付属しており、使用プロセスが大幅に簡素化されます。GUIの使用を強く推奨します！

### GUIの起動

```bash
python app.py
```

### GUI機能

GUIインターフェースには複数のタブが含まれています：

1.  **ダウンロード設定**: マンガダウンロードパラメータを設定します。
2.  **コンソール出力**: ダウンロードプロセスの詳細な出力を表示します。
3.  **画像からPDF**: ダウンロードした画像をPDFファイルに結合します。

### 多言語対応

GUIは多言語に対応しています：
- 中国語
- 英語
- 日本語

トップメニューバーの「Language」（言語）オプションからインターフェース言語を切り替えることができます。

### Chrome設定

メニューバーで「ファイル -> 設定」を選択して設定できます：
- プロジェクトルートディレクトリ
- Chromeブラウザのパス
- ChromeDriverのパス

設定のChromeバージョンとChromeDriverバージョンが一致していることを確認してください。そうでない場合、ダウンロードが失敗する可能性があります。

---

## v0.3.2
このバージョンには、BW向けの以下の優れた機能があります：
- カバー画像をダウンロードできるようになりました（カバー画像がjpeg形式の場合、BWアカウント情報が含まれる可能性があるため、共有する前に確認またはpngに変換することを推奨します）。
- ページ番号を使用して画像ファイルを自動的に命名できるようになりました。任意のページから開始して、前または後に進むことができます！
- ランダムな名前ではなく、BW uuidでフォルダ名を付けられるようになりました。
- 空白または重複するページがスキップされなくなりました。重複ページの確認に画像ハッシュを使用せず、パフォーマンスが向上しました。

スクリーンショット例：
![1670681578(1)](https://user-images.githubusercontent.com/29002064/206859972-0c775ee2-02fd-4d62-8870-4cd262fc6116.jpg)

特定のマンガをダウンロードする際に、ファイル名がすべて「cover_or_extra_xxx」になる場合、バグ報告をお願いします。BWには私が見たもの以上のURLパターンがあるか、パターンが変更された可能性があります。ページ番号が正しく機能するためには、これらのケースをカバーする必要があります。

[リリース](https://github.com/xuzhengyi1995/Manga_downloader/releases/tag/BW-downloader-chrome-v0.3.2)またはこちらからダウンロードしてください: [Windows x64 リリースビルド v0.3.2](https://github.com/xuzhengyi1995/Manga_downloader/releases/download/BW-downloader-chrome-v0.3.2/BW-downloader-chrome-v0.3.2.7z)

## v0.3.1
このバージョンでは、スナップショット保存のパフォーマンスが向上しました。ダウンロード中にブラウザの動作が非常に遅くなる問題がある場合は、新しいバージョンを試してください。

[リリース](https://github.com/xuzhengyi1995/Manga_downloader/releases/tag/BW-downloader-chrome-v0.3.1)またはこちらからダウンロードしてください: [Windows x64 リリースビルド v0.3.1](https://github.com/xuzhengyi1995/Manga_downloader/releases/download/BW-downloader-chrome-v0.3.1/BW-downloader-chrome-v0.3.1.7z)

## v0.3
幅が800px未満の一部のマンガがダウンロードできない問題を修正しました。詳細は[#113](/../../issues/113)を参照してください。

[リリース](https://github.com/xuzhengyi1995/Manga_downloader/releases/tag/BW-downloader-chrome-v0.3)またはこちらからダウンロードしてください: [Windows x64 リリースビルド v0.3](https://github.com/xuzhengyi1995/Manga_downloader/releases/download/BW-downloader-chrome-v0.3/BW-downloader-chrome-v0.3.7z)

## v0.2.1
Chromiumを109.0.5393に更新しました。いくつかの問題が修正される可能性があります。

[リリース](https://github.com/xuzhengyi1995/Manga_downloader/releases/tag/BW-downloader-chrome-v0.2.1)またはこちらからダウンロードしてください: [Windows x64 リリースビルド v0.2.1](https://github.com/xuzhengyi1995/Manga_downloader/releases/download/BW-downloader-chrome-v0.2.1/BW-downloader-chrome-v0.2.1.7z)

## v0.2
このバージョンはChromium 106.0.5243.0に基づいており、変更点は以下の通りです：
- `https://ebook.tongli.com.tw` に対応。ダウンロードした画像は`C:\bw_export_data\TONGLI_URL_STRING`に保存されます。
- `https://www.dlsite.com` に対応。ただし、これはキャッシュ画像を保存するため、最後の3〜4ページは以下のようにダウンロードする必要があります（例えば10ページの場合）：
  - 1ページから10ページまで進みます（次ページに進む前に、現在のページが完全にロードされていることを確認してください）。
  - 10ページ目で、おそらく1-7ページ分の画像しか見つからないことに気づくでしょう。
  - 10ページ目から5ページ目に戻ると、最後のページが保存されていることがわかります（ただし、逆順になる場合があります）。
  - 現在、これ以上良い方法はありません。
- `https://book.dmm.com` で動作します。ページ移動には以下のスクリプトを使用します：
 ```js
   window.i=0;setInterval(()=>{NFBR.a6G.Initializer.views_.menu.options.a6l.moveToPage(window.i);console.log(window.i);window.i++;},3000)
 ```
 上記のスクリプトは**DMM**用です。**BW**用には以下のスクリプトを使用してください：
 ```js
   window.i=0;setInterval(()=>{NFBR.a6G.Initializer.L7v.menu.options.a6l.moveToPage(window.i);console.log(window.i);window.i++;},3000)
 ```
- BWの場合、わずかに高速になる可能性があり、幅が高さより大きい画像もダウンロードされる可能性があります。

[リリース](https://github.com/xuzhengyi1995/Manga_downloader/releases/tag/BW-downloader-chrome-v0.2)またはこちらからダウンロードしてください: [Windows x64 リリースビルド v0.2](https://github.com/xuzhengyi1995/Manga_downloader/releases/download/BW-downloader-chrome-v0.2/BW-downloader-chrome-v0.2.7z)

使用方法（旧バージョンと同じ）：
1.  `BW-downloader-chrome-bin.zip` ファイルを解凍します。
2.  `powsershell` または `cmd` を開き、解凍したブラウザディレクトリに `cd` します。
3.  `.\chrome.exe --user-data-dir=c:\bw-downloader-profile --no-sandbox` というコマンドラインでブラウザを起動します。
4.  ブラウザウィンドウのサイズを調整し、マンガページが一つだけ表示されるように小さくします。例：
    ![image](https://user-images.githubusercontent.com/29002064/139255318-95531cd9-c442-4a61-acb4-cef3d71b7190.png)


5.  これでBWウェブサイトにアクセスし、ログインしてダウンロードしたいマンガを開くことができます。開く前にマンガの既読ステータスをリセットすることを忘れないでください。
6.  `F12` を押して別のウィンドウにし（下図参照）、以下のスクリプトを実行してページを自動的に移動します（`console` に移動してコードをコピー＆ペーストし、Enterを押すだけです）。ネットワークが良い場合、`3000` をより小さい数値に変更できます。3000は3000ms = 3秒を意味し、3秒ごとに次のページに移動します。

    マウスの左ボタンをクリックしたり、キーボードの矢印キーを使用したり、キーボードシミュレーションソフトウェアを使用したりしてページを手動で移動することもできます。好きな方法を選んでください。ページが移動することを確認してください。
    ```js
    window.i=0;setInterval(()=>{NFBR.a6G.Initializer.L7v.menu.options.a6l.moveToPage(window.i);console.log(window.i);window.i++;},3000)
    ```
    
    これが機能せず、「Uncaught TypeError: Cannot read properties of undefined (reading 'menu') at <anonymous>:1:54」と表示される場合、BWがjsを更新したことを意味します。コンソールで探してみてください。`NFBR.a6G.Initializer.*.menu` が `undefined` でなく、* が新しいオブジェクト名であることを確認してください。または、直接バグ報告してください。

    ![image](https://user-images.githubusercontent.com/29002064/138590508-e7555a2d-1528-4e59-8a50-e08e407bc1be.png)


7.  これで`C:\bw_export_data`を確認すると、ランダムなuuidのフォルダがあり、その中にすべてのマンガ画像が含まれていることがわかります。
    ![image](https://user-images.githubusercontent.com/29002064/139255390-03b9191a-e90b-4572-9cde-b7e50ca9787c.png)

同時に複数のマンガをダウンロードしたい場合は、必要なだけマンガを開き、ステップ5〜6を実行してください。

この方法は非常に使いやすく、安定しており、解像度やcookieを探す必要がなく、バーコードなしで本当のオリジナル画像をダウンロードできます。

将来的には、新しいブラウザUIを追加し、クリックでダウンロードできるようにするかもしれません。

現在、カバーページをダウンロードできない可能性があります。

Windowsのみでビルドされており、他のプラットフォーム向けのプログラムは現在ありません。

何か問題が見つかった場合は、バグ報告をお願いします。ありがとうございます！

# Manga_Downloader

`selenium` を使用したマンガダウンロードフレームワーク。

**現在、以下のウェブサイトに対応しています：**

1.  [Bookwalker.jp](https://bookwalker.jp)
2.  [Bookwalker.com.tw](https://www.bookwalker.com.tw)
3.  [Cmoa.jp](https://www.cmoa.jp/)

**プログラムは、指定されたURLのウェブサイトを自動的にチェックします**

**指定したウェブサイトがサポートされていない場合、プログラムはエラーを発生させます。**

**一度ログインするだけで複数のマンガをダウンロードできるようになりました**

**现在支持批量下载**

**以下の情報を用意する必要があります：**

1.  マンガURL
2.  Cookies
3.  画像ディレクトリ（画像を置く場所、フォルダ名）
4.  一部のウェブサイトでは、画像のサイズを確認し、`res`で設定する必要があります。[Cmoa.jp](https://www.cmoa.jp/)では不要です。

# 使用方法

## 全ての設定

全ての設定は`main.py`にあります。

```python
settings = {
    # マンガURL、同じウェブサイトである必要があります
    'manga_url': [
        'URL_1',
        'URL_2'
    ],
    # あなたのcookies
    'cookies': 'YOUR_COOKIES_HERE',
    # マンガを保存するフォルダ名、manga_urlと同じ順序
    'imgdir': [
        'IMGDIR_FOR_URL_1',
        'IMGDIR_FOR_URL_2'
    ],
    # 解像度、（幅、高さ）、cmoa.jpの場合は関係ありません。
    'res': (1393, 2048),
    # 各ページの睡眠時間（秒）、通常は変更不要です。
    'sleep_time': 2,
    # ページ読み込み待機時間（秒）、ネットワークが良い場合はこのパラメータを減らすことができます。
    'loading_wait_time': 20,
    # 画像の切り抜き、（左、上、右、下）ピクセル単位、Noneは画像を切り抜かないことを意味します。これはしばしば端を切り抜くために使用されます。
    # 例：(0, 0, 0, 3)は画像の下から3ピクセル切り抜くことを意味します。
    'cut_image': None,
    # ファイル名のプレフィックス。ファイル名を「klk_v1_001.jpg」のようにしたい場合、ここに「klk_v1」と記述します。
    'file_name_prefix': '',
    # ファイル名の桁数。ファイル名を「001.jpg」のようにしたい場合、ここに3と記述します。
    'number_of_digits': 3,
    # 開始ページ。3ページ目からダウンロードしたい場合、これを3に設定します。Noneは0から開始を意味します。
    'start_page': None,
    # 終了ページ。10ページ目までダウンロードしたい場合、これを10に設定します。Noneは終了までを意味します。
    'end_page': None,
}
```

## 環境のインストールとURL/Cookiesの取得方法

**このプログラムは現在Chromeで動作します。他のブラウザを使用する場合、[このページ](https://selenium-python.readthedocs.io/installation.html)を確認してください**

0.  Pythonパッケージ_selenium_と_pillow_をインストールし、_Google Chromeドライバー_を取得します。

    1.  _selenium_と_pillow_の場合：

    ```shell
    pip install selenium
    pip install Pillow
    # このundetected_chromedriverはBWに検出されないようにするためのものです
    pip install undetected_chromedriver
    ```

    2.  Google Chromeドライバーの場合：

        1.  Chromeのバージョンを確認してください。「ヘルプ」->「Google Chromeについて」。

        2.  あなたのChromeバージョンに合ったChromeドライバーを[こちら](https://sites.google.com/a/chromium.org/chromedriver/downloads)からダウンロードしてください。

        3.  任意のフォルダに入れ、そのフォルダをPATHに追加してください。

    3.  詳細については、[こちら](https://selenium-python.readthedocs.io/installation.html)を確認することを推奨します。


1.  main.pyの`IMGDIR`を、マンガを置く場所を示すように変更します。

2.  プログラムにあなたのcookiesを追加します。

    **F12を使用してcookiesを確認することを忘れないでください！**

    **一部のhttp only cookiesはjavascriptで見ることができないためです！**

    **以下のリンクにアクセスしてcookiesを取得することを忘れないでください！**

    1.  [Bookwalker.jp]のcookiesについては、[こちら](https://member.bookwalker.jp/app/03/my/profile)にアクセスしてください。
    2.  [Bookwalker.com.tw]のcookiesについては、[こちら](https://www.bookwalker.com.tw/member)にアクセスしてください。
    3.  [www.cmoa.jp]のcookiesについては、[こちら](https://www.cmoa.jp/)にアクセスし、プラグイン[EditThisCookie](http://www.editthiscookie.com/)を使用してcookiesを取得する**必要があります**。Chrome用は[こちら](https://chrome.google.com/webstore/detail/edit-this-cookie/fngmhnnpilhplaeedifhccceomclgfbg)からダウンロードしてください。

    -   `EditThisCookie`の場合、これは上記のどのウェブサイトでも使用できますが、`cmoa`の場合はこの方法を使用する**必要があります**。

        1.  `EditThisCookie`のユーザー設定(chrome-extension://fngmhnnpilhplaeedifhccceomclgfbg/options_pages/user_preferences.html)に移動します。
        2.  cookieのエクスポート形式を`Semicolon separated name=value pairs`に設定します。
        3.  [cmoa](https://www.cmoa.jp/)に移動し、`EditThisCookie`をクリックして`エクスポート`ボタンをクリックします。
        4.  ファイル内のcookies（**`// Example: http://www.tutorialspoint.com/javascript/javascript_cookies.htm`の後に続く文字列**）をプログラムにコピーします。

    -   伝統的な方法の場合

        > 1.  ページを開きます。
        > 2.  F12を押します。
        > 3.  _Network_をクリックします。
        > 4.  ページを再読み込みします。
        > 5.  最初の_profile_リクエストを見つけてクリックします。
        > 6.  右側に_Request Headers_が表示されるので、そこに移動します。
        > 7.  _cookie:...._を見つけて、_cookie:_の後の文字列をコピーし、_main.py_の_YOUR_COOKIES_HERE_に貼り付けます。

3.  _main.py_の_manga_url_を変更します。

    1.  [Bookwalker.jp]の場合

        最初に[購入済み書籍一覧](https://bookwalker.jp/holdBooks/)にアクセスしてください。ここで所有しているすべてのマンガを見つけることができます。

        今回のURLは、あなたのマンガの**「この本を読む」**ボタンのURLです。

        このボタンを右クリックし、「リンクアドレスをコピー」をクリックします。

        URLは**viewer.bookwalker.jp**ではなく、**member.bookwalker.jp**で始まります。ここでは、マンガ[【期間限定 無料お試し版】あつまれ！ふしぎ研究部 １](https://member.bookwalker.jp/app/03/webstore/cooperation?r=BROWSER_VIEWER/640c0ddd-896c-4881-945f-ad5ce9a070a6/https%3A%2F%2Fbookwalker.jp%2FholdBooks%2F)を使用します。

        これは**あつまれ！ふしぎ研究部 １**のURLです: <https://member.bookwalker.jp/app/03/webstore/cooperation?r=BROWSER_VIEWER/640c0ddd-896c-4881-945f-ad5ce9a070a6/https%3A%2F%2Fbookwalker.jp%2FholdBooks%2F>

    2.  [Bookwalker.com.tw]の場合

        [线上阅读](https://www.bookwalker.com.tw/member/available_book_list)にアクセスしてください。

        マンガURLは次のようになります：<https://www.bookwalker.com.tw/browserViewer/56994/read>

    3.  [Cmoa.jp]の場合

        マンガを開いて、ブラウザのURLをコピーするだけです。

        マンガURLは次のようになります: <https://www.cmoa.jp/bib/speedreader/speed.html?cid=0000156072_jp_0001&u0=0&u1=0&rurl=https%3A%2F%2Fwww.cmoa.jp%2Fmypage%2Fmypage_top%2F%3Ftitle%3D156072>

    このURLを_main.py_の`MANGA_URL`にコピーするだけです。

4.  プログラムを編集した後、`python main.py`を実行して実行します。

# 注意事項

1.  `SLEEP_TIME`のデフォルトは2秒です。自身のネットワーク状況に合わせて調整できます。ダウンロードで重複画像が多い場合は、5以上に変更できます。遅すぎると感じる場合は、1または0.5にしてみてください。

2.  `LOADING_WAIT_TIME = 20`は、マンガビューアページが読み込まれるまでの待機時間です。ネットワークが良くない場合は、30または50秒に設定できます。

3.  解像度は自由に変更できますが、まずオリジナル画像の解像度を確認してください。

    ```python
    RES = (784, 1200)
    ```

    オリジナル画像がより高い解像度の場合、次のように変更できます（解像度は例です）。

    ```python
    RES = (1568, 2400)
    ```

    **[Cmoa.jp]の場合は不要です。解像度は[Cmoa.jp]によって固定されています。**

4.  時々、ログアウトしてログインする必要があります。このウェブサイトは非常に厳格で、不正利用を防ぐために多くの方法をとっています。

5.  `CUT_IMAGE`を（左、上、右、下）に設定することで、画像を切り抜くことができるようになりました。

    例えば、画像の下から3px切り抜きたい場合、次のように設定できます。

    ```python
    CUT_IMAGE = (0, 0, 0, 3)
    ```

    この機能は`Pillow`を使用します。使用したい場合は、以下のコマンドでインストールする必要があります。

    ```shell
    pip install Pillow
    ```

    デフォルトでは`None`で、画像を切り抜かないことを意味します。

6.  `file_name_prefix`と`number_of_digits`を変更することで、ファイル名のプレフィックスと桁数を変更できるようになりました。

    例えば、キルラキルマンガ第1巻をダウンロードしていて、ファイル名を次のようにしたい場合：

    <pre>
        KLK_V1
        │--KLK_V1_001.jpg
        │--KLK_V1_002.jpg
        │--KLK_V1_003.jpg
    </pre>

    その場合、パラメータを以下のように設定できます：

    ```python
    settings = {
        ...,
        'file_name_prefix': 'KLK_V1',
        # ファイル名の桁数。ファイル名を「001.jpg」のようにしたい場合、ここに3と記述します。
        'number_of_digits': 3
    }
    ```

# 開発

0.  概念

    マンガをダウンロードするには、通常次のように行います：

    <pre>
    +------------+     +-----------+      +------------+      +-------------------+      +--------------+
    |            |     |           |      |            |      |                   | OVER |              |
    |   ログイン  +-----+ ページ読み込み +----->+ 画像保存   +----->+ 次のページへ移動 +----->+   完了       |
    |            |     |           |      |            |      |                   |      |              |
    +------------+     +-----------+      +-----+------+      +---------+---------+      +--------------+
                                                ^                       |
                                                |                       |
                                                |      より多くのページ   |
                                                +-----------------------+
    </pre>

    そのため、コードを再利用するためのフレームワークを作成できます。新しいウェブサイトの場合、通常はいくつかのメソッドを記述するだけで済みます。

1.  ファイル構造

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

2.  抽象`WebsiteActions`クラスの紹介。

    各ウェブサイトに対して、クラスは以下のメソッド/属性を持つ必要があります。ここではbookwalker.jpを例とします：

    ```python
    class BookwalkerJP(WebsiteActions):
        '''
        bookwalker.jp
        '''

        # login_urlは、最初に読み込んでcookiesを設定するページです。
        login_url = 'https://member.bookwalker.jp/app/03/login'

        @staticmethod
        def check_url(manga_url):
            '''
            このメソッドはブール値を返し、指定されたマンガurlがこのクラスに属するかチェックします。
            '''
            return manga_url.find('bookwalker.jp') != -1

        def get_sum_page_count(self, driver):
            '''
            このメソッドは整数を返し、総ページ数を取得します。
            '''
            return int(str(driver.find_element_by_id('pageSliderCounter').text).split('/')[1])

        def move_to_page(self, driver, page):
            '''
            このメソッドは何も返さず、指定されたページ番号に移動します。
            '''
            driver.execute_script(
                'NFBR.a6G.Initializer.B0U.menu.a6l.moveToPage(%d)' % page)

        def wait_loading(self, driver):
            '''
            このメソッドは何も返さず、マンガの読み込みを待ちます。
            '''
            WebDriverWait(driver, 30).until_not(lambda x: self.check_is_loading(
                x.find_elements_by_css_selector(".loading")))

        def get_imgdata(self, driver, now_page):
            '''
            このメソッドはString/ファイルに書き込み可能またはBytesIOに変換可能な何かを返し、画像データを取得します。
            '''
            canvas = driver.find_element_by_css_selector(".currentScreen canvas")
            img_base64 = driver.execute_script(
                "return arguments[0].toDataURL('image/jpeg').substring(22);", canvas)
            return base64.b64decode(img_base64)

        def get_now_page(self, driver):
            '''
            このメソッドは整数を返し、現在のページ上のページ番号です。
            '''
            return int(str(driver.find_element_by_id('pageSliderCounter').text).split('/')[0])
    ```

    また、`before_download`メソッドもあります。このメソッドはダウンロードを開始する前に実行されます。一部のウェブサイトでは、ダウンロードを開始する前にいくつかのポップアップコンポーネントを閉じる必要があるためです。

    ```python
    def before_download(self, driver):
        '''
        このメソッドは何も返さず、ダウンロード前に実行されます。
        '''
        driver.execute_script('parent.closeTips()')
    ```

--- 