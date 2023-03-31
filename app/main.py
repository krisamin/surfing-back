# clast/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine
from app.middlewares.access_logging import AccessLoggingMiddleware

# Init app
app = FastAPI()

app.add_middleware(AccessLoggingMiddleware)


origins = [
    "https://surfing.dimigo.in"
    "https://surfing.2w.vc"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def create_all_table():
    from app.models import user_model, refresh_token_model, submit_model, circle_model, period_model, circle_admin_model
    user_model.Base.metadata.create_all(bind=engine)
    refresh_token_model.Base.metadata.create_all(bind=engine)
    submit_model.Base.metadata.create_all(bind=engine)
    circle_model.Base.metadata.create_all(bind=engine)
    period_model.Base.metadata.create_all(bind=engine)
    circle_admin_model.Base.metadata.create_all(bind=engine)

create_all_table()


from app.apis import auth_api, submit_api, period_api, circle_admin_api
app.include_router(auth_api.router)
app.include_router(submit_api.router)
app.include_router(period_api.router)
app.include_router(circle_admin_api.router)

@app.get("/")
def read_root():
    return {"result": "Good to Go"} 
