English | [中文](README.md)

<h1 align="center"><img src="https://iam.volccdn.com/obj/volcengine-public/pic/volcengine-icon.png"></h1>
<h1 align="center">Volcengine SDK for Python</h1>

Welcome to Volcengine SDK for Python. This document explains how to obtain and use the SDK.

## Prerequisites

### Enable the service

Make sure the service you want to access is enabled. Go to the [Volcengine Console](https://console.volcengine.com/), select the service from the left navigation (or search it from the top bar), and complete the activation process in the service console.

### Obtain security credentials

Access Key is the credential used to access Volcengine services. It consists of Access Key ID (AK) and Secret Access Key (SK).

Log in to the [Volcengine Console](https://console.volcengine.com/), then go to [IAM](https://console.volcengine.com/iam) -> [Access Keys](https://console.volcengine.com/iam/keymanage/) to create and manage your Access Keys. For more information, see the [Access Key documentation](https://www.volcengine.com/docs/6291/65568).

### Environment check

Python version must be **3.7** or later.

## Install

Install the SDK via pip:

```bash
pip install --user volcengine
```

If `volcengine` is already installed, upgrade it with:

```bash
pip install --upgrade volcengine
```

## Configuration

### Credential configuration

Volcengine SDK for Python supports the following credential loading methods.

*Note: Replace `Your AK` and `Your SK` in the code with your actual AK and SK.*

**Method 1**: Set AK/SK on the client **(recommended)**

```python
iam_service = IamService()
iam_service.set_ak('Your AK')
iam_service.set_sk('Your SK')
```

**Method 2**: Load AK/SK from environment variables

```bash
VOLC_ACCESSKEY="Your AK"
VOLC_SECRETKEY="Your SK"
```

**Method 3**: Load AK/SK from a file under HOME

Add the following content to `~/.volc/config`:

```json
{
  "ak": "Your AK",
  "sk": "Your SK"
}
```

## Other resources

### Some service directories and examples

- [Visual Intelligence](volcengine/visual/README.md)
- [NLP](volcengine/nlp/README.md)
