from fastapi import FastAPI
from routes.route import router


app = FastAPI(title="String Analyzer",
              description="A RESTful API service that analyzes strings and stores their computed properties."
              )


app.include_router(router)
