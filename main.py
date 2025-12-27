import time, requests, os, threading
from flask import Flask, render_template_string
from supabase import create_client

app = Flask(__name__)

# --- CONFIGURAÇÃO SUPABASE ---
URL_SB = "https://tpotbyekboefgcbgmckp.supabase.co"
KEY_SB = "SUA_CHAVE_SUPABASE_AQUI"
supabase = create_client(URL_SB, KEY_SB)

SISTEMA = {"ultimo": "--", "status": "Iniciando...", "last_id": None}

def monitor_profissional():
    while True:
        try:
            # 1. Busca o link ATUALIZADO que o GitHub salvou no banco
            config = supabase.table("configuracoes").select("valor_link").eq("id", 1).execute()
            if not config.data:
                SISTEMA["status"] = "🔴 Tabela 'configuracoes' vazia!"
                time.sleep(10)
                continue
                
            url_dinamica = config.data[0]['valor_link']

            # 2. Faz a requisição para a Pragmatic
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            res = requests.get(url_dinamica, headers=headers, timeout=10)

            if res.status_code == 200:
                dados = res.json()
                # Acessa a lista de números da roleta
                historico = dados.get('data', {}).get('lastNumbers', [])
                
                if historico:
                    ultimo_jogo = historico[0]
                    numero = ultimo_jogo['value']
                    game_id = ultimo_jogo['gameId']
                    
                    if game_id != SISTEMA["last_id"]:
                        # Salva o novo número no seu banco de dados
                        supabase.table("resultados_roleta").insert({
                            "numero": str(numero), 
                            "contato": str(game_id)
                        }).execute()
                        
                        SISTEMA["ultimo"] = numero
                        SISTEMA["last_id"] = game_id
                        SISTEMA["status"] = "🟢 ONLINE - CAPTURANDO"
            else:
                SISTEMA["status"] = f"🟡 Token Expirado (Status {res.status_code})"

        except Exception as e:
            SISTEMA["status"] = f"🔴 Erro: {str(e)}"
        
        time.sleep(5) # Verifica a cada 5 segundos se saiu número novo

@app.route('/')
def dashboard():
    return render_template_string('''
        <body style="background:#020617; color:white; font-family:sans-serif; text-align:center; padding-top:80px;">
            <h1 style="color:#6366f1;">BOT ROLETA BLAZE 24H</h1>
            <div style="font-size:5em; font-weight:bold; background:#1e293b; display:inline-block; padding:20px 50px; border-radius:20px; border:4px solid #6366f1; margin:20px;">
                {{ num }}
            </div>
            <p>Status: <span>{{ status }}</span></p>
            <p style="color:#475569;">GitHub Actions: Ativo | Google Cloud: Online</p>
        </body>
    ''', num=SISTEMA["ultimo"], status=SISTEMA["status"])

# Inicia o monitoramento em uma thread separada
threading.Thread(target=monitor_profissional, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
