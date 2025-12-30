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
TOKEN = os.environ.get("REVES_TOKEN") # Token capturado no F12

if not URL or not KEY:
    print("❌ Erro: SUPABASE_URL ou SUPABASE_KEY não configuradas no Render.")
else:
    supabase = create_client(URL, KEY)

# --- MÓDULO DNA: MONITOR DE ACÚMULO (NÃO EXCLUIR) ---
memoria_residuo = [] 

def processar_dna_luxo(numero):
    global memoria_residuo
    
    # 🧬 Regras do DNA de Luxo [cite: 2025-12-29]
    vermelhos = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]
    cor = "Verde" if numero == 0 else ("Vermelho" if numero in vermelhos else "Preto")
    terminal = numero % 10
    alvo = 6 # Alvo exemplo para demonstrar a soma sucessiva
    
    resultado_texto = "Analisando..."

    # 🎰 Lógica de Substituição por Decomposição de Ciclo [cite: 2025-12-29]
    if numero == alvo:
        resultado_texto = "Green Direto ✅"
        memoria_residuo = [] 
    elif numero < alvo:
        memoria_residuo.append(numero)
        soma_atual = sum(memoria_residuo)
        if soma_atual == alvo:
            resultado_texto = "Green por Soma Parcelada ✅"
            memoria_residuo = []
        else:
            resultado_texto = "Roleta iniciou pagamento picado"
    else:
        resultado_texto = "Aguardando Complemento"
        # Mantém resíduo se for útil, ou limpa se o ciclo quebrar
        if numero > alvo and len(memoria_residuo) > 0:
            memoria_residuo = []

    # --- ENVIO PARA O BANCO (ESPELHAMENTO) ---
    payload = {
        "numero": numero,
        "terminal": terminal,
        "resultado": resultado_texto,
        "cor": cor,
        "estrategia": "Mega Roulette - Espelhamento Real"
    }

    try:
        supabase.table("resultados_nexus").insert(payload).execute()
        print(f"🎰 MEGA ROULETTE: {numero} ({cor}) | {resultado_texto}")
    except Exception as e:
        print(f"❌ Erro ao gravar no Banco: {e}")

# --- CONEXÃO COM A API (SINAL CAPTURADO) ---
def on_message(ws, message):
    try:
        data = json.loads(message)
        # Filtro exato para o slug que você me enviou!
        if data.get("slug") == "pragmatic-mega-roulette":
            if "result" in data:
                numero = int(data.get("result"))
                processar_dna_luxo(numero)
    except:
        pass

def on_open(ws):
    print("📡 Conectado! Enviando comando de espelhamento para Mega Roulette...")
    
    # Se você tiver o Token, a API exige autenticação
    if TOKEN:
        ws.send(json.dumps({"action": "auth", "token": TOKEN}))
    
    # Comando de inscrição na mesa correta [cite: 2025-12-29]
    subscribe_msg = {
        "action": "subscribe",
        "slug": "pragmatic-mega-roulette"
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
            # Mantém a conexão viva
            ws.run_forever(ping_interval=30, ping_timeout=10)
        except Exception as e:
            print(f"🔌 Conexão perdida: {e}. Reconectando em 5s...")
            time.sleep(5)

# --- SERVIDOR KEEP-ALIVE (RENDER) ---
class Health(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.end_headers()
        self.wfile.write(b"SISTEMA NEXUS IA: ESPELHAMENTO ATIVO")

if __name__ == "__main__":
    # Inicia servidor de manutenção na porta 10000 (Exigência do Render)
    threading.Thread(target=lambda: HTTPServer(('0.0.0.0', 10000), Health).serve_forever(), daemon=True).start()
    iniciar_websocket()
