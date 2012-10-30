# comics4kindle

从 [http://manhua.178.com](http://manhua.178.com) 网站抓取最新漫画图片并下载到本地，生成 html 文件无广告地看漫画，同时支持生成 mobi 格式并发送到你的 kindle 邮箱（例如`comics4kindle@kindle.com`），这样就能够在 kindle 上看最新的漫画了（尽管 kindle 4/kindle touch 的 6 寸小屏幕看起来体验差了些）。


## how

comics4kindle 用 python 完成，依赖两个 Python 的第三方模块，以及 mobi 生成工具 kindlegen。

- Python
- requests -- 完美封装 Python 的 urllib/urllib2 库
- pyquery -- Python 下的 jQuery 实现
- Amazon kindlegen

模块直接 sudo easy_install xxx 即可，不过如果是 Windows 下，pyquery 没那么容易安装，因为它依赖 lxml 模块，这个模块我是从非官方编译好的 exe(http://www.lfd.uci.edu/~gohlke/pythonlibs/) 进行安装的。

至于我的 OS X 10.6.8，折腾好久都安装不成功（包括看[官网文档](http://lxml.de/installation.html) ），先放弃在 Windows 下完成再说，虽然是很吸引人的模块。

Amazon kindlegen，如果你的 Amazon 帐号地区是 China 的话，直接提示 unavailable，所以得修改下所在 country 才行。**安装完成之后记得将 kindlegen 添加到环境变量中，否则生成 mobi 会失败。**


## 如何使用

目前只支持`海贼王hz` `火影hy` `死神ss` `妖精的尾巴yj`，要增加其他的自己到 [http://manhua.178.com](http://manhua.178.com) 网站看 URL 是咋样并添加到代码中就行。例如，海贼王的是 **http://manhua.178.com/haizeiwang**，最后面是拼音而已，代码如下：

    COMICS = {
        'hz': 'haizeiwang',
        'hy': 'huoyingrenzhe',
        'ss': 'sishen',
        'yj': 'yaojingdeweiba'
    }

    COMIC_NAMES = {
        'haizeiwang': '海贼王',
        'huoyingrenzhe': '火影忍者',
        'sishen': '死神',
        'yaojingdeweiba': '妖精的尾巴'
    }

- 需要发送 mobi 漫画到 kindle 邮箱

    python comics4kindle.py `hz/hy/ss/yj` `mail_from` `mail_to` `mail_pwd`

- 如果不想发送到 kindle 邮箱，不要给出后面跟 mail 相关的参数即可

    python comics4kindle.py `hz/hy/ss/yj`

如果参数个数错误，有如下提示：

    Usage: python comics4kindle.py phz/hy/ss/yj] --> 抓取漫画图片保存到本地
    python comics4kindle.py [hz/hy/ss/yj] [mail_from] [mail_to] [mail_pwd] --> 发到邮箱，例如kindle邮箱


## why

本来看漫画（海贼王、火影）是每周三必期待的事情（周三就开始要打开 GR 看更新了没），谁知前阵子有一次竟然忙到忘了看漫画，推到周五晚上才看。想想感觉不太正常，突然想到手中有个 kindle，或许能够推送到 kindle 尝尝鲜也好，于是...这也是为啥叫`comics4kindle`的原因。


## what

用 python 写个脚本从`manhua.178.com`抓取指定漫画最新一章的 URL，然后根据 HTML 的一点点规律把图片给下载到本地。根据 kindle 电子书的格式要求生成 html 文件，再利用 Amazon 官方的 kindlegen 工具从 html 生成 mobi 文件，利用发送邮件附件的方式推送到指定的 kindle 邮箱，这样就能够在 kindle 上看漫画了。

- 获取指定漫画最新一章的 URL 
- 抓取最新一章中图片的 URL 
- 根据图片 URL 将其下载到本地 
- 根据 kindle 电子书规范生成 html 文件
- 用 Amazon 官方的 kindlegen 工具从 html 生成 mobi 文件
- 将 mobi 文件作为邮件附件发送到 kindle 邮箱
- kindle wifi 同步后即可开始看最新漫画


### 示例输出

    第305话
    http://manhua.178.com/yaojingdeweiba/18744.shtml
    images\yaojingdeweiba\第305话
    第305话\001.jpg
    第305话\002.jpg
    第305话\003.jpg
    第305话\004.jpg
    第305话\005.jpg
    第305话\006.jpg
    第305话\007.jpg
    第305话\008.jpg
    第305话\009.jpg
    第305话\010.jpg
    第305话\011.jpg
    第305话\012.jpg
    第305话\013.jpg
    第305话\014.jpg
    第305话\015.jpg
    第305话\016.jpg
    第305话\017.jpg
    第305话\018.jpg
    第305话\019.jpg
    第305话\020.jpg
    第305话\021.jpg
    images\yaojingdeweiba\妖精的尾巴_第305话.html
    kindlegen images\yaojingdeweiba\妖精的尾巴_第305话.html -c2 -locale zh -o 妖精的
    尾巴_第305话.mobi

    *********************************************************
    Amazon.com kindlegen(Windows) V2.5 build 0626-3a91e28
    命令行电子书制作软件
    Copyright Amazon.com 2012
    *********************************************************

    信息:I9007:选项：-c2：Kindle Huffdic 压缩
    信息(prcgen):I1047: 已添加的元数据dc:Title        "妖精的尾巴 第305话"
    信息(prcgen):I1002: 解析文件  0000002
    信息(prcgen):I1015: 创建 PRC 文件
    信息(prcgen):I1006: 分析超链接
    警告(prcgen):W14016: 没有指定封面
    警告(core):W1002: 字符串转换不精确。
    信息(prcgen):I1045: 本书中使用 UNICODE 范围计算
    信息(prcgen):I1046: 已发现的 UNICODE 范围：Basic Latin [20..7E]
    信息(prcgen/compress):I4001: 编译原文本以进行压缩（最大为 4096 次）。程数  00000
    01
    信息(prcgen/compress):I4001: 编译原文本以进行压缩（最大为 4096 次）。程数  00000
    02
    信息(prcgen/compress):I4001: 编译原文本以进行压缩（最大为 4096 次）。程数  00000
    04
    信息(prcgen/compress):I4001: 编译原文本以进行压缩（最大为 4096 次）。程数  00000
    08
    信息(prcgen/compress):I4001: 编译原文本以进行压缩（最大为 4096 次）。程数  00000
    16
    信息(prcgen/compress):I4001: 编译原文本以进行压缩（最大为 4096 次）。程数  00000
    32
    信息(prcgen/compress):I4001: 编译原文本以进行压缩（最大为 4096 次）。程数  00000
    64
    信息(prcgen/compress):I4001: 编译原文本以进行压缩（最大为 4096 次）。程数  00001
    21
    信息(prcgen/compress):I4002: 压缩程  0000001
    信息(prcgen/compress):I4002: 压缩程  0000002
    信息(prcgen/compress):I4002: 压缩程  0000003
    信息(prcgen/compress):I4006: 文本压缩为（原始大小的 %）：  106.50%
    信息(prcgen/compress):I4007: 压缩字典统计：  000003026字节000000045 条目
    信息(prcgen/compress):I4002: 压缩程  0000004
    信息(prcgen/compress):I4006: 文本压缩为（原始大小的 %）：  106.29%
    信息(prcgen/compress):I4007: 压缩字典统计：  000003014字节000000044 条目
    信息(prcgen/compress):I4002: 压缩程  0000005
    信息(prcgen/compress):I4006: 文本压缩为（原始大小的 %）：  106.39%
    信息(prcgen/compress):I4007: 压缩字典统计：  000003008字节000000044 条目
    信息(prcgen/compress):I4005: 成功完成高级压缩（解码和验证）。
    信息(prcgen):I1039: 最终统计 - 文本压缩为（原始大小的 %）：  106.39%
    信息(prcgen):I1040: 文档标识符是： "CGYGC_U305D"
    信息(prcgen):I1041: 文件格式版本是 V5
    信息(prcgen):I1031: 保存 PRC 文件
    信息(prcgen):I1033: 创建 PRC 出现警告！
    信息(prcgen):I1016: 创建改进的 PRC 文件
    信息(prcgen):I1007: 分析媒体链接
    信息(prcgen):I1011: 写入媒体链接
    信息(prcgen):I1009: 分析指导项
    信息(prcgen):I1046: 已发现的 UNICODE 范围：CJK Unified Ideographs [4E00..9FFF]
    信息(prcgen/compress):I4001: 编译原文本以进行压缩（最大为 4096 次）。程数  00001
    20
    信息(prcgen/compress):I4006: 文本压缩为（原始大小的 %）：  76.42%
    信息(prcgen/compress):I4007: 压缩字典统计：  000003620字节000000128 条目
    信息(prcgen/compress):I4006: 文本压缩为（原始大小的 %）：  76.14%
    信息(prcgen/compress):I4007: 压缩字典统计：  000003536字节000000120 条目
    信息(prcgen/compress):I4006: 文本压缩为（原始大小的 %）：  76.07%
    信息(prcgen/compress):I4007: 压缩字典统计：  000003492字节000000115 条目
    信息(prcgen/compress):I4002: 压缩程  0000006
    信息(prcgen/compress):I4006: 文本压缩为（原始大小的 %）：  76.09%
    信息(prcgen/compress):I4007: 压缩字典统计：  000003472字节000000111 条目
    信息(prcgen):I1039: 最终统计 - 文本压缩为（原始大小的 %）：  76.09%
    信息(prcgen):I1041: 文件格式版本是 V8
    信息(prcgen):I1032: 成功创建 PRC
    信息(prcgen):I1037: 创建 Mobi 域名文件出现警告！

    mobi 文件生成完毕
    images\yaojingdeweiba\妖精的尾巴_第305话.mobi
    正在发送邮件[===妖精的尾巴_第305话@comics4kindle===]...
