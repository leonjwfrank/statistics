## 实现任务
### 1， 实现一个虚拟购物车类Cart，可添加，删除，修改数量，统计价格，统计商品数量；
### 2， 实现一个优惠券类CouponTotal， 可查看基本信息，如有效期时间(多种格式的)，是否还在有效期内， 设置有效期；
### 3， 实现一个收银台类SummaryResult， 可查看当前购物车，可计算当前购物车商品数量，可根据优惠券是否有效计算购物车商品总价格。
### 4,  实现一个测试模块，对购物车，优惠券，收银台类功能进行基本测试。


## 结构
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
    └── cart_manage.py  # 启动文件
