from fastapi import FastAPI, Request, HTTPException
from app.routers import server_info

server = FastAPI()
server.include_router(server_info.router)
