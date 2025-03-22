from flask import Flask, jsonify, request
import requests
import base64

app = Flask(__name__)

sudokuapi =  "https://you-do-sudoku-api.vercel.app/api"


@app.route('/', methods=['GET'])
def index():
    responseSoduko = requests.get("https://cloud-prog.onrender.com/generate_sudoku_easy").json()
    content = responseSoduko['puzzle']
    solution = responseSoduko['solution']

    responseQuotes = requests.get("https://cloud-prog.onrender.com/today").json()
    contentQuotes = responseQuotes['quote']
    author = responseQuotes['author']
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sudoku Checker</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background-color: #f4f4f4;
            }}
            #sudoku-container {{
                display: grid;
                grid-template-columns: repeat(9, 40px);
                grid-template-rows: repeat(9, 40px);
                gap: 2px;
                background-color: #000;
                padding: 5px;
            }}
            input {{
                width: 40px;
                height: 40px;
                text-align: center;
                font-size: 18px;
                border: 1px solid #ccc;
            }}
            input[readonly] {{
                background-color: #ddd;
                font-weight: bold;
            }}
            #check-button, .level-button {{
                margin-top: 10px;
                padding: 10px 20px;
                font-size: 16px;
                cursor: pointer;
            }}
            #result {{
                margin-top: 10px;
                font-size: 18px;
            }}
            #quote {{
                margin-top: 20px;
                font-style: italic;
                font-size: 16px;
            }}
        </style>
    </head>
    <body>

    <div>
        <div id="spotify-container">
            <!-- Embed Spotify Player -->
            <iframe id="spotify-player"
                style="border-radius:12px"
                src="https://open.spotify.com/embed/track/0I2ugiLWhuMPSxpmEeRpZA?utm_source=generator"
                width="300" height="380" frameborder="0"
                allowfullscreen=""
                allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
                loading="lazy">
            </iframe>
        </div>
        <div>
            <button class="level-button" onclick="fetchSudoku('easy')">Easy</button>
            <button class="level-button" onclick="fetchSudoku('medium')">Medium</button>
            <button class="level-button" onclick="fetchSudoku('hard')">Hard</button>
        </div>
        <div id="sudoku-container"></div>
        <button id="check-button" onclick="checkSudoku()">Check Sudoku</button>
        <div id="result"></div>
        <div id="quote">📜 "{contentQuotes}" - {author}</div>
    </div>

    <div id="quote-modal" style="display:none; position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 60%; max-width: 400px; background-color: #fff; padding: 20px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); border-radius: 8px; z-index: 9999;">
        <h3 id="quote-text" style="font-size: 18px; margin-bottom: 10px;"></h3>
        <p id="quote-author" style="font-size: 14px; color: #555;"></p>
        <button onclick="closeModal()" style="margin-top: 10px; padding: 8px 16px; font-size: 14px; background-color: #ff4d4d; color: white; border: none; border-radius: 5px; cursor: pointer;">Close</button>
    </div>

    <script>
        let content = "{content}";
        let solution = "{solution}";

        function generateBoard(content) {{
            const container = document.getElementById('sudoku-container');
            container.innerHTML = '';
            
            for (let i = 0; i < content.length; i++) {{
                const cell = document.createElement('input');
                cell.type = 'text';
                cell.maxLength = 1;
                cell.value = content[i] === '0' ? '' : content[i];
                cell.dataset.index = i;

                if (content[i] !== '0') {{
                    cell.readOnly = true;
                }}

                if ((i % 9 === 2 || i % 9 === 5) && i % 9 !== 8) {{
                    cell.style.borderRight = '2px solid black';
                }}
                if ((i >= 18 && i < 27) || (i >= 45 && i < 54)) {{
                    cell.style.borderBottom = '2px solid black';
                }}

                cell.addEventListener('input', validateInput);
                container.appendChild(cell);
            }}
        }}

        function validateInput(event) {{
            const value = event.target.value;
            if (!/^[1-9]?$/.test(value)) {{
                event.target.value = '';
            }}
        }}

        function checkSudoku() {{
            const cells = document.querySelectorAll('input');
            let userSolution = '';
            
            cells.forEach(cell => {{
                userSolution += cell.value || '0';
            }});

            if (userSolution === solution) {{
                fetchNewQuote();
                document.getElementById('result').innerText = "✅ Correct! Sudoku solved.";
            }} else {{
                document.getElementById('result').innerText = "❌ Incorrect solution. Try again.";
            }}
        }}

        function fetchSudoku(level) {{
            fetch(`/generate_sudoku_${{level}}`)
                .then(response => response.json())
                .then(data => {{
                    content = data.puzzle;
                    solution = data.solution;
                    generateBoard(content);
                    document.getElementById('result').innerText = '';
                }})
                .catch(error => console.error('Error fetching Sudoku:', error));
        }}

        function fetchNewQuote() {{
        fetch(`/random`)
            .then(response => response.json())
            .then(data => {{
                const quote = data.quote;
                const author = data.author;

                document.getElementById('quote-text').innerText = `📜 "${{quote}}"`;
                document.getElementById('quote-author').innerText = `— ${{author}}`;
                document.getElementById('quote-modal').style.display = 'block';
            }})
            .catch(error => console.error('Error fetching quote:', error));
        }}

        function closeModal() {{
            document.getElementById('quote-modal').style.display = 'none';
            fetchSudoku('easy');
        }}

        generateBoard(content);
    </script>

    </body>
    </html>
    """

@app.route('/generate_sudoku_easy', methods=['GET'])
def generate_sudoku_easy():
    body = {
        "difficulty": 'easy',
        "solution": True,
        "array": False
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(sudokuapi, json=body, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return jsonify(data)
    else:
        return f"Error: {response.status_code}", response.status_code

@app.route('/generate_sudoku_medium', methods=['GET'])
def generate_sudoku_medium():
    body = {
        "difficulty": 'medium',
        "solution": True,
        "array": False
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(sudokuapi, json=body, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return jsonify(data)
    else:
        return f"Error: {response.status_code}", response.status_code
    
@app.route('/generate_sudoku_hard', methods=['GET'])
def generate_sudoku_hard():
    body = {
        "difficulty": 'hard',
        "solution": True,
        "array": False
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(sudokuapi, json=body, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return jsonify(data)
    else:
        return f"Error: {response.status_code}", response.status_code


#QUOTES
quoteapi = "https://zenquotes.io"

# shows the a random quote
@app.route('/quote', methods=['GET'])
def quote():
    response = requests.get(f"{quoteapi}/api/quotes")
    if response.status_code == 200:
        data = response.json()
        quote = data[0]['q']
        author = data[0]['a']
        return jsonify({'quote': quote, 'author': author})
    else:
        return jsonify({'error': 'Failed to retrieve quote'})

# shows the an famous technology quote
@app.route('/random', methods=['GET'])
def famous_tech_quotes():
    response = requests.get(f"{quoteapi}/api/random")
    if response.status_code == 200:
        data = response.json()
        quote = data[0]['q']
        author = data[0]['a']
        return jsonify({'quote': quote, 'author': author})
    else:
        return jsonify({'error': 'Failed to retrieve quote'})


# shows the a history quotes
@app.route('/today', methods=['GET'])
def history_quotes():
    response = requests.get(f"{quoteapi}/api/today")
    if response.status_code == 200:
        data = response.json()
        quote = data[0]['q']
        author = data[0]['a']
        return jsonify({'quote': quote, 'author': author})
    else:
        return jsonify({'error': 'Failed to retrieve quote'})
    


#SPOTIFY

spotifyapi = "https://api.spotify.com"
client_id = "806aedb8a563461695c179cb7bb2fafa"
client_secret = "336b8a4574f6456489c07a954a82bf7e"
redirect_uri = "https://www.github.com/Swa-ne"
access_token = ""


#gets the access token of spotify user
@app.route('/get_access_token', methods=['GET'])
def get_access_token():
    auth_str = f"{client_id}:{client_secret}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode('utf-8')

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f"Basic " + b64_auth_str
    }

    body = {
        'grant_type': 'client_credentials',
    }

    response = requests.post(f"https://accounts.spotify.com/api/token", data=body, headers=headers)

    if response.status_code == 200:
        data = response.json()
        global access_token 
        access_token = data['access_token']
        return jsonify(data)
    else:
        return f"Error: {response.status_code}", response.status_code

# gets the playlist of the current acces token user
@app.route('/get_playlist', methods=['GET'])
def get_playlist():
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer " + access_token}
    response = requests.get(f"https://api.spotify.com/v1/playlists/3cEYpjA9oz9GiPac4AsH4n", headers=headers)

    if response.status_code == 200:
        data = response.json()
        return jsonify(data)
    else:
        return f"Error: {response.status_code}", response.status_code

# searches a song
@app.route('/search_item', methods=['POST'])
def search_item():
    json = request.form
    search = json['search']
    headers = { "Authorization": f"Bearer " + access_token}
    response = requests.get(f'https://api.spotify.com/v1/search?q={search}&type=track&market=EN', headers=headers)

    if response.status_code == 200:
        data = response.json()
        return jsonify(data)
    else:
        return f"Error: {response.status_code}", response.status_code


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)
