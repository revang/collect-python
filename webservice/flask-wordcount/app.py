import re
from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def index():
    return '''
        <div style="display: flex;">
            <form method="post" style="width: 50%; margin-block-end: 0em">
              <textarea name="text" style="width: 100%; height:800px;"></textarea>
            </form>
            <textarea id="result" style="width: 50%;"></textarea>
        </div>

        <script>
            const textarea = document.querySelector('textarea[name="text"]');
            const result = document.querySelector('#result');
            textarea.addEventListener('input', function() {
                const xhr = new XMLHttpRequest();
                xhr.open('POST', '/', true);
                xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                xhr.onreadystatechange = function() {
                    if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
                        result.value = xhr.responseText;
                    }
                };
                xhr.send(encodeURI(`text=${textarea.value}`));
            });
        </script>
    '''


@app.route('/', methods=['POST'])
def word_count():
    text = request.form['text']
    words = re.findall(r'\w+', text)
    return f"Word count: {len(words)}"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
