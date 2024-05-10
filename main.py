from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from sougou import Sougou  # 假设你的Sougou类在Sougou.py文件里

app = FastAPI()

class Item(BaseModel):
    query: str

@app.post("/sougou/search")
async def run_sougou(item: Item):
    return Sougou.run(item.query)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9997)