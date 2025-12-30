import os
import json
import threading
import websocket
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from supabase import create_client

# --- CONFIGURAÇÕES DE AMBIENTE ---
URL = os.environ.get("SUPABASE_URL")
KEY = os.environ.get("SUPABASE_KEY")
# O Token que você vai capturar no F12 deve ser colocado no Render como REVES_TOKEN
TOKEN = os.environ.get("REVES_TOKEN") 

supabase = create_client(URL, KEY)

# --- MÓDULO DNA: MONITOR DE ACÚMULO (NÃO EXCLUIR) ---
memoria_residuo = [] 

def processar_dna_luxo(numero):
    global memoria_residuo
    
    # Configurações do DNA de Luxo [cite: 2025-12-29]
    vermelhos = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]
    cor = "Verde" if numero == 0 else ("Vermelho" if numero in vermelhos else "Preto")
    terminal = numero % 10
    alvo = 6 # Exemplo de alvo para a lógica de parcelamento
    
    resultado_texto = "Monitorando..."

    # Lógica de Substituição por Decomposição de Ciclo [cite: 2025-12-29]
    if numero == alvo:
        resultado_texto = "Green Direto ✅"
        memoria_residuo = []
    elif numero < alvo:
        memoria_residuo.append(numero)
        if sum(memoria_residuo) == alvo:
            resultado_texto = "Green por Soma Parcelada ✅"
            memoria_residuo = []
        else:
            resultado_texto = "Roleta iniciou pagamento picado"
    else:
        resultado_texto = "Aguardando Complemento"
        # O 0 continua sendo Verde mesmo na soma [cite: 2025-12-29]

    # --- ENVIO PARA O BANCO (ESPELHAMENTO) ---
    payload = {
        "numero": numero,
        "terminal": terminal,
        "resultado": resultado_texto,
        "cor": cor,
        "estrategia": "Mega Roulette - Espelhamento"
    }

    try:
        supabase.table("resultados_nexus").insert(payload).execute()
        print(f"🎰 DNA IDENTIFICADO: {numero} ({cor}) | {resultado_texto}")
    except Exception as e:
        print(f"❌ Erro Supabase: {e}")

# --- CONEXÃO COM A API (FORMATO SLUG) ---
def on_message(ws, message):
    try:
        data = json.loads(message)
        # Filtro para a Mega Roulette (ou a mesa que você extraiu o sinal)
        # Use "mega-roulette" ou o slug que aparecer no seu F12
        if "result" in data:
            numero = int(data.get("result"))
            processar_dna_luxo(numero)
    except Exception as e:
        pass # Ignora mensagens de sistema da API

def on_open(ws):
    print("✅ Conectado à API Revesbot - Autenticando...")
    # Se você tiver o Token, a API exige esse comando de abertura:
    if TOKEN:
        auth_msg = {"action": "auth", "token": TOKEN}
        ws.send(json.dumps(auth_msg))
    
    # Inscrição na mesa Mega Roulette
    subscribe_msg = {"action": "subscribe", "slug": "mega-roulette"}
    ws.send(json.dumps(subscribe_msg))

def iniciar_websocket():
    while True:
        try:
            ws = websocket.WebSocketApp(
                "wss://api.revesbot.com.br/ws",
                on_open=on_open,
                on_message=on_message
            )
            ws.run_forever(ping_interval=30, ping_timeout=10)
        except:
            time.sleep(5) # Tenta reconectar se a API cair

# --- SERVIDOR KEEP-ALIVE (RENDER) ---
class Health(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.end_headers()
        self.wfile.write(b"DNA NEXUS IA ONLINE")

if __name__ == "__main__":
    threading.Thread(target=lambda: HTTPServer(('0.0.0.0', 10000), Health).serve_forever(), daemon=True).start()
    iniciar_websocket()
