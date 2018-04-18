# 滑机车部署指南

**环境依赖：** 运行需要Linux系统，仅在Arch Linux进行过测试，理论上其余发行版区别不大。需要Python3.6+的运行环境。
—— [项目源码](https://github.com/boeing888/huaji_car)

**操作步骤：（以下均以Arch Linux为例，其余发行版根据具体情况进行调整）**
- 安装Mysql数据库：```pacman -S  mariadb```
- 安装Apache：```pacman -S apache```
- 安装PHP7：```pacman -S php```
- 启用PHP的mysqli模块：取消“php.ini”中```extension=php_mysqli.so```前面的注释
- 运行源码中的sql文件，导入原始测试数据库
- 安装Python模块：```sudo pip3 install tornado pymysql```
- 将“后台数据库管理代码”文件夹中的文件拷贝至Apache服务器根目录
- 进入“网站源码”目录，给予bash脚本运行权限```chmod +x ./run.sh```
- 运行网站源码中的run.sh启动网站```./run.sh```
