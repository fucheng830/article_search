# 搜狗微信文章搜索API

这是一个基于FastAPI的微服务，可以调用搜狗搜索接口，搜索微信公众号文章。

## 主要功能

- 提供了一个POST请求的接口，接受一个查询字符串作为参数，返回搜狗微信搜索的结果。

## 使用方法

1. 安装所需的Python库：`pip install fastapi uvicorn requests lxml html2text`
2. 运行程序：`python main.py`
3. 服务将在 `http://0.0.0.0:9997` 启动，你可以通过POST请求到 `/sougou/search` 来搜索文章。请求体应该是一个JSON对象，如下：
```json
{
    "query": "你的搜索关键词"
}
```

## 项目链接

- 英文版README：[README in English](./README_EN.md)





