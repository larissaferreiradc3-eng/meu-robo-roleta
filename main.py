import time
import requests
import re
import os
import threading
from flask import Flask, request, render_template_string
from supabase import create_client

app = Flask(__name__)

# --- CONFIGURAÇÕES DO BANCO ---
URL_SB = "https://tpotbyekboefgcbgmckp.supabase.co"
KEY_SB = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRwb3RieWVrYm9lZmdjYmdtY2twIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjY4MDc1NjgsImV4cCI6MjA4MjM4MzU2OH0.rlZzMH0EWY54gk9MNolp_KTC2DYFxkb3P7KtPw_aYWw"
supabase = create_client(URL_SB, KEY_SB)

# Link inicial (o que está funcionando agora)
CONFIG = {
    "url_api": "https://games.pragmaticplaylive.net/api/ui/statisticHistory?tableId=mrbras531mrbr532&numberOfGames=500&JSESSIONID=fiJhDiTJWvpKU3-BGSjgJuBLrtPyftVUGcIXse9CH0ht1QvSrUrp!1013244236-a9489409&ck=1766859862010&game_mode=roulette_desktop",
    "status": "Iniciando monitoramento...",
    "ultimo_id": None
}

# --- PAINEL DE CONTROLE (O que você verá no navegador) ---
HTML_PAINEL = '''
<!DOCTYPE html>
<html>
<head>
    <title>ROBÔ ROLETA PRO</title>
    <style>
        body { font-family: sans-serif; text-align: center; background: #0f172a; color: white; padding-top: 50px; }
        .card { background: #1e293b; padding: 30px; border-radius: 15px; display: inline-block; width: 90%; max-width: 500px; border: 1px solid #334155; }
        .status { font-size: 1.2em; color: #10b981; margin-bottom: 20px; border: 1px solid #10b981; padding: 10px; border-radius: 5px; }
        input { width: 90%; padding: 12px; margin: 15px 0; border-radius: 5px; border: none; }
        button { background: #3b82f6; color: white; border: none; padding: 12px 25px; border-radius: 5px; cursor: pointer; font-weight: bold; width: 100%; }
        button:hover { background: #2563eb; }
    </style>
</head>
<body>
    <div class="card">
        <h2>🚀 Status do Robô</h2>
        <div class="status">{{ status }}</div>
        <form method="POST">
            <p>Se o robô parar, cole o novo link 'statisticHistory' abaixo:</p>
            <input type="text" name="link" placeholder="https://games.pragmaticplaylive.net/..." required>
            <button type="submit">ATUALIZAR CONEXÃO</button>
        </form>
        <p style="font-size: 0.8em; color: #64748b; margin-top: 20px;">Versão 12.3 - Estável</p>
    </div>
</body>
</html>
'''

def extrair_numero(texto):
    match = re.search(r'(\d+)', str(texto))
    return match.group(1) if match else None

def monitorar():
    headers = {"User-Agent": "Mozilla/5.0"}
    while True:
        try:
            res = requests.get(CONFIG["url_api"], headers=headers, timeout=10)
            if res.status_code == 200:
                dados = res.json().get('history', [])
                if dados:
                    recente = dados[0]
                    game_id = recente.get('gameId')
                    
                    if game_id != CONFIG["ultimo_id"]:
                        num = extrair_numero(recente.get('gameResult'))
                        if num:
                            supabase.table("resultados_roleta").insert({
                                "numero": str(num), 
                                "contato": str(game_id)
                            }).execute()
                            CONFIG["ultimo_id"] = game_id
                            CONFIG["status"] = f"🟢 ONLINE - Último número salvo: {num}"
            elif res.status_code == 401:
                CONFIG["status"] = "🔴 LINK EXPIROU - Atualize no painel"
        except:
            CONFIG["status"] = "🟡 Tentando reconectar..."
        
        time.sleep(3) # Checagem a cada 3 segundos (Rápido e Seguro)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        novo_link = request.form.get('link')
        if "JSESSIONID" in novo_link:
            CONFIG["url_api"] = novo_link
            CONFIG["ultimo_id"] = None
            CONFIG["status"] = "♻️ Reiniciando com novo link..."
    return render_template_string(HTML_PAINEL, status=CONFIG["status"])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
