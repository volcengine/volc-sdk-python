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

___(wis)___

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

- 【视觉智能】请点击[这里](volcengine/example/visual/README.md)