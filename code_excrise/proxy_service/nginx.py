"""

～～～～～～～～～～～～～～～
常用的几个功能
    1，Http代理，反向代理：作为web服务器最常用的功能之一，尤其是反向代理
        正向代理
        反向代理
    2，负载均衡
        内置策略
        扩展策略

    3，web缓存
        对不同对文件做不同对缓存，支持FastCGI_Cache，主要用于对其动态程序进行缓存，配合第三方ngx_cache_purge，对制定的URL缓存内容进行增删管理


"""
# 源码：https://trac.nginx.org/nginx/browser
# 官网：http://www.nginx.org/

"""
配置文件结构，conf文件夹nginx.conf，Nginx服务器的基础配置，默认配置都在此，注释符号为 #

文件目录结构:
...              #全局块

events {         #events块
   ...
}

http      #http块
{
    ...   #http全局块
    server        #server块
    { 
        ...       #server全局块
        location [PATTERN]   #location块
        {
            ...
        }
        location [PATTERN] 
        {
            ...
        }
    }
    server
    {
      ...
    }
    ...     #http全局块
}

释义:
1、全局块：配置影响nginx全局的指令。一般有运行nginx服务器的用户组，nginx进程pid存放路径，日志存放路径，配置文件引入，允许生成worker process数等。
2、events块：配置影响nginx服务器或与用户的网络连接。有每个进程的最大连接数，选取哪种事件驱动模型处理连接请求，是否允许同时接受多个网路连接，开启多个网络连接序列化等。
3、http块：可以嵌套多个server，配置代理，缓存，日志定义等绝大多数功能和第三方模块的配置。如文件引入，mime-type定义，日志自定义，是否使用sendfile传输文件，连接超时时间，单连接请求数等。
4、server块：配置虚拟主机的相关参数，一个http中可以有多个server。
5、location块：配置请求的路由，以及各种页面的处理情况。
"""


"""配置实例
########### 每个指令必须有分号结束。#################
#user administrator administrators;  #配置用户或者组，默认为nobody nobody。
#worker_processes 2;  #允许生成的进程数，默认为1
#pid /nginx/pid/nginx.pid;   #指定nginx进程运行文件存放地址
error_log log/error.log debug;  #制定日志路径，级别。这个设置可以放入全局块，http块，server块，级别以此为：debug|info|notice|warn|error|crit|alert|emerg
events {
    accept_mutex on;   #设置网路连接序列化，防止惊群现象发生，默认为on
    multi_accept on;  #设置一个进程是否同时接受多个网络连接，默认为off
    #use epoll;      #事件驱动模型，select|poll|kqueue|epoll|resig|/dev/poll|eventport
    worker_connections  1024;    #最大连接数，默认为512
}
http {
    include       mime.types;   #文件扩展名与文件类型映射表
    default_type  application/octet-stream; #默认文件类型，默认为text/plain
    #access_log off; #取消服务日志    
    log_format myFormat '$remote_addr–$remote_user [$time_local] $request $status $body_bytes_sent $http_referer $http_user_agent $http_x_forwarded_for'; #自定义格式
    access_log log/access.log myFormat;  #combined为日志格式的默认值
    sendfile on;   #允许sendfile方式传输文件，默认为off，可以在http块，server块，location块。
    sendfile_max_chunk 100k;  #每个进程每次调用传输数量不能大于设定的值，默认为0，即不设上限。
    keepalive_timeout 65;  #连接超时时间，默认为75s，可以在http，server，location块。

    upstream mysvr {   
      server 127.0.0.1:7878;
      server 192.168.10.121:3333 backup;  #热备
    }
    error_page 404 https://www.baidu.com; #错误页
    server {
        keepalive_requests 120; #单连接请求上限次数。
        listen       4545;   #监听端口
        server_name  127.0.0.1;   #监听地址       
        location  ~*^.+$ {       #请求的url过滤，正则匹配，~为区分大小写，~*为不区分大小写。
           #root path;  #根目录
           #index vv.txt;  #设置默认页
           proxy_pass  http://mysvr;  #请求转向mysvr 定义的服务器列表
           deny 127.0.0.1;  #拒绝的ip
           allow 172.18.5.54; #允许的ip           
        } 
    }
}
"""

"""
1、几个常见配置项：

1.$remote_addr 与 $http_x_forwarded_for 用以记录客户端的ip地址；
2.$remote_user ：用来记录客户端用户名称；
3.$time_local ： 用来记录访问时间与时区；
4.$request ： 用来记录请求的url与http协议；
5.$status ： 用来记录请求状态；成功是200；
6.$body_bytes_s ent ：记录发送给客户端文件主体内容大小；
7.$http_referer ：用来记录从那个页面链接访问过来的；
8.$http_user_agent ：记录客户端浏览器的相关信息；
2、惊群现象：一个网路连接到来，多个睡眠的进程被同事叫醒，但只有一个进程能获得链接，这样会影响系统性能。

3、每个指令必须有分号结束。
"""

"""
参考：https://gist.github.com/beatfactor/a093e872824f770a2a0174345cacf171
安装过程如下
download nginx
$ cd /usr/local/src
$ curl -OL http://nginx.org/download/nginx-1.12.2.tar.gz
$ tar -xvzf nginx-1.12.2.tar.gz && rm nginx-1.12.2.tar.gz


download pcre
需要从PCRE站点下载并提取PCRE库分发（版本4.4 — 8.41）。其余的由nginx的./configure和make完成。 
http_rewrite_module和location指令中的正则表达式支持都需要PCRE。

$ curl -OL https://ftp.pcre.org/pub/pcre/pcre-8.41.tar.gz
$ tar xvzf pcre-8.41.tar.gz && rm pcre-8.41.tar.gz

cofigure nginx
cd nginx-1.12.2/
$ ./configure --with-pcre=../pcre-8.41/ 

$ curl -OL https://www.openssl.org/source/openssl-1.1.0g.tar.gz
$ tar xvzf openssl-1.1.0g.tar.gz && rm openssl-1.1.0g.tar.gz 

$ ./configure --with-pcre=../pcre-8.41/ --with-http_ssl_module --with-openssl=/usr/local/src/openssl-1.1.0g

install nginx
$ [sudo] make && make install

Add the nginx binary to $PATH:
export PATH="/usr/local/nginx/sbin:$PATH"
"""