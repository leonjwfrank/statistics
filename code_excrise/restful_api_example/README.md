# 配置文件说明
    swagger 该文件是以分层方式组织的：缩进级别代表所有权或范围级别。

    例如，路径定义了定义所有API URL端点的起点。缩进的/ people值定义了将定义所有/ api / people URL端点的开始。下面的get：缩进定义了与/ api / people URL端点的HTTP GET请求关联的定义部分。整个配置过程都如此。

    这是swagger.yml文件此部分中各字段的含义：

    本节是全局配置信息的一部分：

    swagger：告诉Connexion正在使用哪个版本的Swagger API
    info：开始有关所构建API的新信息“作用域”
    description：用户定义的关于API提供或有关内容的描述。这是在Connexion生成的UI系统中
    版本：用户定义的API版本值
    title：Connexion生成的UI系统中包含的用户定义标题
    消费：告诉Connexion API需要的MIME类型。
    产生：告诉Connexion API的调用者期望什么内容类型。
    basePath：“ / api”定义API的根，类似于REST API的命名空间。
    本节开始配置API URL端点路径：

    路径：定义配置中包含所有API REST端点的部分。
    / people：定义URL端点的一个路径。
    get：定义此URL端点将响应的HTTP方法。与先前的定义一起，这将创建GET / api / people URL端点。
    本节开始配置单个/ api / people URL端点：

    operationId：“ people.read”定义将响应HTTP GET / api / people请求的Python导入路径/函数。为了将功能连接到HTTP请求，“ people.read”部分可能会深入到您需要的深度。类似“ <package_name>。<package_name>。<package_name>。<function_name>”之类的东西也可以正常工作。您将很快创建它。
    标签：定义UI界面的分组
    
    