from app import app

from .homeView import homeBp
from .contextView import contextBp

app.register_blueprint(homeBp)
app.register_blueprint(contextBp)