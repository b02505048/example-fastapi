from fastapi import Header, HTTPException

async def verify_jwt(access_token:str=Header(None)):
  print(access_token)
  if access_token is None:
    raise HTTPException(status_code=400, detail="Unauthorized Access: Access-Token invalid")
  
  # Check the access_token