"""
This is the people module and supports all the ReST actions for the
PEOPLE collection

。您将为人员端点定义的所有CRUD方法都将共享此标记定义。
    摘要定义了此端点的UI界面显示文本。
    description：定义UI界面将为实现说明显示的内容。


    本节定义了来自URL端点的成功响应的配置部分：

    响应：定义预期响应部分的开始。
    200：定义成功响应的部分，HTTP状态码200。
    description：定义UI界面显示文本，响应为200。
    模式：将响应定义为模式或结构。
    类型：将模式的结构定义为数组。
    items：开始定义数组中的项目。
    属性：将数组中的项目定义为具有键/值对的对象。
    fname：定义对象的第一个键。
    type：将与fname关联的值定义为字符串。
    lname：定义对象的第二个键。
    type：将与lname关联的值定义为字符串。
    时间戳：定义对象的第三个键。
    类型：将与时间戳关联的值定义为字符串。
    人员端点处理程序
    在swagger.yml文件中，您配置了具有operationId值的Connexion，以在API获取针对GET / api / people的HTTP请求时调用人员模块和模块中的读取功能。这意味着people.py模块必须存在并且包含read（）函数。这是您将创建的people.py模块：

    在这段代码中，您创建了一个名为get_timestamp（）的帮助程序函数，该函数生成当前时间戳记的字符串表示形式。当您开始使用API​​修改数据时，它用于创建内存结构并修改数据。

然后，您创建了PEOPLE词典数据结构，它是一个简单的名称数据库，以姓氏为关键字。这是一个模块变量，因此其状态在REST API调用之间保持不变。在实际的应用程序中，PEOPLE数据将存在于数据库，文件或网络资源中，这可以持久保存数据，而不是运行/停止Web应用程序。

然后，您创建了read（）函数。服务器收到对GET / api / people的HTTP请求时，将调用此方法。该函数的返回值将转换为JSON字符串（调用swagger.yml文件中的produces：定义）。您创建的read（）函数将构建并返回按姓氏排序的人员列表。

运行服务器代码并在浏览器中导航到localhost：5000 / api / people将在屏幕上显示人员列表：
"""

# System modules
from datetime import datetime

# 3rd party modules
from flask import make_response, abort


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


# Data to serve with our API
PEOPLE = {
    "Farrell": {
        "lname": "Farrell",
        "fname": "Ad12",
        "price": 160,
        # "bill": False,
        "timestamp": get_timestamp()
    },
    "Brockman": {
        "lname": "Brockman",
        "fname": "ABC1",
        "price": 210,
        # "bill": False,
        "timestamp": get_timestamp()
    },
    "Easter": {
        "lname": "Easter",
        "fname": "CD123",
        "price": 220,
        # "bill": False,
        "timestamp": get_timestamp()
    }
}


def read_all():
    """
    This function responds to a request for /api/people
    with the complete lists of people
    :return:        json string of list of people
    """
    # Create the list of people from our data
    return [PEOPLE[key] for key in sorted(PEOPLE.keys())]


def read_one(lname):
    """
    This function responds to a request for /api/people/{lname}
    with one matching person from people
    :param lname:   last name of person to find
    :return:        person matching last name
    """
    # Does the person exist in people?
    if lname in PEOPLE:
        person = PEOPLE.get(lname)

    # otherwise, nope, not found
    else:
        abort(
            404, "Person with name {lname} not found".format(lname=lname)
        )

    return person


def create(person):
    """
    This function creates a new person in the people structure
    based on the passed in person data
    :param person:  person to create in people structure
    :return:        201 on success, 406 on person exists
    """
    lname = person.get("lname", None)
    fname = person.get("fname", None)
    price = person.get("price", 0)

    # Does the person exist already?
    if lname not in PEOPLE and lname is not None:
        PEOPLE[lname] = {
            "lname": lname,
            "fname": fname,
            "price": price,
            "timestamp": get_timestamp(),
        }
        return PEOPLE[lname], 201

    # Otherwise, they exist, that's an error
    else:
        abort(
            406,
            "Peron with name {lname} already exists".format(lname=lname),
        )


def update(lname, person):
    """
    This function updates an existing person in the people structure
    :param lname:   last name of person to update in the people structure
    :param person:  person to update
    :return:        updated person structure
    """
    # Does the person exist in people?
    if lname in PEOPLE:
        PEOPLE[lname]["fname"] = person.get("fname")
        PEOPLE[lname]["price"] = person.get("price")
        PEOPLE[lname]["timestamp"] = get_timestamp()

        return PEOPLE[lname]

    # otherwise, nope, that's an error
    else:
        abort(
            404, "Person with name {lname} not found".format(lname=lname)
        )


def delete(lname):
    """
    This function deletes a person from the people structure
    :param lname:   last name of person to delete
    :return:        200 on successful delete, 404 if not found
    """
    # Does the person to delete exist?
    if lname in PEOPLE:
        del PEOPLE[lname]
        return make_response(
            "{lname} successfully deleted".format(lname=lname), 200
        )

    # Otherwise, nope, person to delete not found
    else:
        abort(
            404, "Person with name {lname} not found".format(lname=lname)
        )