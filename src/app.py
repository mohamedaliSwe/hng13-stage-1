from decouple import config
from fastapi import FastAPI
from src.routes.route import router


app = FastAPI(title="String Analyzer",
              description="A RESTful API service that analyzes strings and stores their computed properties."
              )


app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    port = int(config("PORT", 8000))
    uvicorn.run("src.app:app", host="0.0.0.0", port=port)
