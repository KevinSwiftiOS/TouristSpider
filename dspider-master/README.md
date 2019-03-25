dspider
========

 一款基于django的以selenium为引擎的爬虫框架。

- 用Python编写
- Web管理界面包含任务监控、项目管理、结果查看
- 数据库使用MongoDB(注意：不要设置密码)
- Python版本3.4以上
- 命令行使用视频
- https://github.com/mannuan/dspider/blob/master/docs/mp4/spider-cli.mp4
- web管理界面使用视频
- https://github.com/mannuan/dspider/blob/master/docs/mp4/spider-gui.mp4
- 依赖于有gnome-terminal的debian系列的linux系统

Installation
------------

* `pip install -r requirements.txt`
* `python manage.py migrate(用户名默认是root,密码默认是12345678)`
* `sudo apt-get install tsocks`
* run command `python manage.py runserver`, visit [http://localhost:8000/spider/](http://localhost:8000/spider/)


License
-------
Licensed under the Apache License, Version 2.0

