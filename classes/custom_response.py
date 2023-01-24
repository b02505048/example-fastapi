from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse


error_codes = {
  4001: {
    "status_code": 400,
    "error_type": "Bad Request"
  },

  4011: {
    "status_code": 401,
    "error_type": "Unauthorized"
  },

  4031: {
    "status_code": 403,
    "error_type": "Access Denied"
  },

  4041: {
    "status_code": 404,
    "error_type": "Not Found"
  },

  4091: {
    "status_code": 409,
    "error_type": "Duplicated"
  },

  4291: {
    "status_code": 429,
    "error_type": "Too Many Request"
  },

  5001: {
    "status_code": 500,
    "error_type": "Unexpected Error"
  }
}

class Response():

  def __init__(self, code:int=2001, result:dict={}):
    # Check the response code
    if self.__code_verifier__(code=code) is False:
      raise Exception("Invalid response code.")

    self.req_id = str(uuid4())
    self.content = {
      "code": int(code),
      "result": result,
      "req_id": self.req_id
    }
    self.status_code = 200

  
  def __code_verifier__(self, code:int):
    try:
      code = int(code)
      if code != 2001 and code not in error_codes.keys():
        raise Exception()
      
      return True
    except Exception as err:
      return False


  # Error 500
  class Error500(BaseModel):
    code:int=5001
    has_error:bool=True
    message:str="Unexpected Error"
    req_id:UUID=Field(default_factory=uuid4)


  # Error 400
  class Error400(BaseModel):
    code:int=4001
    has_error:bool=True
    req_id:UUID=Field(default_factory=uuid4)
    message:str="Bad Request"


  def send(self) -> JSONResponse:
    return JSONResponse(status_code=self.status_code, content=self.content)


  def set_error(self, code:int=5001, message:str="") -> None:
    """This function will set the error response following our predefined
    standard.

    Args:
      code (int, optional): The error code which is listed on our predefined
          standard. Defaults to 5001.
      message (str, optional): The error message we want to let user knows.
          Defaults to "".

    Returns:
      None
    """
    # Check the response code
    if self.__code_verifier__(code=code) is False:
      raise Exception("Invalid response code.")

    # Initialize the args
    code = int(code)
    message = str(message)

    self.content = {
      "code": int(code),
      "has_error": True,
      "req_id": self.req_id
    }

    # Lookup the error codes
    status_code = error_codes.get(code).get("status_code", 500)
    error_type = error_codes.get(code).get("error_type", "Unexpected Error")

    # Append the error message if provided
    if not message:
      self.content["message"] = error_type
    else:
      self.content["message"] = f"{error_type}: {message}"

    # Overwrite the status code
    self.status_code = status_code


  def set_payload(self, payload) -> None:
    """This function will set the error response following our predefined
    standard.

    Args:
      payload (*): The result of the API response return to user.

    Returns:
      None
    """
    # print(f"WHAT?! {payload}")
    # if isinstance(payload, list) or isinstance(payload, tuple):
    #   self.content["result"] = {"list": payload}
    # elif isinstance(payload, str):
    #   self.content["result"] = {"text": payload}
    # else:
    self.content["result"] = payload

    