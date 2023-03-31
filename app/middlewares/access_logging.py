# clast/app/middlewares/clast_logging.py

import time
import json
import datetime 
import logging
from app.utils import logger

from fastapi import HTTPException
from fastapi.requests import Request
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

# Logger setup
access_logger = logger.generate_logger("Access", logging.INFO, '/log/access.log')

# Access log middleware
class AccessLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        time_format: str = "%Y/%m/%d %H:%M:%S"
        start_time: float = time.time()

        response: Response = await call_next(request) # run request processing

        status_code: int = response.status_code
        process_time: float = (time.time() - start_time) * 1000
        formatted_process_time: str = '{0:.2f}'.format(process_time)
        try:
            log_dict = dict(
                uri=request.url.path,
                method=str(request.method),
                status_code=str(status_code),
                datetimeUTC=datetime.datetime.utcnow().strftime(time_format),
                datetimeKR=(datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime(time_format),
                processedTime=formatted_process_time+"ms",
                
            )
        except KeyError:
            raise HTTPException(status_code=400, detail="Invalid request")
        access_logger.info(json.dumps(log_dict))
        
        return response
