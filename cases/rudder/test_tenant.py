# -*- coding: utf-8 -*-


import uuid
import pytest


# @pytest.mark.parametrize("admin_login", [{'password': 'Y2hhbmdlbWU='}], indirect=True)
@pytest.mark.usefixtures("create_tenant")
class TestTenant():

    def test_create_tenant(self):
        '''
        创建租户空间
        '''
        pass

    def test_tenant_reset_password(self, tenant_reset_password):
        '''
        重置租户密码
        '''
        pass

    @pytest.mark.run(order=1)
    def test_edit_tenant(self):
        '''
        编辑租户空间
        '''
        tenant_id = self.tenant_id
        new_tenant_title = str(uuid.uuid1())[0:8]

        payload = {
            'title': new_tenant_title,
            'remark': "这是一个修改版"
        }
        resp = self.bs.put(
            f'/apis/security/v1/tenants/{tenant_id}', json=payload)
        assert resp.status_code == 200

    @pytest.mark.run(order=2)
    def test_delete_tenant(self):
        '''
        删除租户空间
        '''
        tenant_id = self.tenant_id
        resp = self.bs.delete(f'/apis/security/v1/tenants/{tenant_id}')
        assert resp.status_code == 200
