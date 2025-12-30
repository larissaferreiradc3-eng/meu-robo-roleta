import os
import json
import threading
import websocket
from http.server import HTTPServer, BaseHTTPRequestHandler
from supabase import create_client

# --- CONFIGURAÇÕES DE AMBIENTE (RENDER) ---
# Usando os nomes padrão que o Supabase e Render reconhecem melhor
URL = os.environ.get("SUPABASE_URL")
KEY = os.environ.get("SUPABASE_KEY")

if not URL or not KEY:
    print("❌ ERRO: Chaves SUPABASE_URL ou SUPABASE_KEY não encontradas!")
else:
    supabase = create_client(URL, KEY)

# --- SERVIDOR HEALTH-CHECK (PARA O RENDER NÃO DORMIR) ---
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"NEXUS IA: DNA DE LUXO ONLINE")

def run_web_server():
    server = HTTPServer(('0.0.0.0', 10000), HealthCheckHandler)
    print("🌐 Servidor Keep-Alive Ativo na porta 10000")
    server.serve_forever()

# --- MÓDULO DNA: MONITOR DE ACÚMULO E PARCELAMENTO ---
# Esta memória não pode ser apagada no Red se houver resíduo [cite: 2025-12-29]
memoria_residuo = [] 

def analisar_pagamento_parcelado(numero):
    global memoria_residuo
    
    # Configurações do DNA [cite: 2025-12-29]
    vermelhos = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]
    cor = "Verde" if numero == 0 else ("Vermelho" if numero in vermelhos else "Preto")
    terminal = numero % 10
    
    # Exemplo de Alvo (Pode ser dinâmico conforme sua estratégia)
    alvo = 6 
    
    resultado_texto = "Analisando..."

    # Lógica de Substituição por Decomposição de Ciclo [cite: 2025-12-29]
    if numero == alvo:
        resultado_texto = "Green Direto ✅"
        memoria_residuo = [] # Ciclo concluído
    
    elif numero < alvo:
        memoria_residuo.append(numero)
        soma_atual = sum(memoria_residuo)
        
        if soma_atual == alvo:
            resultado_texto = "Green por Soma Parcelada ✅"
            memoria_residuo = [] # Ciclo concluído
        else:
            resultado_texto = "Roleta iniciou pagamento picado (Aguardar complemento)"
            # O sistema mantém o resíduo na "memória de espera" [cite: 2025-12-29]
            
    else:
        # Se o número for maior que o alvo sem completar soma
        resultado_texto = "Loss ❌"
        memoria_residuo = []

    # --- ENVIO PARA O BANCO DE DADOS ---
    payload = {
        "numero": numero,
        "terminal": terminal,
        "resultado": resultado_texto,
        "cor": cor,
        "estrategia": "DNA DE LUXO - PARCELADO"
    }

    try:
        supabase.table("resultados_nexus").insert(payload).execute()
        print(f"📡 DNA IDENTIFICADO: {numero} | {resultado_texto}")
    except Exception as e:
        print(f"❌ Erro ao gravar DNA: {e}")

# --- CONEXÃO API REVESBOT ---
def on_message(ws, message):
    try:
        data = json.loads(message)
        if "numero" in data:
            analisar_pagamento_parcelado(int(data["numero"]))
    except Exception as e:
        print(f"⚠️ Erro ao processar mensagem: {e}")

def on_open(ws):
    print("✅ Conectado à API Revesbot - Monitoramento DNA Iniciado")

def iniciar_websocket():
    ws = websocket.WebSocketApp(
        "wss://api.revesbot.com.br/ws",
        on_open=on_open,
        on_message=on_message
    )
    ws.run_forever()

# --- START ---
if __name__ == "__main__":
    # 1. Inicia Health Check (Thread)
    threading.Thread(target=run_web_server, daemon=True).start()
    
    # 2. Inicia Robô
    iniciar_websocket()
