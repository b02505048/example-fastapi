from fastapi import FastAPI, Request, HTTPException
from .routers import server_info

server = FastAPI()
server.include_router(server_info.router)

