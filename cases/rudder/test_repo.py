# -*- coding: utf-8 -*-


import pytest


@pytest.mark.usefixtures('admin_login')
class TestRepo():

    def test_add_repo(self):
        '''
        添加仓库
        '''
        pass
