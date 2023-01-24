from fastapi import APIRouter, Depends, Request
from classes.custom_response import Response
from app.auth import verify_jwt
import platform

router = APIRouter()


@router.get("/server_info", dependencies=[Depends(verify_jwt)])
def get_server_info():
  resp = Response()
  try:
    server_info = {
      "os": platform.system(),
      "cpu": platform.processor()
    }
    resp.set_payload(server_info)
  
  except Exception as err:
    # Unknown error handling
    resp.set_error(code=5001, message=err)
    
  finally:
    return resp.send()


@router.get("/health_check")
def health_check():
  resp = Response()
  try:
    print("Health Checking...")
    resp.set_payload({"status": "ok"})

  except Exception as err:
    # Unknown error handling
    resp.set_error(code=5001, message=err)
    
  finally:
    return resp.send()