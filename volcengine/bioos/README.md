## Example

调用代码示例均在`volcengine/example/bioos`文件夹下

运行代码方式为在根目录下执行

```bash
python volcengine/example/bioos/example_xxx_xxx.py
```

## Sphinx文档
在**volcengine/bioos/doc**目录下执行下列命令生成html文件
```bash
make html
```
接着进入生成的build/html目录执行下列命令启动服务
```bash
python -m http.server ${port}
```
最后在偏好的浏览器中输入`127.0.0.1:${port}`查看文档

## 接口文档
文档链接请点击[这里](https://www.volcengine.com/docs/6971)
