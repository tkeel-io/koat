# Koat

keel of auto test

## usage

install with pipenv

```python
git clone git@github.com:tkeel-io/koat.git
cd koat
pipenv install
pipenv run pytest cases/<rudder> -s -v 

```

install with pip

``` shell
git clone git@github.com:tkeel-io/koat.git
cd koat
pip intall -r requirements.txt
pytest cases/<rudder> -s -v

```

## 什么是会话对象

=============

会话对象让你能够跨请求保持某些参数。它也会在同一个 Session 实例发出的所有请求之间保持 cookie。
会话对象具有主要的 Requests API 的所有方法。

我们来跨请求保持一些 cookie:

```python

    bs = BaseUrlSession(base_url=url)
    resp = bs.get('/apis/rudder/v1/oauth2/admin', params=payload)
    assert resp.status_code == 200

    access_token = jq('data.access_token', resp.json())
    bs.headers.update(authorization=f'Bearer {access_token}')
```

[主要接口](https://docs.python-requests.org/zh_CN/latest/api.html#id4)

## 什么是固件

=============

固件（Fixture）是一些函数，pytest 会在执行测试函数之前（或之后）加载运行它们。

我们可以利用固件做任何事情，其中最常见的可能就是初始化登录。

[参考资料](https://www.osgeo.cn/pytest/contents.html)

Pytest 使用 ``pytest.fixture()`` 定义固件，下面是最简单的固件，管理员登录平台, 创建租户空间：

```python

    # conftest.py

    @pytest.fixture()
    def admin_login(request):
        '''
        管理员登录
        '''
        bs = BaseUrlSession(base_url=url)
        resp = bs.get('/apis/rudder/v1/oauth2/admin', params=payload)
        assert resp.status_code == 200

        access_token = jq('data.access_token', resp.json())
        bs.headers.update(authorization=f'Bearer {access_token}')

        request.cls.bs = bs

固件可以显式的作为一个参数传递，创建租户之前，会先执行 ``admin_login`` , 如果有必要也可以将返回值传递到 ``create_tenant``。
.. code-block:: python

    @pytest.fixture()
    def create_tenant(request, admin_login):
        '''
        创建租户空间
        '''
        tenant_title = random_string()

        payload = {
            'title': tenant_title,
            'auth_type': "internal",
            'admin': {
                'username': "admin",
                'nick_name': "admin"
            },
            'remark': ""
        }
        resp = request.cls.bs.post('/apis/security/v1/tenants', json=payload)
        assert resp.status_code == 200

        request.cls.tenant_id = jq('data.tenant_id', resp.json())
        request.cls.reset_key = jq('data.reset_key', resp.json())
```

固件可以直接定义在各测试脚本中，就像上面的例子。更多时候，我们希望一个固件可以在更大程度上复用，这就需要对固件进行集中管理。Pytest 使用文件 ``conftest.py`` 集中管理固件。

> 在复杂的项目中，可以在不同的目录层级定义 ``conftest.py``，其作用域为其所在的目录和子目录。
>不要自己显式调用 ``conftest.py``，pytest 会自动调用，可以把 conftest 当做插件来理解。

## 什么是参数化

=============

当对一个测试函数进行测试时，通常会给函数传递多组参数。比如测试账号登陆，我们需要模拟各种千奇百怪的账号密码。

当然，我们可以把这些参数写在测试函数内部进行遍历。不过虽然参数众多，但仍然是一个测试，当某组参数导致断言失败，测试也就终止了。

通过异常捕获，我们可以保证程所有参数完整执行，但要分析测试结果就需要做不少额外的工作。

在 pytest 中，我们有更好的解决方法，就是参数化测试，即每组参数都独立执行一次测试。使用的工具就是 ``pytest.mark.parametrize(argnames, argvalues)``。

看一个多参数的例子，用于校验用户密码：

```python

    # test_parametrize.py

    @pytest.mark.parametrize('user, passwd',
                             [('jack', 'abcdefgh'),
                              ('tom', 'a123456a')])
    def test_passwd_md5(user, passwd):
        db = {
            'jack': 'e8dc4081b13434b45189a720b77b6818',
            'tom': '1702a132e769a623c1adb78353fc9503'
        }

        import hashlib

        assert hashlib.md5(passwd.encode()).hexdigest() == db[user]
```

如果觉得每组测试的默认参数显示不清晰，我们可以使用 ``pytest.param`` 的 ``id`` 参数进行自定义。

```python


    # test_parametrize.py

    @pytest.mark.parametrize('user, passwd',
                             [pytest.param('jack', 'abcdefgh', id='User<Jack>'),
                              pytest.param('tom', 'a123456a', id='User<Tom>')])
    def test_passwd_md5_id(user, passwd):
        db = {
            'jack': 'e8dc4081b13434b45189a720b77b6818',
            'tom': '1702a132e769a623c1adb78353fc9503'
        }

        import hashlib

        assert hashlib.md5(passwd.encode()).hexdigest() == db[user]
```

``pytest.mark.parametrize(argnames, argvalues)`` 也可以用在测试用例类，在测试用例类 ``TestTenant`` 执行前，会先执行 ``admin_login`` , 并将两组参数通过 ``request.param`` 传递给 ``admin_login``, 同时通过 ``request.cls`` 在测试用例类中传递测试数据

```python

    # conftest.py

    @pytest.fixture()
    def admin_login(request):
        '''
        管理员登录
        '''
        payload = {'password': admin_password}
        if hasattr(request, 'name'):
            payload.update(request.param)
        
        bs = BaseUrlSession(base_url=url)
        resp = bs.get('/apis/rudder/v1/oauth2/admin', params=payload)
        assert resp.status_code == 200

        access_token = jq('data.access_token', resp.json())
        bs.headers.update(authorization=f'Bearer {access_token}')

        request.cls.bs = bs



    @pytest.mark.parametrize("admin_login", [{'password': 'Y2hhbmdlbWU='},{'password': 'anythings'}], indirect=True)
    @pytest.mark.usefixtures("admin_login")
    class TestTenant():

        def test_create_tenant(self):
            '''
            创建租户空间
            '''
            assrt self.bs != 0
```

因为固件也是函数，我们同样可以对固件进行参数化。
固件参数化需要使用 pytest 内置的固件 ``request``，并通过 ``request.param`` 获取参数。

```python

    @pytest.fixture(params=[
        ('redis', '6379'),
        ('elasticsearch', '9200')
    ])
    def param(request):
        return request.param


    @pytest.fixture(autouse=True)
    def db(param):
        print('\nSucceed to connect %s:%s' % param)

        yield

        print('\nSucceed to close %s:%s' % param)


    def test_api():
        assert 1 == 1
```

> 与函数参数化使用 ``@pytest.mark.parametrize`` 不同，固件在定义时使用 ``params`` 参数进行参数化。
> 固件参数化依赖于内置固件 ``request`` 及其属性 ``param``。
