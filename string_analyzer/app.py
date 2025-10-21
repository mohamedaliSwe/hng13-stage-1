from fastapi import FastAPI
from .routes import route


app = FastAPI(title="String Analyzer",
              description="A RESTful API service that analyzes strings and stores their computed properties."
              )


app.include_router(route.router)
