
# robotstxt

## Overview

![](https://img.shields.io/badge/Python-3.12-blue)
![](https://img.shields.io/badge/License-AGPLv3-blue)

robots.txt を読み込み、参照権限の確認と、サイトマップの情報を取得する機能を提供します。

## Usage

```txt
User-Agent: *
Disallow: /

User-Agent: TestBot
Disallow: /
Allow: /public/

Sitemap: https://www.example.com/sitemap.xml
```

```py
import robotstxt

with open("robots.txt", "r") as file:
  loaded = robotstxt.load(file)
  loaded.permissions.is_accessable("/") #False
  loaded.permissions.is_accessable("/public/") #False
  loaded.permissions.is_accessable("/", user_agent="TestBot") #False
  loaded.permissions.is_accessable("/public/", user_agent="TestBot") #True
  loaded.sitemaps #{"https://www.example.com/sitemap.xml"}
```

## Install

```shell
pip install .
```

### Test

```shell
pip install .[test]
pytest .
```

### Document

```py
import robotstxt

help(robotstxt)
```

## Donation

<a href="https://buymeacoffee.com/tikubonn" target="_blank"><img src="doc/img/qr-code.png" width="3000px" height="3000px" style="width:150px;height:auto;"></a>

もし本パッケージがお役立ちになりましたら、少額の寄付で支援することができます。<br>
寄付していただいたお金は書籍の購入費用や日々の支払いに使わせていただきます。
ただし、これは寄付の多寡によって継続的な開発やサポートを保証するものではありません。ご留意ください。

If you found this package useful, you can support it with a small donation.
Donations will be used to cover book purchases and daily expenses.
However, please note that this does not guarantee ongoing development or support based on the amount donated.

## License

© 2025 tikubonn

robotstxt licensed under the [AGPLv3](./LICENSE).
