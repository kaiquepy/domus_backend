from fastapi import FastAPI

from domus_backend.routers import auth

app = FastAPI()

app.include_router(auth.router)


@app.get('/')
def read_root():
    return {'Message': 'Hello World!'}
