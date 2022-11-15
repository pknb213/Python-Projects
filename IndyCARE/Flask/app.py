import sys, os
sys.path.append(os.getcwd() + os.path.sep + 'python')
from utils import *
from apis import *

if __name__ == '__main__':
    app.run(threaded=True, host="0.0.0.0", port=4000)
    sess.init_app(app)






