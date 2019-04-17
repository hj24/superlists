# 配置新网站

======================================

## 文件夹结构

假设有用户账号，家目录为/home/username

/home/username

|___ SITENAME

​          |___ database

​          |___ source

​          |___ static

​          |___ virtualenv

## 需要的包

- Python 3.6
- pip
- virtualenv 
- Git 
- nginx
- gunicorn

以 **centos 6** 为例，Ubuntu相对更简单：

1. Python 3.6 + pip3

   step 1:准备安装环境

   ```shell
   yum groupinstall 'Development Tools'
   yum install zlib-devel bzip2-devel  openssl-devel ncurses-devel
   ```

   step 2: 下载并解压python3.6.1版本

   ```shell
   wget https://www.python.org/ftp/python/3.6.1/Python-3.6.1.tgz
   tar zxvf  Python-3.6.1.tgz
   ```

   step 3: 编译安装

   ```shell
   cd Python-3.6.1
   ./configure --prefix=/usr/local/python3
   make && make install
   ```

   step 4: 设置环境变量

   ```shell
   echo 'export PATH=$PATH:/usr/local/python3/bin' >> ~/.bashrc
   ```

   step 5: 重启

   现在就可以使用python3.6 和 pip3 了

2. virtualenv

   ```shell
   pip3 install virtualenv
   ```

3. Git

   ```shell
   sudo yum install git
   ```

4. nginx

   ```shell
   sudo yum install nginx
   ```

   相关命令：

   ```shell
   /etc/init.d/nginx start # 启动Nginx服务
   /etc/init.d/nginx stop # 停止Nginx服务
   /etc/nginx/nginx.conf # Nginx配置文件位置
   chkconfig nginx on    #设为开机启动
   ```

5. Gunicorn

   在项目中的Python中的虚拟环境中安装，假设当前在~/sites/SITENAME/source/:

   ```shell
   ../virtualenv/bin/pip install gunicorn
   ```

## 配置nginx虚拟主机

- 参考 nginx.template.conf
- 把其中的SITENAME替换成所需的域名，例如：tddlist.tk即可

## Upstart 服务(自启动脚本)

- 参考gunicorn-tddlist.conf
- 把其中的SITENAME替换成所需的域名，例如：tddlist.tk即可

- 把EMAIL_PASSWORD替换自己的邮箱密码
- 把SERVER_PASSWORD替换为自己的服务器密码