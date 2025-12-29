import os
import json
import threading
import websocket
from http.server import HTTPServer, BaseHTTPRequestHandler
from supabase import create_client

# --- CONFIGURAÇÕES DE AMBIENTE (RENDER) ---
URL = os.environ.get("SUPABASE_URL")
KEY = os.environ.get("SUPABASE_KEY")
supabase = create_client(URL, KEY)

# --- SERVIDOR PARA O SERVIÇO DE CLICKS (KEEP-ALIVE) ---
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Nexus IA: Sistema Online e Monitorando")

def run_web_server():
    # O Render exige escuta na porta 10000 para Web Services
    server = HTTPServer(('0.0.0.0', 10000), HealthCheckHandler)
    print("🌐 Servidor de Manutenção Ativo na porta 10000")
    server.serve_forever()

# --- LÓGICA DO DNA NEXUS IA ---
historico_residuos = [] # Memória de Espera para Parcelamento [cite: 2025-12-29]

def processar_dna(numero):
    global historico_residuos
    terminal = numero % 10
    vermelhos = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]
    cor = "Verde" if numero == 0 else ("Vermelho" if numero in vermelhos else "Preto")
    
    # Exemplo de Alvo da Geometria (ajuste conforme sua estratégia específica)
    alvo_exemplo = 6 
    
    resultado = "Monitorando..."
    
    # Filtro de Pagamento Parcelado (DNA) [cite: 2025-12-29]
    if numero < alvo_exemplo:
        historico_residuos.append(numero)
        resultado = "Roleta iniciou pagamento picado"
    elif sum(historico_residuos) + numero >= alvo_exemplo and len(historico_residuos) > 0:
        resultado = "Green por Soma ✅"
        historico_residuos = [] # Limpa a memória após o Green
    elif numero == alvo_exemplo:
        resultado = "Green Direto ✅"
        historico_residuos = []

    # Envio para o Banco de Dados (Supabase)
    payload = {
        "numero": numero,
        "terminal": terminal,
        "estrategia": "Geometria Gabriel / NERA",
        "resultado": resultado,
        "cor": cor
    }
    
    try:
        supabase.table("resultados_nexus").insert(payload).execute()
        print(f"📡 Dado Enviado: {numero} | {resultado}")
    except Exception as e:
        print(f"❌ Erro Supabase: {e}")

# --- CONEXÃO COM A API REVESBOT ---
def on_message(ws, message):
    data = json.loads(message)
    if "numero" in data:
        processar_dna(int(data["numero"]))

def on_error(ws, error):
    print(f"⚠️ Erro WebSocket: {error}")

def on_close(ws, close_status_code, close_msg):
    print("🔌 Conexão Fechada. Reconectando...")

def on_open(ws):
    print("✅ Conectado à API Revesbot - Nexus IA Ativo")

def iniciar_websocket():
    ws = websocket.WebSocketApp("wss://api.revesbot.com.br/ws",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)
    ws.run_forever()

# --- EXECUÇÃO EM PARALELO ---
if __name__ == "__main__":
    # 1. Inicia o Servidor Web para o Render não dormir (Thread 1)
    threading.Thread(target=run_web_server, daemon=True).start()
    
    # 2. Inicia o Robô de Monitoramento (Thread Principal)
    iniciar_websocket()
