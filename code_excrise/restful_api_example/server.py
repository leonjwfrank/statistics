"""
Main module of the server file
"""

# 3rd party moudles
from flask import render_template, send_file
import connexion
import os

"""
这使Connexion模块可用于您的程序。 Connexion模块允许Python程序使用Swagger规范。这提供了很多功能：验证往返于您的API的输入和输出数据，配置API URL端点和所需参数的简便方法，以及一个非常好的UI界面，可与创建的API一起使用并进行探索。

当您创建应用程序可以访问的配置文件时，所有这些都可能发生。 Swagger站点甚至提供了一个在线配置编辑器工具，以帮助创建和/或语法检查将要创建的配置文件。
"""

# Create the application instance
app = connexion.App(__name__, specification_dir="./")
"""
使用Connexion将REST API URL端点添加到您的应用程序分为两个部分。您会将Connexion添加到服务器，并创建将使用的配置文件。
以将Connexion添加到服务器：
"""

# Read the swagger.yml file to configure the endpoints
app.add_api("agger.yml")
"""
您已经添加了几件事将Connexion整合到服务器中。 import connexion语句将模块添加到程序中。下一步是使用Connexion而非Flask创建应用程序实例。在内部，仍会创建Flask应用程序，但现在已添加了其他功能。

应用实例创建的一部分包括参数specification_dir。这将通知Connexion要在哪个目录中查找其配置文件，在本例中为当前目录。此后，您添加了以下行：

app.add_api（'swagger.yml'）

这告诉应用程序实例从规范目录读取文件swagger.yml并配置系统以提供Connexion功能。

agger
文件agger.yml是YAML或JSON文件，其中包含配置服务器以提供输入参数验证，输出响应数据验证，
URL端点定义和Swagger UI所需的所有信息。这是swagger.yml文件，用于定义REST API将提供的GET / api / people端点：



class ImageForm(FlaskForm):
    description = StringField('添加描述', validators=[InputRequired(), Length(max=160)])
    # description = PageDownField("description for image", validators=[DataRequired()])
    image = FileField('提示，上传的图片名称格式:字母和数字组合', validators=[FileRequired(),
                                        FileAllowed(images, 'Images only!')])
    submit = SubmitField('上传')


@main.route('/add_new', methods=['GET', 'POST'])
@login_required
def add_new():
    # Cannot pass in 'request.form' as this initializes the form with a specific form data, which replaces
    # the default data attribute (FileField) with the FileStorage object
    # form = PostForm()
    form_image = ImageForm()

    for item in request.__dict__:
        print('request:{}, item:{}, file_name:{}'.format(type(item), item, type(item)))
    print('file_type:{}, files:{}'.format(type(request.files), request.files))
    print('request:{}, args:{}'.format(request.__dict__, request.args))
    time_suff = '{}'.format(str(datetime.datetime.now())[:10])
    if request.method == 'POST':
        if form_image.validate_on_submit():
            f = request.files['image']
            print('{}, file name:{}'.format(f, f.filename))
            f.filename = '{}-{}'.format(time_suff, str(f.filename))
            filename = images.save(storage=f, folder=current_app.config['UPLOADED_IMAGES_DEST'])

            print('filename:{}, config:{}, type:{}, des:{} '.format(filename, current_app.config,
                                                                    type(form_image.description),
                                                                    form_image.description))
            url = '{}{}'.format(current_app.config['UPLOADED_IMAGES_URL'], str(f.filename))
            img_entry = PostImg(image_string=form_image.description.data, image_filename=filename, image_url=url,
                                image_own=current_user.username)
            db.session.add(img_entry)
            db.session.commit()
            # f.save(current_app.config['UPLOADED_IMAGES_DEST'] + secure_filename(f.filename))
            flash('The Image {} was added, url for:'.format(f.filename))
            flash('{}'.format(url))
            # return redirect(url_for('main.add_new'))
        else:
            # flash_errors(form)
            flash('ERROR! Recipe was not added.', 'error')

    return render_template('add_new.html', form=form_image)
"""


@app.route("/menu", methods=['GET', 'POST'])
def menu():
    """
    :return:
    """
    # return send_file(filename_or_fp='static/san_menu.png')
    return send_file(filename_or_fp='static/san_menu.jpg')
    # return send_from_directory(os.path.join('./', 'static/menu'), "san_menu.jpeg")


# create a URL route in our application for "/"
@app.route("/")
def home():
    """
    This function just responds to the browser URL
    localhost:5000/
    :return:        the rendered template "start.html"
    """
    return render_template("start.html")


"""

Swagger UI
现在，您有了一个带有单个URL端点的简单Web API。在这一点上，可以合理地认为：​​“使用swagger.yml文件进行配置很酷，但是，这对我有什么帮助呢？”

您会认为是正确的。我们没有利用输入或输出验证。 swagger.yml给我们提供的只是对连接到URL端点的代码路径的定义。但是，您还可以获得额外的工作，就是为您的API创建Swagger UI。

如果导航到localhost：5000 / api / ui，系统将显示一个类似于以下内容的页面：

这将显示预期响应的结构，该响应的内容类型以及您在swagger.yml文件中输入的有关端点的描述文本。

您甚至可以通过单击“试用”来试用端点！屏幕底部的按钮。这将进一步扩展界面，使其看起来像这样：

当API完整时，这将非常有用，因为它为您和您的API用户提供了一种无需编写任何代码即可探索和试验API的方法。

以这种方式构建API对我的工作非常有用。 Swagger用户界面不仅可以用作试验API和阅读提供的文档的方式，而且还具有动态性。每当配置文件更改时，Swagger UI也会更改。

另外，该配置提供了一种很好的，干净的方式来考虑和创建API URL端点。我从经验中知道，API有时会随时间以随机的方式进行开发，这使得找到支持端点的代码以及协调它们充其量非常困难。

通过将代码与API URL端点配置分开，我们可以使一个与另一个脱钩。在我的工作中，对支持单页Web应用程序的API系统而言，仅此一项就对我非常有用。

建立完整的API
我们最初的目标是构建一个API，以提供对我们人员结构的完整CRUD访问。您还记得，我们的API的定义如下所示：

为此，您将扩展swagger.yml和people.py文件以完全支持上面定义的API。为了简洁起见，将仅为两个文件提供一个链接：

swagger.yml
people.py

Swagger UI已完成
更新完swagger.yml和people.py文件以完成people API功能后，Swagger UI系统将进行相应更新，如下所示：
通过该用户界面，您可以查看swagger.yml文件中包含的所有文档，并与构成人员界面的CRUD功能的所有URL端点进行交互。

演示单页应用程序
您已经拥有有效的REST API，并且具有出色的Swagger UI文档/交互系统。但是，您现在如何处理？下一步是创建一个Web应用程序，以半实用的方式演示API的使用。

您将创建一个Web应用程序，以在屏幕上显示人员，并允许用户创建新人员，更新现有人员和删除人员。所有这些都将通过从JavaScript到people API URL端点的AJAX调用来处理。

首先，您需要扩展home.html文件，使其看起来像这样：

上面的HTML代码扩展了home.html文件，以引入外部normalize.min.css文件，该文件是CSS重置文件，用于标准化浏览器中元素的格式。

它还会引入外部jquery-3.3.1.min.js文件，以提供用于创建单页应用程序交互性的jQuery功能。

上面的HTML代码创建了应用程序的静态框架。出现在表结构中的动态部分将由JavaScript在加载时以及用户与应用程序交互时添加。

静态文件
在您创建的home.html文件中，有两个静态文件的引用：static / css / home.css和static / js / home.js。要添加这些内容，您需要将以下目录结构添加到应用程序中：

因为Flask应用程序将自动为名为static的目录提供服务，所以您放置在css和js文件夹中的任何文件都将可用于home.html文件。为了简洁起见，以下是指向home.css和home.js文件的链接：

home.css
home.js
JavaScript文件
如前所述，JavaScript文件提供了与Web应用程序的所有交互和更新。它通过使用MVC（模型/视图/控制器）设计模式将必要的功能分为三个部分来实现此目的。

每个对象都是由一个自调用函数创建的，该函数返回自己的API供其他组件使用。例如，在实例化过程中，将参数的Model和View实例作为参数传递给Controller。它通过这些对象公开的API方法与这些对象进行交互。

唯一的其他连接是通过AJAX方法调用上的自定义事件在模型和控制器之间建立的：

Model 该模型提供了与人员API的连接。当用户交互事件需要它时，Controller会调用它自己的API与服务器进行交互。
Views 视图提供了更新Web应用程序DOM的机制。当用户交互事件需要它时，Controller会调用它自己的API来更新DOM。
Control 控制器提供所有事件处理程序，供用户与Web应用程序进行交互。这允许它调用模型以向人员API发出请求，并向视图发出以使用从人员API接收到的新信息来更新DOM的请求。
它还处理由模型对人员API发出的异步AJAX请求生成的自定义事件。

这是home.js文件中使用的MVC结构的示意图：

这个想法是，Controller与Model和View都有很强的联系。模型与Controller的链接（自定义事件）较弱，而与View的连接则完全没有。从模型到控制器的薄弱环节减少了耦合和依赖性，这在这种情况下很有用。


创建按钮允许用户在服务器上的人员结构中创建新人员。当您输入名字和姓氏并点击创建时，控制器会调用模型向POST / api / people URL端点发出请求。这将验证姓氏不存在。如果不是，它将在人员结构中创建一个新人员。

这会在模型中生成一个自定义事件，该事件使控制器再次调用模型以请求GET / api / people，这将返回已排序人员的完整列表。然后，控制器将其传递到视图以重绘人员表。

双击表中的任何行，将在应用程序的编辑器部分填充“姓氏”和“姓氏”字段。此时，用户可以更新或删除此人。

要成功更新，用户必须更改有关“名字”的内容。姓氏必须与要更新的人的查找键保持相同。单击更新后，控制器将调用模型以向PUT / api / people / {lname} URL端点发出请求。这将验证姓氏当前是否存在。如果是这样，它将在人员结构中更新该人员。

这会在模型中生成一个自定义事件，该事件使控制器再次调用模型以请求GET / api / people，这将返回已排序人员的完整列表。然后，控制器将其传递到视图以重绘人员表。

要成功删除，用户只需单击删除。单击删除后，控制器将调用模型以向DELETE / api / people / {lname} URL端点发出请求。这将验证姓氏当前是否存在。如果是这样，它将从人员结构中删除该人员。

这会在模型中生成一个自定义事件，该事件使控制器再次调用模型以请求GET / api / people，这将返回已排序人员的完整列表。然后，控制器将其传递到视图以重绘人员表。

尝试在编辑器中故意犯错误，例如拼写姓氏，然后查看由Web应用程序上表示的API生成的错误。
"""

if __name__ == "__main__":
    """
    当您运行此应用程序时，Web服务器将在端口5000上启动，这是Flask使用的默认端口。如果打开浏览器并导航到localhost：5000，应该会看到Hello World！显示。现在，这对于查看Web服务器正在运行很有用。您稍后将使用正在开发的REST API将home.html文件扩展为一个完整的单页Web应用程序。

在Python程序中，您已经导入了Flask模块，从而使应用程序可以访问Flask功能。然后，您创建了Flask应用程序实例，即app变量。接下来，通过使用@ app.route（'/'）装饰URL连接，将URL路由'/'连接到home（）函数。此函数调用Flask render_template（）函数从模板目录中获取home.html文件，并将其返回到浏览器。

所有示例代码都可以从本文结尾处提供的链接中获得。
    """
    app.run(debug=True)
