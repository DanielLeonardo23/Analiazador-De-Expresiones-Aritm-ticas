from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from modules.parser import Parser

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-syntax-tree', methods=['POST'])
def generate_syntax_tree():
    data = request.json
    expression = data['expression']
    parser = Parser([])
    base64_image = parser.draw_syntax_tree(expression)
    if base64_image:
        return jsonify({"success": True, "image": base64_image})
    else:
        return jsonify({"success": False})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
