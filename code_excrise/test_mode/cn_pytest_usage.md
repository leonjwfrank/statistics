# 安装和简单样例
    1，安装python3
    使用pip安装 pytest
        pip3 install pytest==5.2.0
        或
        pip3 install -U pytest
    版本确认
     $ pytest --version
        This is pytest version 5.x.y, imported from $PYTHON_PREFIX/lib/python3.7/site-
        ˓→packages/pytest.py
    2，创建一个简单测试case
    
        #  content of test_sample.py
        def func(x): return x + 1
        失败测试
        def test_answer(): assert func(3) == 5
        成功测试
        def test_five(): assert func(4) == 5
        
    3，执行测试case，
        pytest test_sample.py
        pytest将默认将 test开头的函数当成case执行
    执行结果，两个项目，一个成功，一个失败
        collected 2 items                                                                                                                                                                                      

        simple_test.py F.                                                                                                                                                                                [100%]

        =============================================================================================== FAILURES ===============================================================================================
        _____________________________________________________________________________________________ test_answer ______________________________________________________________________________________________

            def test_answer():
        >       assert func(3) == 5
        E       assert 4 == 5
        E        +  where 4 = func(3)

        simple_test.py:6: AssertionError
        ===================================================================================== 1 failed, 1 passed in 0.10s ======================================================================================
    4 执行多个
        pytest将在当前目录及子目录中，发现和运行test_*.py 和 *_test.py所有测试文件。更一般而言，它遵循标准的测试发现规则。
        测试文件发现规则，步骤
        1 如果未指定任何参数，则收集将从测试路径（如果已配置）或当前目录开始。另外，命令行参数可以在目录，文件名或节点ID的任何组合中使用。
        2 递归到指定目录，除非它们匹配norecursedirs(无递归)
        3 在这些目录中，搜索通过测试包名称导入的test _ *。py或* _test.py文件。
        4 从这些文件中，收集测试项目：
            –在类之外测试带有前缀的测试函数或方法
            –测试前缀，测试类中的测试前缀测试函数或方法（无__init__方法）
            有关如何自定义测试发现的示例，请参见更标准（Python）测试发现。在Python模块中，pytest还使用标准unittest.TestCase子类化技术发现测试。
    * 5 参数， 忽略 --ignore 某些路径
        通过在cli上传递--ignore = path选项，可以轻松地在收集过程中忽略某些测试目录和模块。 pytest允许多个--ignore选项。例：
        例:tests/
        |-- example
            |-- test_example_01.py
            |-- test_example_02.py
            '-- test_example_03.py
        |-- foobar
            |-- test_foobar_01.py
            |-- test_foobar_02.py
            '-- test_foobar_03.py
        '-- hello
                '-- world
                    |-- test_world_01.py
                    |-- test_world_02.py
                    '-- test_world_03.py
         如果您使用--ignore = tests / foobar / test_foobar_03.py --ignore = tests / hello /调用pytest，您将看到pytest仅收集测试模块，这些模块与指定的模式不匹配
         =========================== test session starts ============================
            platform linux -- Python 3.x.y, pytest-5.x.y, py-1.x.y, pluggy-0.x.y
            rootdir: $REGENDOC_TMPDIR, inifile:
            collected 5 items
            tests/example/test_example_01.py .          [ 20%]
            tests/example/test_example_02.py .          [ 40%]
            tests/example/test_example_03.py .          [ 60%]
            tests/foobar/test_foobar_01.py .            [ 80%]
            tests/foobar/test_foobar_02.py .            [100%]

         ========================= 5 passed in 0.02 seconds =========================
         --ignore-glob选项允许忽略基于Unix Shell样式通配符的测试文件路径。如果要排除以_01.py结尾的测试模块，请使用--ignore-glob ='* _ 01.py'执行pytest。
         
    * 6 参数  --deselect 定制实例和技巧
         通过传递--deselect = item选项，可以在收集过程中分别取消选择测试。例如，假设tests / foobar / test_foobar_01.py包含test_a和test_b。
         您可以通过使用--deselect tests / foobar / test_foobar_01.py :: test_a调用pytest来运行tests /中除tests / foobar / test_foobar_01.py :: test_a以外的所有测试。 
         pytest允许多个--deselect选项。
         
         保留重复路径 --keep-duplicates 
            pytest的默认行为是忽略从命令行指定的重复路径。例：
            pytest path_a path_a
            ...
            collected 1 item
            
            pytest --keep-duplicates path_a path_a
            ...
            collected 2 item
            
            单个文件是默认保留的
            由于收集器仅适用于目录，因此，如果您为单个测试文件指定两次，则pytest仍将收集两次，无论是否未指定--keep-duplicates。例：
            pytest file_a.py file_a.py
            ...
            collected 2 item
         
         
    * 7 更改搜索目录 -- 标准目录
         您可以在ini文件中设置非递归目录 norecursedirs，例如在项目根目录中的pytest.ini:
             content of pytest.ini
            [pytest]
            norecursedirs = .svn _build tmp*
         这将告诉pytest，发现测试文件时，不要递归到典型的subversion或sphinx-build目录或任何带tmp前缀的目录。
         
    * 8 更改测试文件命名约定
         您可以通过设置python_files，python_classes和python_functions配置选项来配置不同的命名约定。这是一个例子：
         # content of pytest.ini
            # Example 1: have pytest look for "check" instead of "test"
            # can also be defined in tox.ini or setup.cfg file, although the section # name in setup.cfg files should be "tool:pytest"
            [pytest]
            python_files = check_*.py
            python_classes = Check
            python_functions = *_check
            
         这将使pytest在与check_ * .py glob-pattern匹配的文件，在类中的Check前缀以及与* _check匹配的函数和方法中查找测试。例如，如果我们有：
            # content of check_myapp.py
            class CheckMyApp:
                def simple_check(self): pass
                def complex_check(self): pass
            
           执行: pytest --collect-only
           =========================== test session starts ============================
            platform linux -- Python 3.x.y, pytest-5.x.y, py-1.x.y, pluggy-0.x.y
            cachedir: $PYTHON_PREFIX/.pytest_cache
            rootdir: $REGENDOC_TMPDIR, inifile: pytest.ini
            collected 2 items
            <Module check_myapp.py>
            <Class CheckMyApp>
             <Function simple_check>
             <Function complex_check>
           ========================== no tests ran in 0.12s ===========================
           您可以通过在模式之间添加空格来检查多个glob模式：
            # Example 2: have pytest look for files with "test" and "example"
            # content of pytest.ini, tox.ini, or setup.cfg file (replace "pytest" # with "tool:pytest" for setup.cfg)
            [pytest]
            python_files = test_*.py example_*.py
           注意：python_functions和python_classes选项对unittest.TestCase测试发现无效，因为pytest将测试用例方法的发现委托给unittest代码。
     * 9 参数 --pyargs 将命令行参数解释为Python包，所跟的参数是否为可导入的程序包
        您可以使用--pyargs选项使pytest尝试将参数解释为python包名称，派生其文件系统路径，然后运行测试。例如，如果您安装了unittest2，则可以键入：    
            pytest --pyargs unittest2.test.test_skipping -q    
        它将运行相应的测试模块。与其他选项一样，通过ini文件和addopts选项，您可以更永久地进行此更改：
            #  content of pytest.ini
            [pytest]
            addopts = --pyargs
        现在，作为pytest NAME的简单调用将检查NAME是否存在于可导入的程序包/模块中，否则将其视为文件系统路径。
        
    10 查看测试文件中哪些能被收集
        pytest --collect-only pythoncollection.py
        =========================== test session starts ============================
        platform linux -- Python 3.x.y, pytest-5.x.y, py-1.x.y, pluggy-0.x.y
        cachedir: $PYTHON_PREFIX/.pytest_cache
        rootdir: $REGENDOC_TMPDIR, inifile: pytest.ini
        collected 3 items
        <Module CWD/pythoncollection.py>
        <Function test_function>
        <Class TestClass>
             <Function test_method>
            <Function test_anothermethod>
        ========================== no tests ran in 0.12s ===========================    
        
## 可插拔系统 pluggy
    pytest 可以使用pluggy实现可插拔case
    1，组成要素
    host or host program:   通过指定钩子函数并在程序执行过程中调用其实现来提供可扩展性的程序   
    plugin:     当主机调用实现时，实现指定钩子（的子集）并参与程序执行的程序
    pluggy:  通过使用连接主机和插件
        定义主机提供的呼叫签名的钩子规范（又称为钩子规范-请参阅标记钩子）
            * 插件是命名空间类型（当前是类或模块中的一种），它定义了一组挂钩函数。
            * 如插件注册表中所述 所有指定挂钩的插件(pluggy API) 均由pluggy.PluginManager实例管理和定义。
            * 为了使PluginManager能够检测到计划用作钩子命名空间中的函数，必须使用特殊的标记来装饰它们。
            
        由注册插件提供的钩子实现（也称为hookimpl-请参阅回调）
        挂钩调用方-在主机中适当程序位置触发的调用循环，调用实现并收集结果
    当PluginManager扫描插件上定义的挂钩函数时，将使用project_name值。这允许来自多个项目的多个插件管理器相互定义挂钩。
    
    2，使用钩子
    Pluggy的核心功能使扩展提供程序可以覆盖整个程序，程序中某些地点进行的函数调用都可以用到扩展程序。
    通过调用plugy._HookCaller的实例来调用特定的挂钩，该实例循环通过 1:N 注册的hookimpls并依次顺序调用它们。
    每个pluggy.PluginManager都有一个hook属性，该属性是此pluggy._HookRelay的一个实例。 
    _HookRelay本身包含对每个已注册hookimpl的_HookCaller实例的引用(按挂钩名称)
    请注意，您必须使用关键字参数语法来调用钩子！
    调用实例:
        import sys
        import pluggy
        import mypluginspec
        import myplugin
        from configuration import config

        pm = pluggy.PluginManager("myproject")
        pm.add_hookspecs(mypluginspec)
        pm.register(myplugin)

        # we invoke the _HookCaller and thus all underlying hookimpls
        result_list = pm.hook.myhook(config=config, args=sys.argv)
    挂钩实现按LIFO注册顺序调用:最后一个注册插件的挂钩首先调用。例如，以下断言不应出错:
    代码见jupyter book
    
    收集结果(collecting results)
    默认情况下，调用钩子会导致所有基础hookimpls函数通过循环依次调用。任何返回非None值的函数都会将该结果附加到调用返回的列表中。
    唯一的例外情况是，如果挂钩已标记为仅返回其第一个结果，则在这种情况下，仅将返回第一个单个值（不是None）。
    
    例外和异常处理(Exception handing)
    如果有任何带有异常的hookimpl错误，则不会再调用任何回调，并且将该异常打包并传递给任何Wrappers，然后在挂钩调用点重新引发该异常：
    
    3 历史调用
    历史调用允许所有新注册的函数接收在注册之前发生的所有挂钩调用。含义是，仅当您期望在首次调用该挂钩之后可能会注册一些hookimpls时，这才有用。
    必须使用pluggy._HookCaller.call_historic（）方法对历史挂钩进行特殊标记和调用：
        
    您可以使用插件的子集进行呼叫，方法是先向PluginManager询问_HookCaller，并使用Pluggy.PluginManager.subset_hook_caller（）方法删除了那些插件。

    然后，您可以根据需要使用_HookCaller进行常规，call_historic（）或call_extra（）调用。
    
    4 在pytest中钩子调用
    对于任何给定的挂钩规范，可能有多个实现，因此我们通常将挂钩执行视为1:N函数调用，其中N是已注册函数的数量。
    有多种方法可以影响钩子实现是在其他实现之前还是之后，即函数在N尺寸列表中的位置:
    # Plugin 1
        @pytest.hookimpl(tryfirst=True)
        def pytest_collection_modifyitems(items):
            # will execute as early as possible
            ...

    # Plugin 2
        @pytest.hookimpl(hookwrapper=True)
        def pytest_collection_modifyitems(items):
            # will execute even before the tryfirst one above!
            outcome = yield
            # will execute after all non-hookwrappers executed
    
    执行顺序如下：

    插件3的pytest_collection_modifyitems被调用直到yield 返回，因为它是一个钩子包装(hook wrapper)。
    之所以调用Plugin1的pytest_collection_modifyitems，是因为其标有tryfirst = True。
    之所以调用Plugin2的pytest_collection_modifyitems，是因为它标有trylast = True（但即使没有此标记，它也会在Plugin1之后出现）。
    然后，Plugin3的pytest_collection_modifyitems执行yield点之后的代码。 
    yield接收一个Result实例，该实例封装了调用非包装程序的结果。包装程序不得修改结果。
    可以同时将tryfirst和trylast与hookwrapper = True结合使用，在这种情况下，这将影响hookwrapper彼此之间的顺序。
    
    
## pytest 用于非python测试
    这是一个示例conftest.py（摘自Ali Afshnars专用pytest-yamlwsgi插件）。此conftest.py将收集test * .yaml文件并将执行yaml格式的内容作为自定义测试
    
           
## 用法和援引(usage & invocations)
    
## 在已有测试集中使用pytest，集成unitTest.TestCase 
    以下pytest功能可在unittest.TestCase子类中使用： 
    • Marks: skip, skipif , xfail;
    • Auto-use fixtures;
    以下pytest功能不起作用，由于不同的设计理念，可能永远不会起作用：•灯具（自动使用的fixtures除外，请参见下文）；
    • Parametrization;
    • Custom hooks;
    第三方插件可能无法正常运行，具体取决于插件和测试套件。
    
    将pytest固定装置混入unittest.TestCase使用标记来子类化
    使用pytest运行unittest允许您将其装饰器机制与unittest.TestCase样式测试一起使用。
    假设您至少略过了pytest 装饰器功能，让我们开始一个示例，该示例集成了pytest db_class固定装置，设置了一个类缓存的数据库对象，然后从unittest风格的测试中引用它：
    # content of conftest.py
    # we define a fixture function below and it will be "used" by
    # referencing its name from tests
    import pytest
    @pytest.fixture(scope="class") 
    def db_class(request):
        class DummyDB: pass
            # set a class attribute on the invoking test context
            # 在调用测试上下文上设置类属性
            request.cls.db = DummyDB()
    
    这定义了一个插件函数db_class，如果使用它，则为每个测试类调用一次，并将类级别的db属性设置为DummyDB实例。
    固定装置功能通过接收特殊的请求对象来实现此目的，该对象可以访问请求的测试上下文，例如cls属性，表示使用固定装置的类。
    这种架构使装饰器的编写与实际的测试代码脱钩，并允许通过最少的引用（夹具名称）重新使用夹具。因此，让我们使用灯具定义编写一个实际的unittest.TestCase类：
    # content of test_unittest_db.py
    import unittest
    import pytest
    @pytest.mark.usefixtures("db_class") 
    class MyTest(unittest.TestCase):
        def test_method1(self):
            assert hasattr(self, "db")
            assert 0, self.db # fail for demo purposes
        def test_method2(self):
            assert 0, self.db # fail for demo purposes
        
    @pytest.mark.usefixtures(“db_class”)类修饰符可确保每个类一次调用pytest固定函数db_class。
    由于故意使assert语句失败，我们可以看一下追溯中的self.db值.
    @pytest test_unittest_db.py 
    ___________________________ MyTest.test_method2 ____________________________
    self = <test_unittest_db.MyTest testMethod=test_method2>
    def test_method2(self):
        >       assert 0, self.db  # fail for demo purposes
        E       AssertionError: <conftest.db_class.<locals>.DummyDB object at 0xdeadbeef>
        E       assert 0
        test_unittest_db.py:13: AssertionError
    ============================ 2 failed in 0.12s =============================
    缺省的pytest追溯显示这两个测试方法共享相同的self.db实例，这是我们在编写上面的类作用域的装饰器函数时使用的意图。
    尽管通常最好明确声明使用给定测试所需的装饰器，但有时您可能希望拥有在给定上下文中自动使用的装饰器。
    毕竟，传统的单元测试设置样式要求使用这种隐式的装饰器编写，并且您习惯或喜欢它。
    您可以使用@pytest.fixture（autouse = True）标记装饰器功能，并在要使用它的上下文中定义装饰器功能。
    让我们看一下一个initdir固定程序，该程序使TestCase类的所有测试方法都在带有预先初始化的samplefile.ini的临时目录中执行。
    我们的initdir装饰器本身使用pytest内置的tmpdir装饰器来委派每次测试临时目录的创建: 
    
## 记录和报告测试的判定

## pytest 显式，模块化，可扩展(explicit, modular, scalable)
    参数化装饰器和测试功能
    可以对装饰器功能进行参数设置，在这种情况下，每次执行一组相关测试时，它们将被多次调用e。
    取决于此装饰器的测试。测试功能通常不需要知道它们的重新运行。
    装饰器参数化有助于为组件编写详尽的功能测试，这些组件本身可以通过多种方式进行配置。
    扩展前面的示例，我们可以标记装饰器以创建两个smtp_connection fixture 实例，这将导致使用该fixture的所有测试运行两次。
     Fixture函数通过特殊的请求对象访问每个参数：
     # content of conftest.py
    import pytest
    import smtplib
    @pytest.fixture(scope="module", params=["smtp.gmail.com", "mail.python.org"]) def smtp_connection(request):
    smtp_connection = smtplib.SMTP(request.param, 587, timeout=5) yield smtp_connection
    print("finalizing {}".format(smtp_connection)) smtp_connection.close()
    主要更改是使用@pytest.fixture声明参数，这是固定值函数将执行的每个值的列表，并可通过request.param访问值。
    无需更改测试功能代码。因此，让我们再进行一次运行:
    * 执行和输出
     pytest -q test_module.py
    FFFF                                                                 [100%]
    ================================= FAILURES =================================
    ________________________ test_ehlo[smtp.gmail.com] _________________________
    smtp_connection = <smtplib.SMTP object at 0xdeadbeef>
    def test_ehlo(smtp_connection):
        response, msg = smtp_connection.ehlo()
        assert response == 250
        assert b"smtp.gmail.com" in msg
    >       assert 0  # for demo purposes
    E       assert 0
    

## 用属性标记测试功能 marks
    通过使用pytest.mark帮助程序，您可以轻松地在测试功能上设置元数据。有一些内置标记，例如
    • skip - 总是跳过的功能
    • skipif - 如果条件满足，跳过某个功能
    • xfail - 如果满足特定条件，则会产生“预期的失败”结果•参数化以执行对同一测试功能的多次调用。
    
    [pytest]
    markers =
        slow: marks tests as slow (deselect with '-m "not slow"')
        serial    
    注意:之后的所有内容均为可选说明。另外，您可以在pytest_configure挂钩中以编程方式注册新标记
    
    
## 模拟模块和环境(Monkeypatching)
    有时，测试需要调用依赖于全局设置的功能，或者调用无法轻易测试的代码（例如网络访问）的功能。 
    Monkeypatch固定装置可帮助您安全地设置/删除属性，字典项或环境变量，或修改sys.path进行导入。
    Monkeypatch固定装置提供了以下帮助程序方法，用于安全地修补和模拟测试中的功能:
        monkeypatch.setattr(obj, name, value, raising=True)
        monkeypatch.delattr(obj, name, raising=True)
        monkeypatch.setitem(mapping, name, value)
        monkeypatch.delitem(obj, name, raising=True)
        monkeypatch.setenv(name, value, prepend=False)
        monkeypatch.delenv(name, raising=True)
        monkeypatch.syspath_prepend(path)
        monkeypatch.chdir(path)
        
    请求的测试功能或固定装置完成后，所有修改都将被撤消。如果设置/删除操作的目标不存在，则raising参数确定是否将引发KeyError或AttributeError。
    
    
## 临时文件夹和文件(temporary)
    您可以使用tmp_path固定装置，该固定装置将为测试调用提供唯一的临时目录，该目录在基本临时目录。
    tmp_path是pathlib / pathlib2.Path对象。这是测试用法示例:
    # content of test_tmp_path.py
    import os
    CONTENT = "content"
    def test_create_file(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "hello.txt"
    p.write_text(CONTENT)
    assert p.read_text() == CONTENT
    assert len(list(tmp_path.iterdir())) == 1 assert 0    
    
    执行 pytest test_tmp_path.py
    
## 捕获标准测试输出和文件
    在执行测试期间，将捕获发送到stdout和stderr的所有输出。如果测试或设置方法失败，则通常会显示其相应的捕获输出以及失败回溯。 
    （可以通过--show-capture命令行选项配置此行为）。
    此外，将stdin设置为“ null”对象，如果尝试从其读取将失败，因为在运行自动化测试时很少希望等待交互式输入。
    默认情况下，捕获是通过拦截对低级文件描述符的写入来完成的。这允许捕获简单打印语句的输出以及测试启动的子流程的输出。
    pytest可以执行两种捕获方式：
        •文件描述符（FD）级别捕获（默认）：所有写入操作系统文件描述符1和2的操作将被捕获​​。
        •sys级捕获：仅捕获对Python文件sys.stdout和sys.stderr的写入。不捕获对文件描述符的写入。
        您可以从命令行影响输出捕获机制:
         pytest -s # disable all capturing
         pytest --capture=sys # replace sys.stdout/stderr with in-mem files 
         pytest --capture=fd # also point filedescriptors 1 and 2 to temp file
    
        # content of test_module.py
        def setup_function(function): print("setting up", function)
        def test_func1(): assert True
        def test_func2(): assert False
    运行该模块将精确显示失败函数的输出并隐藏另一个函数:
    ________________________________ test_func2 ________________________________
    def test_func2():
        >       assert False
        E       assert False
        test_module.py:12: AssertionError
    -------------------------- Captured stdout setup ---------------------------
    setting up <function test_func2 at 0xdeadbeef>
    
## 警告捕获
    从3.1版开始，pytest现在会在测试执行期间自动捕获警告，并在会话结束时显示警告:
    # content of test_show_warnings.py
    import warnings
    def api_v1():
    warnings.warn(UserWarning("api v1, should use functions from v2")) return 1
    def test_one():
    assert api_v1() == 1
    
    $ pytest test_show_warnings.py
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-5.x.y, py-1.x.y, pluggy-0.x.y
    cachedir: $PYTHON_PREFIX/.pytest_cache
    rootdir: $REGENDOC_TMPDIR
    collected 1 item
    test_show_warnings.py .                                              [100%]
    ============================= warnings summary =============================
    test_show_warnings.py::test_one
    $REGENDOC_TMPDIR/test_show_warnings.py:5: UserWarning: api v1, should use functions ˓→from v2
    warnings.warn(UserWarning("api v1, should use functions from v2"))
    -- Docs: https://docs.pytest.org/en/latest/warnings.html    
    
    可以传递-W标志来控制将显示哪些警告，甚至将它们变成错误：
    $ pytest -q test_show_warnings.py -W error::UserWarning
    F                                                                    [100%]
    ================================= FAILURES =================================
    _________________________________ test_one _________________________________
    def test_one():
    >       assert api_v1() == 1
    test_show_warnings.py:10: ______________________________________
    def api_v1():
    >       warnings.warn(UserWarning("api v1, should use functions from v2"))
    E       UserWarning: api v1, should use functions from v2
    test_show_warnings.py:5: UserWarning
    1 failed in 0.12s
    
    当警告匹配列表中的多个选项时，将执行最后一个匹配选项的操作。
    -W命令行选项和filterwarnings ini选项都基于Python自己的-W选项，并且警告-ings.simplefilter，因此请参阅Python文档中的这些部分，以获取其他示例和高级用法。
        
    您可以使用@pytest.mark.filterwarnings将警告过滤器添加到特定的测试项目，以便您可以更好地控制应在测试，课程甚至模块级别捕获哪些警告：
    
    使用标记应用的过滤器优先于通过命令行或由filterwarnings ini选项配置的过滤器。
    您可以通过将filterwarnings标记用作类装饰器，将过滤器应用于类的所有测试，或者可以通过设置pytestmark变量将过滤器应用于模块中的所有测试：
    import warnings
    def api_v1():
    warnings.warn(UserWarning("api v1, should use functions from v2")) return 1
    @pytest.mark.filterwarnings("ignore:api v1") def test_one():
    assert api_v1() == 1
    
    # turns all warnings into errors for this module
    pytestmark = pytest.mark.filterwarnings("error")
    
    对于pytest-warnings插件中的参考实现，请参考Florian Schulze。
    
    当有效地删除了过时的警告时，这可以帮助用户使代码保持现代化并避免损坏。
    
## doctest 文件测试 Doctest集成模块和测试文件
    默认情况下，所有与test * .txt模式匹配的文件都将通过python标准doctest模块运行。您可以通过发出以下命令来更改模式：
    pytest --doctest-glob='*.rst'
    在命令行上。 --doctest-glob可以在命令行中多次给出。如果您有这样的文本文件:
    # content of test_example.txt
    hello this is a doctest
    >>> x = 3
    >>> x
    3
    执行，
    pytest test_example.txt
    collected 1 item
    test_example.txt .                                                   [100%]
    ============================ 1 passed in 0.12s =============================
    
    默认情况下，pytest将收集test * .txt文件以查找doctest指令，但是您可以使用--doctest-glob选项（多允许）传递其他glob。
    除了文本文件，您还可以直接从类和函数的文档字符串中执行doctest，包括从测试模块中执行：
    # content of mymodule.py
    def something():
        """ a doctest in a docstring >>> something()
            42
        """
        return 42
   
    测试模块文件py中的doc文档
     pytest --doctest-modules
      =========================== test session starts ============================
        platform linux -- Python 3.x.y, pytest-5.x.y, py-1.x.y, pluggy-0.x.y
        cachedir: $PYTHON_PREFIX/.pytest_cache
        rootdir: $REGENDOC_TMPDIR
        collected 2 items
        mymodule.py .           [ 50%]
        test_example.txt .       [100%]

      ============================ 2 passed in 0.12s =============================
     
    您可以通过将它们放入pytest.ini文件中，使这些更改在项目中永久存在：
    #  content of pytest.ini
    [pytest]
    addopts = --doctest-modules
    内置的pytestdoctest测试仅支持doctest块，但是如果您在找所有文档（包括doctests，.. codeblock :: python Sphinx指令支持）以及所有其他示例进行检查，您不妨考虑使用Sybil。
    Sybil它提供开箱即用的pytest集成。

##  Skip 和 xfail， 处理无法执行的测试
    跳过和xfail：处理无法成功的测试
    xfail表示您希望测试由于某种原因而失败。一个常见的示例是对尚未实现的功能或尚未修复的错误进行测试。如果尽管测试通过，但预期会失败（标记为pytest.mark.xfail），则它是xpass，并会在测试摘要中报告。
    pytest分别计数和列出跳过和xfail测试。默认情况下，不显示有关跳过/未通过测试的详细信息，以避免混乱输出。您可以使用-r选项查看与测试进度中显示的“短”字母相对应的详细信息：
    pytest -rxXs # show extra info on xfailed, xpassed, and skipped tests
    
    您可以使用xfail标记来指示您期望测试失败：
    @pytest.mark.xfail
    def test_function(): ...
    
    该测试将运行，但失败时不会报告任何回溯。相反，终端报告将在“预期失败”（XFAIL）或“意外通过”（XPASS）部分列出该报告。
    另外，您也可以从测试或设置功能中强制将测试标记为XFAIL：
    def test_function():
    if not valid_config():
        pytest.xfail("failing configuration (but should work)")
        
    这将无条件使test_function为XFAIL。请注意，在pytest之后不会再执行其他代码。 xfail调用，与标记不同。那是因为它是通过引发已知异常在内部实​​现的。
    参考：pytest.mark.xfail
    
    除非严格的仅关键字参数作为True传递，否则XFAIL和XPASS都不会使测试套件失败。
     @pytest.mark.xfail(strict=True) def test_function():...
    这会使该测试的XPASS（“意外通过”）结果无法通过测试套件。
    您可以使用xfail_strict ini选项更改strict参数的默认值:
     [pytest]
    xfail_strict=true
    
    reason parameter
    与skipif一样，您也可以标记对特定平台失败的期望：
     @pytest.mark.xfail(sys.version_info >= (3, 6), reason="python3.6 api changes") def test_function():...

    raises 参数
    如果您想更具体地说明测试失败的原因，则可以指定一个异常或一个异常元组，在引发异常。
     @pytest.mark.xfail(raises=RuntimeError) def test_function():...
     
    run parameter
    如果测试应标记为xfail并报告为xfail，但不应执行，则将run参数用作False：
     @pytest.mark.xfail(run=False) def test_function():... 
    
    忽略xfail ，通过指令运行
    pytest --runxfail
    
    您可以强制运行和报告xfail标记的测试，就像根本没有标记一样。这也会导致pytest.xfail无效。 
    完整的例子
    import pytest
    xfail = pytest.mark.xfail
    
    @xfail
    def test_hello(): assert 0
    
    @xfail(run=False) 
    def test_hello2():assert 0
    
    @xfail("hasattr(os, 'sep')") 
    def test_hello3():assert 0
    
    @xfail(reason="bug 110") 
    def test_hello4():assert 0
    
    @xfail('pytest.__version__[0] != "17"') 
    def test_hello5():assert 0
    
    def test_hello6(): pytest.xfail("reason")
    
    @xfail(raises=IndexError) 
    def test_hello7():x = [] x[1] = 1
    
    执行，使用report-on-xfail选项运行它会得到以下输出：
    example $ pytest -rx xfail_demo.py
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-5.x.y, py-1.x.y, pluggy-0.x.y
    cachedir: $PYTHON_PREFIX/.pytest_cache
    rootdir: $REGENDOC_TMPDIR/example
    collected 7 items
    xfail_demo.py xxxxxxx                                                [100%]
    ========================= short test summary info ==========================
    XFAIL xfail_demo.py::test_hello
    XFAIL xfail_demo.py::test_hello2
      reason: [NOTRUN]
    XFAIL xfail_demo.py::test_hello3
      condition: hasattr(os, 'sep')
    XFAIL xfail_demo.py::test_hello4
      bug 110
    XFAIL xfail_demo.py::test_hello5
      condition: pytest.__version__[0] != "17"
    XFAIL xfail_demo.py::test_hello6
      reason: reason
    XFAIL xfail_demo.py::test_hello7
    ============================ 7 xfailed in 0.12s ============================
    
## 参数化装饰器和测试功能
    3个级别的装饰器功能
    •pytest.fixture（）允许参数化装饰器功能。
    •@pytest.mark.parametrize允许在测试函数或类中定义多组参数和装饰器。
    •pytest_generate_tests允许定义自定义参数化方案或扩展。
    
    @pytest.mark.parametrize: parametrizing test functions
    内置的pytest.mark.parametrize装饰器为测试函数启用参数的参数化。这里有一个测试功能的典型示例，该功能实现检查某些输入是否导致期望的输出：
    # content of test_expectation.py
    import pytest
    @pytest.mark.parametrize("test_input,expected", [("3+5", 8), ("2+4", 6), ("6*9", 42)]) def test_eval(test_input, expected):
    assert eval(test_input) == expected
    
    在这里，@parametrize装饰器定义了三个不同的（test_input，expected）元组，以便t​​est_eval函数依次使用它们运行三遍：
    运行和输出
    $ pytest test_expectation.py
    ================================= FAILURES =================================
    ____________________________ test_eval[6*9-42] _____________________________
    test_input = '6*9', expected = 42
    @pytest.mark.parametrize("test_input,expected", [("3+5", 8), ("2+4", 6), ("6*9", ˓→42)])
    > E E
    def test_eval(test_input, expected):
        assert eval(test_input) == expected
        AssertionError: assert 54 == 42
        +  where 54 = eval('6*9')
    test_expectation.py:6: AssertionError
    ======================= 1 failed, 2 passed in 0.12s ========================
    
    字符问题
    pytest默认情况下会使用dinunicode字符串转义任何非ascii字符以进行参数化，因为这有几个缺点。
    但是，如果您想在参数化中使用unicode字符串，并在终端中按原样查看它们（未转义），请在pytest.ini中使用以下选项：
     [pytest]
    disable_test_id_escaping_and_forfeit_all_rights_to_community_support = True
    但是请记住，根据所使用的操作系统和当前安装的插件，这可能会导致不良的作用，甚至导致错误，因此使用此方法后果自负。
    
## 缓存：使用跨测试运行状态
    
    该插件提供了两个命令行选项来从上次pytest调用中重新运行失败：•--lf，--last-failed-仅重新运行失败。
    •--ff，-failed-first-先运行故障，然后再运行其余测试。
    为了进行清理（通常不需要），--cache-clear选项允许在测试运行之前删除所有跨会话缓存的内容。
    其他插件可以访问config.cache对象以在pytest调用之间设置/获取json可编码的值。
    
    该插件默认情况下处于启用状态，但可以根据需要禁用：请参阅通过以下方式停用/注销插件：名称(此插件的内部名称为cacheprovider).
    仅重新运行故障或先运行故障
    示例
    创建50个测试请求，并且设置2个失败
      
    # content of test_50.py
    import pytest
    @pytest.mark.parametrize("i", range(50)) 
    def test_num(i):
        if i in (17, 25): pytest.fail("bad luck")
    执行和输出
    pytest -q words_modes.py  # -q 和不带参数，执行顺序一样，两个失败 F F
    .................F.......F........................  
    words_modes.py:32: Failed
    _____________________________________________________________________________________________ test_num[25] _____________________________________________________________________________________________

    i = 25
    
    @pytest.mark.parametrize("i", range(50))
    def test_num(i):
    >       if i in (17, 25): pytest.fail("bad luck")
    E       Failed: bad luck

    words_modes.py:32: Failed
    2 failed, 48 passed in 0.25s
    
    pytest -lf words_modes.py 
    FF 
    仅执行两次失败case
    
    如果使用--ff选项运行，则将运行所有测试，但之前的第一个失败将首先执行（可以从FF和点系列中可以看到）：
    先执行失败case
     FF................................................ 
     
    
    新增--nf，--new-first选项：先运行新测试，然后再进行其余测试，在这两种情况下，测试还按照文件修改时间进行排序，最新的文件排在第一位。
    先执行新增case 
    .................F.......F........................  
    
    
#### cache 处理，失败时是否继续执行
    如果在上次运行中没有测试失败，或者找不到缓存的最后失败数据，则可以使用--last-failed-no-failures选项将pytest配置为运行所有测试或不运行测试。以下值：
    pytest --last-failed --last-failed-no-failures all # 继续执行 run all tests (default ˓→behavior)
    pytest --last-failed --last-failed-no-failures none # 不继续执行，退出  run no tests and exit
    
    插件或conftest.py支持代码可以使用pytest配置对象获取缓存的值。
    这是一个实现pytest装饰器的基本示例插件：显式，模块化，可扩展(pytest fixtures: explicit, modular, scalable  )
    可在pytest调用之间重用先前创建的状态：
    
    # content of test_caching.py
    import pytest
    import time
    def expensive_computation():
        print("running expensive computation...")
    @pytest.fixture
    def mydata(request):
        val = request.config.cache.get("example/value", None) if val is None:
        expensive_computation()
        val = 42
        request.config.cache.set("example/value", val)
        return val
    def test_function(mydata): assert mydata == 23
    
    执行后查看缓存信息--cache-show， 也可以使用可选参数来指定用于过滤的全局模式：
    $ pytest --cache-show example/*
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-5.x.y, py-1.x.y, pluggy-0.x.y
    cachedir: $PYTHON_PREFIX/.pytest_cache
    rootdir: $REGENDOC_TMPDIR
    cachedir: $PYTHON_PREFIX/.pytest_cache
    ----------------------- cache values for 'example/*' -----------------------
    example/value contains:
     42
    ========================== no tests ran in 0.12s ===========================
    
    缓存清理
    pytest --cache-clear
    
    建议从Continuous Integration服务器进行调用，因为隔离和正确性比速度更重要。
    
#### 跳过失败case继续执行   
    作为--lf -x的替代方法，尤其是在您希望测试套件的大部分都将失败的情况下，--sw，--stepwise 允许您一次修复它们。
    测试套件将一直运行到第一个失败，然后停止。在下一次调用时，测试将从上一个失败的测试继续，然后运行直到下一个失败的测试。
    您可以使用--stepwise-skip选项忽略一个失败的测试，而在第二个失败的测试上停止测试执行。如果您被困在失败的测试上并且只想忽略它直到以后，这将很有用。

## pytest