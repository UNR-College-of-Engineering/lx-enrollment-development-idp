import uvicorn
import logging

from typing import Annotated
from fastapi import FastAPI, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
app = FastAPI()

from starlette.config import Config
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.cors import CORSMiddleware
from authlib.integrations.starlette_client import OAuth, OAuthError

import database as db

logger = logging.getLogger(__name__)

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')

templates = Jinja2Templates(directory='templates')
app.mount('/static', StaticFiles(directory='static'), name='static')

logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

from config import settings

app.add_middleware(SessionMiddleware, secret_key=settings.MIDDLEWARE_SECRET)

origins = [
    "http://localhost:8000",
    "http://localhost:8000/*",
    "http://127.0.0.1:8000/*",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

config = Config('keycloak.env')
oauth = OAuth(config)

CONF_URL = 'https://idp.nevada.dev/realms/NSHE/.well-known/openid-configuration'
oauth.register(
    name='keycloak',
    client_id=settings.CLIENT_ID,
    client_secret=settings.CLIENT_SECRET.get_secret_value(),
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'profile email',
    }
)

show_auth = True
selected_class = ""

@app.route('/login')
async def login(request: Request):
    redirect_uri = request.url_for('auth')
    return await oauth.keycloak.authorize_redirect(request, redirect_uri)

@app.route('/auth')
async def auth(request: Request):
    try:
        token = await oauth.keycloak.authorize_access_token(request)
    except OAuthError as error:
        return templates.TemplateResponse('error.html', {'request': request, 'error': error})
    user = token.get('userinfo')
    if user:
        request.session['user'] = dict(user)
    return templates.TemplateResponse('home.html', {'request': request, 'user': user})

@app.get('/success')
async def private(request: Request):
    user = request.session.get('user')
    if user:
        return templates.TemplateResponse('success.html', {'request': request, 'user': user})
    else:
        return RedirectResponse(url='/error')

@app.get('/error')
async def error():
    return {'result': 'This is a error endpoint.'}

@app.get('/')
async def public(request: Request):
    user = request.session.get('user')
    show_auth = user is None
    if user is not None and selected_class != "":
        return RedirectResponse(url='/success')
    return templates.TemplateResponse('home.html', {'request': request, 'show_auth': show_auth})

@app.post('/submit')
async def public(request: Request, selected_class: Annotated[str, Form()]):
    user = request.session.get('user')

    complete = selected_class != "" and user is not None
    if complete:
        inserted = db.insertUser(str(user['preferred_username']), str(selected_class))
        if inserted:
            return templates.TemplateResponse('success.html', {'request': request, 'user': user})
        else:
            already = True
            return templates.TemplateResponse('success.html', {'request': request, 'user': user, 'already': already})
    else:
        return templates.TemplateResponse('home.html', {'request': request, 'selected_class': selected_class, 'complete': complete, 'show_auth': show_auth})

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
