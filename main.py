import os
import json
import threading
import websocket
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from supabase import create_client

# --- CONFIGURAÇÕES ---
URL = os.environ.get("SUPABASE_URL")
KEY = os.environ.get("SUPABASE_KEY")
# Se você tiver um Token da Revesbot, coloque aqui no Render como REVES_TOKEN
TOKEN = os.environ.get("REVES_TOKEN", "SEU_TOKEN_AQUI") 

supabase = create_client(URL, KEY)

# --- MEMÓRIA DNA (Parcelamento) ---
memoria_residuo = [] 

def processar_dna_mega(numero):
    global memoria_residuo
    terminal = numero % 10
    alvo = 6 # Exemplo de alvo do DNA
    
    # Lógica de DNA: Pagamento Parcelado [cite: 2025-12-29]
    if numero == alvo:
        res = "Green Direto ✅"
        memoria_residuo = []
    elif numero < alvo:
        memoria_residuo.append(numero)
        res = "Roleta iniciou pagamento picado"
    elif sum(memoria_residuo) + numero == alvo:
        res = "Green por Soma Parcelada ✅"
        memoria_residuo = []
    else:
        res = "Aguardando Padrão"
        memoria_residuo = []

    # Envio para o Supabase (Espelhamento)
    payload = {
        "numero": numero,
        "terminal": terminal,
        "resultado": res,
        "estrategia": "Mega Roulette - Espelhamento"
    }
    supabase.table("resultados_nexus").insert(payload).execute()
    print(f"🎰 MEGA ROULETTE: {numero} | {res}")

# --- CONEXÃO COM FILTRO DE MESA ---
def on_message(ws, message):
    data = json.loads(message)
    
    # O PULO DO GATO: Filtramos apenas a Mega Roulette
    # Nota: Verifique se o nome no log da API é 'Mega Roulette' ou 'mega_roulette'
    if data.get("mesa") == "Mega Roulette" or "mega" in str(data).lower():
        if "numero" in data:
            processar_dna_mega(int(data["numero"]))

def on_open(ws):
    print("📡 Autenticando na Mega Roulette...")
    # Comando de Assinatura para a mesa específica
    subscribe_msg = {
        "action": "subscribe",
        "mesa": "Mega Roulette",
        "token": TOKEN
    }
    ws.send(json.dumps(subscribe_msg))

def iniciar_websocket():
    while True:
        try:
            ws = websocket.WebSocketApp(
                "wss://api.revesbot.com.br/ws",
                on_open=on_open,
                on_message=on_message
            )
            ws.run_forever(ping_interval=30)
        except:
            time.sleep(5)

# --- SERVIDOR KEEP-ALIVE ---
class Health(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.end_headers()
        self.wfile.write(b"ESPELHAMENTO MEGA ONLINE")

if __name__ == "__main__":
    threading.Thread(target=lambda: HTTPServer(('0.0.0.0', 10000), Health).serve_forever(), daemon=True).start()
    iniciar_websocket()
