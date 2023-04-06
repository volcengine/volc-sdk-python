.. bioos documentation master file, created by
   sphinx-quickstart on Thu Mar 16 15:15:05 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to bioos's documentation!
=================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

      bioos <bioos.rst>

Installation
==================

Python 版本需要不低于2.7，可以直接通过pip进行安装

Example
------------------
        ::

            pip install volcengine

Quickstart
==================

密钥使用授权
------------------
*仅子账号需要关注*

1. 登录控制台，点击右上角头像，在下拉菜单中选择「访问控制」。

2. 点击左侧边的「策略管理」，确认本子账户拥有「AccessKeyFullAccess」权限或包含此权限的更高级权限，例如「AdministratorAccess」，若没有则用 主账号 登录控制台为子账户添加相关权限。

Example
------------------
        ::

         from __future__ import print_function

         from volcengine.bioos.BioOsService import BioOsService

         if __name__ == '__main__':
             # set endpoint/region here if the default value is unsatisfied
             bioos_service = BioOsService(endpoint='endpoint', region='region')

             # call below method if you don't set ak and sk in $HOME/.volc/config
             bioos_service.set_ak('ak')
             bioos_service.set_sk('sk')

             params = {}

             resp = bioos_service.list_workspaces(params)
             print(resp)

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
