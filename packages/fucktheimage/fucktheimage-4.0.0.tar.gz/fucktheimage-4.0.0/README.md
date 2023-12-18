### 介绍

fucktheimage是一个基于SunPics开发的免费图床库，可以上传图片并获取图片链接。
fucktheimage is a free image hosting library based on SunPics. It allows users to upload images and obtain the corresponding image links.

### 安装

使用以下命令通过pip安装图床库：

```
pip install fucktheimage
```

### 示例

以下是使用图床库上传图片并获取图片链接的简单示例：

```python
from fucktheimage import upload

file_path = input("请输入文件名或目录：")
image_url = upload.upload_image(file_path)

if image_url:
    print("上传成功")
    print("图片链接：" + image_url)
else:
    print("上传失败")
```

这段代码示例通过调用`upload_image`函数上传图片，并打印出上传结果和图片链接。