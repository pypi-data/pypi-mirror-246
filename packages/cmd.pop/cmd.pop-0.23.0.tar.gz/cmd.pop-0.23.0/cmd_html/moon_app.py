# %%file moon_app.py
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    # from google.colab.output import eval_js
    # # print(eval_js("google.colab.kernel.proxyPort(5000)"))
    # url = eval_js("google.colab.kernel.proxyPort(5000)")
    # print(url)
    # app.run(host=url,port=5000)
    # app.run(port=5000)
    app.run()