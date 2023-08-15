qcos
==========

腾讯云对象存储库，支持命令行

安装
----

通过pip安装::

    pip install qcos

配置
----

使用官方的 `命令行工具CLI <https://cloud.tencent.com/document/product/440>`_ 配置secret_id, scret_key


代码中使用
----------

参照源码，比较简单, 调用方式::

    from qcos import Client
    client = Client(secret_id, secret_key, region, bucket)
    # 根据路径上传
    client.put_local('a.txt', local_path)
    # 直接上传内容
    client.put_object('a.txt', data='content')
    # 检查文件是否存在
    client.head_object('a.txt')


命令行
------

格式::

    qcos 本地文件夹 region bucket cos文件夹路径

比如::

    qcos ./build ap-beijing testbucket-10000 /
