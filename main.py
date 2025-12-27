import time
import requests
import re
import os
import threading
from flask import Flask, render_template_string
from supabase import create_client

app = Flask(__name__)

# --- CONFIGURAÇÕES ---
URL_SB = "https://tpotbyekboefgcbgmckp.supabase.co"
KEY_SB = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRwb3RieWVrYm9lZmdjYmdtY2twIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjY4MDc1NjgsImV4cCI6MjA4MjM4MzU2OH0.rlZzMH0EWY54gk9MNolp_KTC2DYFxkb3P7KtPw_aYWw"
supabase = create_client(URL_SB, KEY_SB)

# Link da API (Use o mais recente que você pegou)
URL_API = "https://games.pragmaticplaylive.net/api/ui/statisticHistory?tableId=mrbras531mrbr532&numberOfGames=500&JSESSIONID=fiJhDiTJWvpKU3-BGSjgJuBLrtPyftVUGcIXse9CH0ht1QvSrUrp!1013244236-a9489409"

# Estado do Sistema
SISTEMA = {
    "ultimo_numero": "Aguardando...",
    "status": "Iniciando",
    "erros": 0
}

def monitorar_roleta():
    ultimo_id = None
    while True:
        try:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            res = requests.get(URL_API, headers=headers, timeout=8)
            
            if res.status_code == 200:
                SISTEMA["status"] = "🟢 Rodando 24h"
                historico = res.json().get('history', [])
                if historico:
                    recente = historico[0]
                    game_id = recente.get('gameId')
                    
                    if game_id != ultimo_id:
                        num = re.search(r'(\d+)', str(recente.get('gameResult'))).group(1)
                        # Salva no banco
                        supabase.table("resultados_roleta").insert({"numero": str(num), "contato": str(game_id)}).execute()
                        SISTEMA["ultimo_numero"] = num
                        ultimo_id = game_id
            
            elif res.status_code == 401:
                SISTEMA["status"] = "🔴 Sessão Expirada (Precisa de novo link)"
            
        except Exception:
            SISTEMA["status"] = "🟡 Falha na conexão... tentando de novo"
        
        time.sleep(3)

# Página para o seu usuário ver (Simples e Limpa)
@app.route('/')
def home():
    html = '''
    <body style="background:#0f172a; color:white; font-family:sans-serif; text-align:center; padding-top:100px;">
        <h1>📊 Monitor de Resultados</h1>
        <div style="font-size:3em; margin:20px; color:#10b981;">{{ num }}</div>
        <p>Status do Robô: <b>{{ status }}</b></p>
        <p style="font-size:0.8em; color:#64748b;">Conectado via UptimeRobot 24/7</p>
    </body>
    '''
    return render_template_string(html, num=SISTEMA["ultimo_numero"], status=SISTEMA["status"])

# Inicia o monitor em segundo plano
threading.Thread(target=monitorar_roleta, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
