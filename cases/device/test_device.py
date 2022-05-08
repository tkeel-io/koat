# -*- coding: utf-8 -*-


import pytest


@pytest.mark.usefixtures("create_templates")
class TestDevice():

    def test_create_device(self):
        '''
        创建设备
        '''
        pass
