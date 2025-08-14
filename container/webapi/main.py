from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import logging

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPIアプリケーションの作成
app = FastAPI(
    title="WebAPI Service",
    description="FastAPI based web service",
    version="1.0.0",
    debug=True
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では適切に制限してください
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# データモデル
class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: float

class Response(BaseModel):
    message: str
    data: Optional[dict] = None

# サンプルデータ
items_db = [
    {"id": 1, "name": "Item 1", "description": "First item", "price": 100.0},
    {"id": 2, "name": "Item 2", "description": "Second item", "price": 200.0},
]

# ヘルスチェックエンドポイント
@app.get("/", response_model=Response)
async def root():
    logger.info("Root endpoint accessed")
    return Response(message="WebAPI Service is running!")

@app.get("/health", response_model=Response)
async def health_check():
    logger.info("Health check endpoint accessed")
    return Response(message="Service is healthy", data={"status": "ok"})

# アイテム関連のエンドポイント
@app.get("/items", response_model=List[Item])
async def get_items():
    logger.info("Getting all items")
    return items_db

@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    logger.info(f"Getting item with id: {item_id}")
    for item in items_db:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.post("/items", response_model=Item)
async def create_item(item: Item):
    logger.info(f"Creating new item: {item.name}")
    new_id = max([i["id"] for i in items_db]) + 1 if items_db else 1
    new_item = {"id": new_id, **item.dict()}
    items_db.append(new_item)
    return new_item

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item):
    logger.info(f"Updating item with id: {item_id}")
    for i, existing_item in enumerate(items_db):
        if existing_item["id"] == item_id:
            items_db[i] = {"id": item_id, **item.dict()}
            return items_db[i]
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}", response_model=Response)
async def delete_item(item_id: int):
    logger.info(f"Deleting item with id: {item_id}")
    for i, item in enumerate(items_db):
        if item["id"] == item_id:
            deleted_item = items_db.pop(i)
            return Response(message="Item deleted successfully", data=deleted_item)
    raise HTTPException(status_code=404, detail="Item not found")

# エラーハンドリング
@app.exception_handler(404)
async def not_found_handler(request, exc):
    logger.warning(f"404 error: {request.url}")
    return Response(message="Resource not found")

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    logger.error(f"500 error: {request.url} - {exc}")
    return Response(message="Internal server error")

if __name__ == "__main__":
    # 開発用設定（ホットリロード有効）
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,  # ホットリロード有効
        log_level="info",
        access_log=True
    )
