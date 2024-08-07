from flask import Blueprint
from flask_cors import CORS

module = Blueprint('azon_api', __name__, url_prefix='/azon_api')

# register cors, because that api only for ajax from javascript
CORS(module, origins=['https://azon-azjx.onrender.com', 'https://example.com'])

from app.api.azon_api import cart, item, errors
