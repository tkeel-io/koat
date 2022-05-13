# -*- coding: utf-8 -*-

''' good helper for you'''


import uuid

import jmespath
from jmespath import functions


class Functions(functions.Functions):
    """
    jmespath自定义方法
    """
    @functions.signature({'types': ['string']})
    def _func_str_to_unicode(self, s):
        """
        str转为unicode,方便中文对比
        https://github.com/jmespath/jmespath.py/issues/132
        :param s: 
        :return: 
        """
        return s.decode('utf-8')


def search(expression, data):
    """
    自定义search方法,自动传入options参数
    :param expression: 
    :param data: 
    :return: 
    """
    options = jmespath.Options(custom_functions=Functions())
    # 使用自定义方法后，所有操作都需要带上options参数
    return jmespath.search(expression, data, options)


def random_string(end=6):
    return str(uuid.uuid1())[0:end]
