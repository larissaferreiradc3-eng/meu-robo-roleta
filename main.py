import time
import requests
import re
import os
import threading
from flask import Flask, request, render_template_string
from supabase import create_client

app = Flask(__name__)

# --- CONFIGURAÇÕES DO BANCO ---
URL_SB = "https://stsqpalmjeybdxeodexo.supabase.co"
KEY_SB = "sb_secret_PFcBWZuXAGbUcfZiYsnmRg_x4OBmWB8"
supabase = create_client(URL_SB, KEY_SB)

# Variável global para o link (começa com o seu atual)
CONFIG = {
    "url_api": "https://games.pragmaticplaylive.net/api/ui/statisticHistory?tableId=mrbras531mrbr532&numberOfGames=500&JSESSIONID=OSBg5G4sGAKXfy6-RTD5KAKUIt6xLHqbb_f53t75pmwMq_hv8Vba!-472946834-adaccecb&ck=1766857116400&game_mode=roulette_desktop",
    "status": "Iniciando..."
}

# --- INTERFACE VISUAL (PAINEL) ---
HTML_PAINEL = '''
<!DOCTYPE html>
<html>
<head>
    <title>Painel do Robô</title>
    <style>
        body { font-family: sans-serif; text-align: center; padding: 50px; background: #f4f4f9; }
        .card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); display: inline-block; width: 80%; max-width: 600px; }
        input { width: 90%; padding: 10px; margin: 10px 0; border: 1px solid #ccc; border-radius: 5px; }
        button { background: #28a745; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; }
        .status { color: #555; font-weight: bold; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="card">
        <h2>🚀 Monitor de Roleta Pro</h2>
        <p>Status: <span class="status">{{ status }}</span></p>
        <form method="POST">
            <p>Cole o novo link da API abaixo:</p>
            <input type="text" name="novo_link" placeholder="https://games.pragmaticplaylive.net/api/ui/statisticHistory..." required>
            <br>
            <button type="submit">Atualizar Robô</button>
        </form>
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        novo_link = request.form.get('novo_link')
        if "JSESSIONID=" in novo_link:
            CONFIG["url_api"] = novo_link
            CONFIG["status"] = "Link Atualizado! Monitorando..."
        else:
            CONFIG["status"] = "Erro: Link inválido!"
    return render_template_string(HTML_PAINEL, status=CONFIG["status"])

# --- LÓGICA DO MONITOR ---
def extrair_numero(texto):
    match = re.search(r'(\d+)', str(texto))
    return match.group(1) if match else None

def monitorar():
    ultimo_id = None
    while True:
        try:
            response = requests.get(CONFIG["url_api"], timeout=10)
            if response.status_code == 200:
                CONFIG["status"] = "Rodando e Coletando..."
                dados = response.json().get('history', [])
                if dados:
                    recente = dados[0]
                    game_id = recente.get('gameId')
                    if game_id != ultimo_id:
                        numero = extrair_numero(recente.get('gameResult'))
                        if numero:
                            supabase.table("resultados_roleta").insert({"numero": str(numero), "contato": str(game_id)}).execute()
                            ultimo_id = game_id
            elif response.status_code == 401:
                CONFIG["status"] = "🔴 SESSÃO EXPIROU! Cole um novo link."
        except Exception as e:
            CONFIG["status"] = f"Erro: {str(e)[:50]}"
        time.sleep(5)

# Inicia o monitor em segundo plano
threading.Thread(target=monitorar, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
