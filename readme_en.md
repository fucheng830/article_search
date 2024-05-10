# Sogou WeChat Article Search API

This is a microservice based on FastAPI, which can call the Sogou search interface to search for WeChat Official Account articles.

## Main Features

- Provides a POST request interface, accepts a query string as a parameter, and returns the results of Sogou WeChat search.

## How to Use

1. Install the required Python libraries: `pip install fastapi uvicorn requests lxml html2text`
2. Run the program: `python main.py`
3. The service will be launched at `http://0.0.0.0:9997`, you can search for articles by sending a POST request to `/sougou/search`. The request body should be a JSON object, like this:
```json
{
    "query": "your search keywords"
}
```

## Project Links

- [README in Chinese](./README.md)