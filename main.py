import time
import requests
import re
import os
import threading
from flask import Flask
from supabase import create_client

# --- CONFIGURAÇÃO PARA O RENDER NÃO DESLIGAR ---
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Monitor da Roleta Rodando!", 200

# --- CONFIGURAÇÕES DO BANCO ---
URL_SB = "https://stsqpalmjeybdxeodexo.supabase.co"
KEY_SB = "sb_secret_PFcBWZuXAGbUcfZiYsnmRg_x4OBmWB8"
supabase = create_client(URL_SB, KEY_SB)

# O link agora pode ser atualizado direto no código ou via variável de ambiente
URL_API = "https://games.pragmaticplaylive.net/api/ui/statisticHistory?tableId=mrbras531mrbr532&numberOfGames=500&JSESSIONID=OSBg5G4sGAKXfy6-RTD5KAKUIt6xLHqbb_f53t75pmwMq_hv8Vba!-472946834-adaccecb&ck=1766857116400&game_mode=roulette_desktop"

def extrair_numero(texto):
    match = re.search(r'(\d+)', str(texto))
    return match.group(1) if match else None

def monitorar():
    print("--- [SISTEMA] Monitor Iniciado ---")
    ultimo_game_id_salvo = None
    
    while True:
        try:
            response = requests.get(URL_API, timeout=15)
            if response.status_code == 200:
                dados = response.json()
                historico = dados.get('history', [])
                if historico:
                    recente = historico[0]
                    game_id = recente.get('gameId')
                    
                    if game_id != ultimo_game_id_salvo:
                        numero = extrair_numero(recente.get('gameResult'))
                        if numero:
                            supabase.table("resultados_roleta").insert({
                                "numero": str(numero),
                                "contato": str(game_id)
                            }).execute()
                            print(f"🎯 Novo: {numero}")
                            ultimo_game_id_salvo = game_id
            elif response.status_code == 401:
                print("🛑 Sessão expirada no Render.")
        except Exception as e:
            print(f"⚠️ Erro: {e}")
        time.sleep(5)

# Inicia o monitor em uma thread separada
threading.Thread(target=monitorar, daemon=True).start()

if __name__ == "__main__":
    # O Render define a porta automaticamente na variável PORT
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
