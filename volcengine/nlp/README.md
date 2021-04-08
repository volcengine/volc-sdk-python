## Example

调用代码示例均在`volcengine/example/nlp`文件夹下，以下为文本情感分析调用示例

```python
#  -*- coding: utf-8 -*-
from __future__ import print_function

from volcengine.nlp.NLPService import NLPService

if __name__ == '__main__':
    nlp_service = NLPService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    nlp_service.set_ak('ak')
    nlp_service.set_sk('sk')

    params = dict()

    form = {
        "text": "我很生气"
    }

    resp = nlp_service.sentiment_analysis(form)
    print(resp)

```

运行代码方式，在根目录下执行

```bash
python volcengine/example/nlp/example_sentiment_analysis.py
```