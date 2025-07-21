基于搜狗搜索的公众号爬虫，爬取内容放到本目录的文章目录下，并对其做归纳，归纳内容在归纳目录下。
搜索内容为输入的公众号的发表内容，不是其公众号发表的都会将其过滤。搜索只对前10页的文章进行归纳，一般都能覆盖最近几年。

# 前提工作

1. 确保系统安装了google chrome， 不是gptchrome
2. 进入wxweb目录，使用pip安装必要的库
     pip install -r requiremens.txt
3. 删除account_name文件并重新新建一个， 输入关注的公众号。输入的公众号可以先去[搜狗搜索](https://weixin.sogou.com/) 尝试搜索查看质量。
   
  
# 运行程序
## window
使用win+r 输入cmd 
进入wxweb目录， 如何使用cmd可以自行百度
运行脚本：
  python generate.py

最好使用vscode，运行方便


## ubuntu
直接进入目录运行


