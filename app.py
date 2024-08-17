from flask import Flask, request, jsonify
import pandas as pd
from werkzeug.utils import secure_filename
import os
from itsdangerous import URLSafeTimedSerializer
from cachelib.simple import SimpleCache
import functools
import sqlite3

# Configuração Inicial
SECRET_KEY = '123456ABCDEF'
serializer = URLSafeTimedSerializer(SECRET_KEY)

# Criar instância de cache
cache = SimpleCache()
app = Flask(__name__)

# Pasta de upload para salvar arquivos
UPLOAD_FOLDER = 'uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def generate_token(data, expiration=300):
    token = serializer.dumps(data)
    cache.set(token, data, timeout=expiration)
    return token

def validate_token(token):
    data = cache.get(token)
    if data is not None:
        return data
    return None

def token_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or ' ' not in auth_header:
            return jsonify({'error': 'Authorization header is missing or malformed'}), 401
        token = auth_header.split(' ')[1]
        data = validate_token(token)
        if not data:
            return jsonify({'error': 'Token is invalid'}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/token', methods=['POST'])
def token():
    data = request.json
    token = generate_token(data)
    return jsonify({'token': token}), 200

@app.route('/upload', methods=['POST'])
@token_required
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    f = request.files['file']

    if f.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if f.filename.endswith(".csv"):
        # Salvar o arquivo em um diretório seguro
        filename = secure_filename(f.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        f.save(file_path)
        
        # Ler o CSV usando Pandas
        df = pd.read_csv(file_path)
        
        # Converter para JSON e salvar
        jsonfilename = os.path.join(UPLOAD_FOLDER, filename.replace(".csv", ".json"))
        df.to_json(jsonfilename, orient='records')
        
        # Inserir os dados no banco de dados
        for row in df.itertuples(index=False, name=None):
            add_avaliacao(row[0], row[1], row[2], row[3], row[4])
        
        return jsonify(df.head().to_dict(orient='records')), 200
    else:
        return jsonify({'error': 'file is not csv'}), 400

def init_db():
    conn = sqlite3.connect('demo.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS
                    AVALIACOES (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        data TEXT NOT NULL,
                        quarto TEXT NOT NULL,
                        avaliacao TEXT NOT NULL,
                        nota INTEGER NOT NULL
                    )
                ''')
    conn.commit()
    conn.close()

def add_avaliacao(nome, data, quarto, avaliacao, nota):
    conn = sqlite3.connect('demo.db')
    c = conn.cursor()
    c.execute('''
                INSERT INTO 
                AVALIACOES (nome, data, quarto, avaliacao, nota)
                VALUES     (?, ?, ?, ?, ?)'''
                , (nome, data, quarto, avaliacao, nota))
    conn.commit()
    conn.close()

@app.route('/avaliacoes', methods=['GET'])
@token_required
def get_items():
    conn = sqlite3.connect('demo.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM AVALIACOES')
    items = c.fetchall()
    items_result = [dict(item) for item in items]
    conn.close()
    return jsonify(items_result), 200

# Inicializar o banco de dados na inicialização do aplicativo
init_db()

if __name__ == '__main__':
    app.run(debug=True)
