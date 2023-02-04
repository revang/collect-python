from flask import Flask, request
import re

app = Flask(__name__)


@app.route('/')
def index():
    return '''
        <form method="post">
          <textarea name="text"></textarea>
          <br>
          <button type="submit">Submit</button>
        </form>
    '''


@app.route('/', methods=['POST'])
def word_count():
    text = request.form['text']
    words = re.findall(r'\w+', text)
    return f"Word count: {len(words)}"


if __name__ == '__main__':
    app.run()
