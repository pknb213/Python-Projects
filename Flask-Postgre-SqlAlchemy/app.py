from apps import create_app
from apps.utils.utils import JWTManager

app = create_app()
jwt = JWTManager(app)

from apps.views.routes import *

if __name__ == '__main__':
    app.run()
