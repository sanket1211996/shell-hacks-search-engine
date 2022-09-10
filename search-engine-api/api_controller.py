import uvicorn
from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response

app = FastAPI()

origins = ["*"]

middleware = [Middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], )
]

app = FastAPI(middleware=middleware)


async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception:
        return Response("Internal server error", status_code=505)


app.middleware('http')(catch_exceptions_middleware)


@app.get("/search-api")
async def search_api(search_text):
    search_service = SearchService()
    return search_service.filterData(search_text)



def setup():
    print('welcome to search engine api')
    uvicorn.run(app, host="0.0.0.0", port=4600)



if __name__ == '__main__':
    setup()