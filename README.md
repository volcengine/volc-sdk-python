# 火山引擎开发者Python SDK

## 安装（建议）
require python verion >= 2.7

```
    pip install --user volcengine
```

如果已经安装volcengine包，则用下面命令升级即可
```
    pip install --upgrade volcengine
```

## 关于AK/SK

### AK/SK 注册申请流程

主账户和有权限的子用户可以新建AK密钥，操作如下：

1.使用帐号/密码登录控制台；

2.选择一级菜单“访问控制”->选择二级菜单“密钥管理”；

3.页面中展示主账号的访问密钥列表，每个IAM用户最多可同时拥有2个访问密钥，如果当前IAM用户的访问密钥数量未达到上限，则可以点击新建密钥按钮；

4.点击新建密钥按钮，弹出新建密钥弹窗，点击查看AccessKey详情，可直接查看访问密钥信息。

### 通过API申请AK/SK

[生成访问密匙](https://www.volcengine.cn/docs/6291/65578)

### AK/SK在sdk中的使用

- (option 1 推荐) 在代码里显示调用方法set_ak/set_sk，例：
  ```python
      iam_service = IamService()
      # call below method if you dont set ak and sk in $HOME/.volc/config
      iam_service.set_ak('ak')
      iam_service.set_sk('sk')
  ```

- (option 2) 在当前环境变量中分别设置 
  ```bash
  VOLC_ACCESSKEY="your ak"  
  VOLC_SECRETKEY="your sk"
  ```
- (option 3) json格式放在～/.volc/config中，格式为：
  ```json
    {"ak":"your ak","sk":"your sk"}
  ```

## 地域Region设置

- 目前已开放三个地域设置，分别为

  ```
  - cn-north-1 (默认)
  - ap-singapore-1
  - us-east-1
  ```

- 默认为cn-north-1，如果需要调用其它地域服务，请在初始化函数getInstance中传入指定地域region，例如：
  
  ```
  iam_service = IamService('us-east-1')
  ```

- 注意：IAM模块目前只开放cn-north-1区域

## SDK服务目录及实例

- 【视觉智能】请点击[这里](volcengine/visual/README.md)