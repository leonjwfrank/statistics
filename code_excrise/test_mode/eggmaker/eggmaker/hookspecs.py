import pluggy

hookspec = pluggy.HookspecMarker("eggmaker")
"""HookspecMarker
    用于标记功能的装饰器帮助器类是挂钩规范。

    您可以使用project_name实例化它以获得装饰器。
    稍后调用PluginManager.add_hookspecs将发现所有标记的功能
    如果PluginManager使用相同的project_name。"""


@hookspec
def eggsample_add_ingredients(ingredients: tuple):
    """Have a look at the ingredients and offer your own.

    :param ingredients: the ingredients, don't touch them!
    :return: a list of ingredients
    """


@hookspec
def eggsample_prep_condiments(condiments: dict):
    """Reorganize the condiments tray to your heart's content.

    :param condiments: some sauces and stuff
    :return: a witty comment about your activity
    """