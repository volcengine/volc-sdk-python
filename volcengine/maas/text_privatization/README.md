
欢迎使用火山方舟的文本隐私化功能。

在使用大模型精调服务时，直接上传私域训练数据存在一定的隐私泄露风险。
针对这一问题，本功能主要采用本地差分隐私技术，在用户本地对用于大模型精调的训练数据进行扰动，加强了对用户数据隐私的保护。
目前本功能仅支持文本分类任务，采用基于词元贡献度衡量的动态隐私预算分配机制，实现了更好的效用隐私权衡。

相关研究论文：[基于分割学习的“分割-隐私化”大语言模型精调框架](https://mp.weixin.qq.com/s/IuIY-QBOpl7_FDZCriVSjw)

以下为您介绍如何使用文本隐私化功能。

## 获取与安装
建议使用不低于3.7的Python版本。
1. 使用pip安装SDK for Python：
```
    pip install --user volcengine
```
如果已经安装volcengine包，则用下面命令升级即可：
```
    pip install --upgrade volcengine
```

2. 使用pip安装依赖包：
```
    pip install numpy typing_extensions sentencepiece torch~=1.13 transformers~=4.30
```

## 使用方式

1. 准备文本隐私化过程中需要用到的分词器tokenizer以及嵌入模型embedding model。
可以选择使用`get_bottom_model`方法从hugging face获取某个开源预训练模型的tokenizer以及embedding模块。
```python
from volcengine.maas.text_privatization import get_bottom_model

your_tokenizer, your_embedding_model = get_bottom_model(model_id="MODEL_ID")
```
2. 使用`make_privatizer`方法初始化文本隐私化器，其中`priv_level`参数表示隐私保护水平，分为"1","2","3"三档。
3. 使用`load_tokenizer_embedding`方法指定所用的tokenizer以及embedding model。
4. 给定训练数据路径，使用`fit`方法执行文本隐私化。数据格式要求符合[火山方舟大模型精调数据集格式](https://www.volcengine.com/docs/82379/1099461)。
3. 使用`save`方法保存隐私化结果，格式不变。

```python
from volcengine.maas.text_privatization import ClsPrivConf
from volcengine.maas.text_privatization import make_privatizer

text_privatizer = make_privatizer(task_type="classification", priv_conf=ClsPrivConf(priv_level="3"))
text_privatizer.load_tokenizer_embedding(tokenizer=your_tokenizer, embedding_model=your_embedding_model)
text_privatizer.fit(train_path="PATH/TO/DATA.jsonl")
text_privatizer.save(out_dir="PATH/TO/SAVE")
```




