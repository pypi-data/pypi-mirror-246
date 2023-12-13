import uvicorn
import os
from .api import app

if __name__=="__main__":
    uvicorn.run(app,port = 5000)




