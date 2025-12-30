import os, json, threading, websocket, time
from http.server import HTTPServer, BaseHTTPRequestHandler
from supabase import create_client

# CONFIGURAÇÕES DNA [cite: 2025-12-29]
URL = "https://tpotbyekboefgbgmckp.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRwb3RieWVrYm9lZmdjYmdtY2twIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjgwNzU2OCwiZXhwIjoyMDgyMzgzNTY4fQ.F7J0g_iTIE_7oxXsGpObSsRq7AApc1y7pvpLmYjQcgk"
supabase = create_client(URL, KEY)

def processar_dna_mega(numero):
    # Cores DNA [cite: 2025-12-28, 2025-12-29]
    vermelhos = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]
    cor = "Verde" if numero == 0 else ("Vermelho" if numero in vermelhos else "Preto")
    terminal = numero % 10
    
    payload = {
        "numero": numero, 
        "terminal": terminal, 
        "resultado": "Sinal Monitorado", 
        "cor": cor, 
        "estrategia": "Mega Roulette DNA"
    }
    
    try:
        supabase.table("resultados_nexus").insert(payload).execute()
        print(f"📡 MEGA ROULETTE: {numero} salvo com sucesso!")
    except Exception as e:
        print(f"Erro no Supabase: {e}")

def on_message(ws, message):
    data = json.loads(message)
    # AJUSTADO PARA MEGA ROULETTE [cite: 2025-12-29]
    if data.get("slug") == "pragmatic-mega-roulette":
        num = data.get("result")
        if num is not None:
            threading.Thread(target=processar_dna_mega, args=(int(num),)).start()

def iniciar_websocket():
    while True:
        try:
            ws = websocket.WebSocketApp("wss://api.revesbot.com.br/ws",
                on_open=lambda ws: ws.send(json.dumps({"action": "subscribe", "slug": "pragmatic-mega-roulette"})),
                on_message=on_message)
            ws.run_forever(ping_interval=10)
        except:
            time.sleep(2)

# SERVIDOR DE SAÚDE PARA O RENDER NÃO DESLIGAR
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"NEXUS DNA IS ALIVE")

def rodar_servidor_web():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    print(f"🌍 Servidor de Saúde na porta {port}")
    server.serve_forever()

if __name__ == "__main__":
    # Inicia o servidor web em uma linha separada
    threading.Thread(target=rodar_servidor_web, daemon=True).start()
    # Inicia a leitura da roleta
    print("🚀 MOTOR DNA NEXUS INICIADO...")
    iniciar_websocket()
