qcos
==========

腾讯云对象存储库，支持命令行

安装
----

通过pip安装::

    pip install qcos

配置
----

使用官方的 `命令行工具CLI <https://www.qcloud.com/product/cli>`_ 配置secret_id, scret_key


代码中使用
----------

参照源码，比较简单, 调用方式::

    client = COSClient(secret_id, secret_key, region, appid, bucket)
    # 简单上传
    client.upload_local(local_path, cos_path)
    # 查询文件属性
    client.stat(cos_path)


命令行
------

格式::

    qcos 本地文件夹 appid bucket cos文件夹路径


比如::

    qcos ./build 10000 image-bucket /
