
# 在线商店
## 商品类别 存储为树 ，方便检索
## 商品可以是礼包，道具，书籍，材料等。  



## 结构
   博客链接：https://github.com/stevenInno/exercise_blog

    .
    ├── cart_edu  # 存放整个项目
    │   ├── apps  # 存放应用模块包
    │   │   ├── cart  # 购物车模块
    │   │   │   ├── __init__.py  # 创建cart应用蓝图
    │   │   │   ├── models.py  # 数据库模型
    │   │   │   ├── urls.py  # 创建api，进行路由分发
    │   │   │   └── views.py  # 处理请求视图类
    │   │   ├── db  # 存放应用模型共用字段模型类
    │   │   │   ├── base_model.py
    │   │   │   └── __init__.py
    │   │   ├── goods
    │   │   │   ├── __init__.py
    │   │   │   ├── models.py
    │   │   │   ├── urls.py
    │   │   │   └── views.py
    │   │   ├── __init__.py
    │   │   ├── coupon
    │   │   │   ├── __init__.py
    │   │   │   ├── models.py
    │   │   │   ├── urls.py
    │   │   │   └── views.py
    │   │   └── user
    │   │       ├── __init__.py
    │   │       ├── models.py
    │   │       ├── urls.py
    │   │       └── views.py
    │   ├── __init__.py  # 创建flask应用文件（工厂函数）
    │   ├── static  # 静态文件存储目录
    │   ├── templates  # 模板目录
    │   └── tools  # 存放全局共用文件包
    │       ├── __init__.py
    │       └──  user.py  # 用户应用所需函数
    ├── config.py  # 配置文件
    ├── logs  # 日志文件目录
    └── manager.py  # 启动文件
  
## 基于实时的可交互数据 可视化系统
  功能 ：
  
  
     基于internet 调试协议 监控 抓取 网络 目标站点 数据包
     基于 mongo redis 处理实时数据
  
     查询线条各处的值    
       
  
     实时展示 和调整 趋势    
  
   
    
