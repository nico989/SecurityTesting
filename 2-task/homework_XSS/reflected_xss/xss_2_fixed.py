from flask import Flask, request
from html import escape
app = Flask(__name__)

@app.route("/hello")
def hello():
    name = request.args.get('name')
    content = """
    <html>
        <head><title>Internet knows</title></head>
        <body>
            Would you like to know what internet thinks about you? Visit this <a href="https://www.bing.com/search?q={}" attribute="aaa">Link</a>
        </body>
    </html>
    """.format(escape(name))
    return content

if __name__ == "__main__":
    app.run()
