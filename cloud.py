from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

sudokuapi =  "https://you-do-sudoku-api.vercel.app/api"

@app.route('/', methods=['GET'])
def index():
    response = requests.get(sudokuapi)
    if response.status_code == 200:
        data = response.json()
        return jsonify({"difficulty": data.get("difficulty"), "puzzle": data.get("puzzle")})
    else:
        return f"Error: {response.status_code}", response.status_code

@app.route('/solution', methods=['GET'])
def solution():
    response = requests.get(sudokuapi)
    if response.status_code == 200:
        data = response.json()
        return jsonify({"solution": data.get("solution")})
    else:
        return f"Error: {response.status_code}", response.status_code

# di q sure kung gagana na to
@app.route('/generate_sudoku', methods=['POST'])
def generate_sudoku():
    difficulty = request.json.get('difficulty', 'easy')
    solution = request.json.get('solution', True)
    array = request.json.get('array', False)
    
    body = {
        "difficulty": difficulty,
        "solution": solution,
        "array": array
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(sudokuapi, json=body, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return jsonify(data)
    else:
        return f"Error: {response.status_code}", response.status_code




quoteapi = "http://api.forismatic.com/api/1.0/"

@app.route('/quote', methods=['GET'])
def quote():
    params = {
        'method': 'getQuote',
        'format': 'json',
        'lang': 'en'
    }
    response = requests.get(quoteapi, params=params)
    if response.status_code == 200:
        data = response.json()
        quote = data['quoteText']
        author = data['quoteAuthor']
        return jsonify({'quote': quote, 'author': author})
    else:
        return jsonify({'error': 'Failed to retrieve quote'})

@app.route('/new_quote', methods=['GET'])
def new_quote():
    params = {
        'method': 'getQuote',
        'format': 'json',
        'lang': 'en'
    }
    response = requests.get(quoteapi, params=params)  # Make sure it's the correct API
    if response.status_code == 200:
        data = response.json()
        quote = data['quoteText']
        author = data['quoteAuthor']
        return jsonify({'quote': quote, 'author': author})
    else:
        return jsonify({'error': 'Failed to retrieve quote'})

@app.route('/quote_russian', methods=['GET'])
def quote_russian():
    params = {
        'method': 'getQuote',
        'format': 'json',
        'lang': 'ru'  # Russian language code
    }
    response = requests.get(quoteapi, params=params)
    if response.status_code == 200:
        data = response.json()
        quote = data['quoteText']
        author = data['quoteAuthor']
        return jsonify({'quote': quote, 'author': author})
    else:
        return jsonify({'error': 'Failed to retrieve quote'})


if __name__ == '__main__':
    app.run(debug=True)
