# inference.py
import torch
from fastapi import FastAPI
import uvicorn

app = FastAPI()

# Suppose we load our saved model here
# model = ...

@app.get("/recommend/{user_id}")
def recommend(user_id: int, top_k: int = 10):
    # 1. Gather candidate items (may be all items or a filtered subset).
    # 2. Score each item using the model.
    # 3. Sort by predicted score.
    # 4. Return top_k items.
    return {"user_id": user_id, "recommendations": []}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
