from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from slinkieforumsserver import routes

import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router)

def main():
    uvicorn.run(app, host="localhost", port=8000)
    from slinkieforumsserver import api, database

if __name__ == "__main__": main()