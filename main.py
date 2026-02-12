import os
import sys
import json
import subprocess

# --- PROTOCOLO DE AUTO-REPARO DO GOD DEV ---
def install_dependencies():
    try:
        import flask
        import flask_cors
    except ImportError:
        print("Soberano, detectei ausência de bibliotecas. Iniciando reparo imediato...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask", "flask-cors"])
        print("Reparo concluído. Reinicie o script.")
        sys.exit()

install_dependencies()

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DB_FILE = 'links_sagrados.json'

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_db(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

# --- INTERFACE DE ALTA TECNOLOGIA ---
HTML_PAGE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>GOD DEV | Vault</title>
    <style>
        :root { --bg: #050505; --acc: #00ff41; --surf: #111; --txt: #fff; }
        body { background: var(--bg); color: var(--txt); font-family: 'Consolas', monospace; padding: 40px; }
        .container { max-width: 900px; margin: auto; }
        header { border-bottom: 2px solid var(--acc); padding-bottom: 10px; margin-bottom: 30px; }
        .input-box { display: grid; grid-template-columns: 1fr 2fr auto; gap: 10px; background: var(--surf); padding: 20px; border-radius: 4px; }
        input { background: #000; border: 1px solid #333; padding: 12px; color: var(--acc); outline: none; }
        button { background: var(--acc); color: #000; border: none; padding: 12px 25px; font-weight: bold; cursor: pointer; transition: 0.3s; }
        button:hover { box-shadow: 0 0 15px var(--acc); }
        .grid { display: grid; gap: 10px; margin-top: 30px; }
        .item { background: var(--surf); padding: 20px; display: flex; justify-content: space-between; align-items: center; border-left: 4px solid var(--acc); }
        .item a { color: var(--txt); text-decoration: none; font-size: 1.1rem; }
        .item a:hover { color: var(--acc); }
        .del { color: #ff4444; cursor: pointer; background: none; border: none; font-size: 1.5rem; }
    </style>
</head>
<body>
    <div class="container">
        <header><h1>SYSTEM: LINK_VAULT</h1></header>
        <div class="input-box">
            <input type="text" id="t" placeholder="Identificador">
            <input type="text" id="u" placeholder="URL (https://...)">
            <button onclick="add()">ARMAZENAR</button>
        </div>
        <div id="list" class="grid"></div>
    </div>
    <script>
        async function load() {
            const r = await fetch('/api/links');
            const data = await r.json();
            document.getElementById('list').innerHTML = data.map(l => `
                <div class="item">
                    <a href="${l.url}" target="_blank"><strong>${l.title}</strong> - <small>${l.url}</small></a>
                    <button class="del" onclick="del('${l.id}')">×</button>
                </div>
            `).join('');
        }
        async function add() {
            const t = document.getElementById('t').value;
            const u = document.getElementById('u').value;
            if(!u) return;
            await fetch('/api/links', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({title: t || 'Link', url: u})
            });
            document.getElementById('t').value = '';
            document.getElementById('u').value = '';
            load();
        }
        async function del(id) {
            await fetch(`/api/links/${id}`, { method: 'DELETE' });
            load();
        }
        load();
    </script>
</body>
</html>
"""

@app.route('/')
def index(): return render_template_string(HTML_PAGE)

@app.route('/api/links', methods=['GET'])
def get_l(): return jsonify(load_db())

@app.route('/api/links', methods=['POST'])
def post_l():
    db = load_db()
    item = {"id": str(len(db) + 1), "title": request.json['title'], "url": request.json['url']}
    db.append(item)
    save_db(db)
    return jsonify(item)

@app.route('/api/links/<id>', methods=['DELETE'])
def del_l(id):
    db = [l for l in load_db() if l['id'] != id]
    save_db(db)
    return '', 204

if __name__ == '__main__':
    print("O Vault está pronto. Acesse: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)