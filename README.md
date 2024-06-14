<h1 align="center"><img src="https://iam.volccdn.com/obj/volcengine-public/pic/volcengine-icon.png"></h1>
<h1 align="center">火山引擎SDK for Python</h1> 
欢迎使用火山引擎SDK for Python，本文档为您介绍如何获取及调用SDK。

## 前置准备
### 服务开通
请确保您已开通了您需要访问的服务。您可前往[火山引擎控制台](https://console.volcengine.com/ )，在左侧菜单中选择或在顶部搜索栏中搜索您需要使用的服务，进入服务控制台内完成开通流程。
### 获取安全凭证
Access Key（访问密钥）是访问火山引擎服务的安全凭证，包含Access Key ID（简称为AK）和Secret Access Key（简称为SK）两部分。您可登录[火山引擎控制台](https://console.volcengine.com/ )，前往“[访问控制](https://console.volcengine.com/iam )”的“[访问密钥](https://console.volcengine.com/iam/keymanage/ )”中创建及管理您的Access Key。更多信息可参考[访问密钥帮助文档](https://www.volcengine.com/docs/6291/65568 )。
### 环境检查
Python版本需要不低于3.7。

## 获取与安装

使用pip安装SDK for Python：
```
    pip install --user volcengine
```
如果已经安装volcengine包，则用下面命令升级即可：
```
    pip install --upgrade volcengine
```

## 相关配置
### 安全凭证配置
火山引擎SDK for Python支持以下几种方式进行凭证管理：

*注意：代码中Your AK及Your SK需要分别替换为您的AK及SK。*

**方式一**：在Client中设置AK/SK **（推荐）**
  ```python
      iam_service = IamService()
      iam_service.set_ak('Your AK')
      iam_service.set_sk('Your SK')
  ```

**方式二**：从环境变量加载AK/SK
  ```bash
  VOLC_ACCESSKEY="Your AK"  
  VOLC_SECRETKEY="Your SK"
  ```
**方式三**：从HOME文件加载AK/SK

在本地的~/.volc/config中添加如下内容：
  ```json
    {
      "ak": "Your AK",
      "sk": "Your SK"
    }
  ```



##其它资源
###部分SDK服务目录及示例

- 【视觉智能】请点击[这里](volcengine/visual/README.md)
- 【智能语义】请点击[这里](volcengine/nlp/README.md)
