## Example

调用代码示例均在`volcengine/example/visual`文件夹下，以下为银行卡OCR调用示例

```python
# coding:utf-8
from __future__ import print_function

from volc.visual.VisualService import VisualService

if __name__ == '__main__':
    visual_service = VisualService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    visual_service.set_ak('ak')
    visual_service.set_sk('sk')
    # visual_service.set_host('host')

    params = dict()

    form = {
        "image_base64": "image_base64_str"
    }

    resp = visual_service.bank_card(form)
    print(resp)

```

运行代码方式，在根目录下执行

```bash
python volcengine/example/visual/example_bank_card.py
```

## 接口文档
文档链接请点击[这里](https://www.volcengine.cn/docs)
并在【视觉智能】列表查看

