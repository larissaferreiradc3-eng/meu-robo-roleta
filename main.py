import os, json, threading, websocket, time
from http.server import HTTPServer, BaseHTTPRequestHandler
from supabase import create_client

# CONFIGURAÇÕES DO DNA NEXUS [cite: 2025-12-29]
URL = "https://tpotbyekboefgbgmckp.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRwb3RieWVrYm9lZmdjYmdtY2twIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjgwNzU2OCwiZXhwIjoyMDgyMzgzNTY4fQ.F7J0g_iTIE_7oxXsGpObSsRq7AApc1y7pvpLmYjQcgk"
supabase = create_client(URL, KEY)

memoria_residuo = [] 

def processar_dna_mega(numero):
    global memoria_residuo
    # DNA de Cores [cite: 2025-12-28, 2025-12-29]
    vermelhos = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]
    cor = "Verde" if numero == 0 else ("Vermelho" if numero in vermelhos else "Preto")
    terminal = numero % 10
    alvo = 6 
    
    # Lógica de Pagamento Parcelado (Substituição por Decomposição) [cite: 2025-12-29]
    if numero == alvo:
        res = "Green Direto ✅"
        memoria_residuo = []
    elif numero < alvo and numero > 0:
        memoria_residuo.append(numero)
        if sum(memoria_residuo) == alvo:
            res = "Green por Soma Parcelada ✅"
            memoria_residuo = []
        else:
            res = "Roleta iniciou pagamento picado"
    else:
        res = "Aguardando Padrão"
        memoria_residuo = []

    payload = {"numero": numero, "terminal": terminal, "resultado": res, "cor": cor, "estrategia": "Mega Roulette - DNA Luxo"}
    try:
        supabase.table("resultados_nexus").insert(payload).execute()
        print(f"📡 MEGA DNA: {numero} | {res} | Terminal: {terminal}")
    except: pass

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
            ws.run_forever(ping_interval=10, ping_timeout=5)
        except: time.sleep(2)

class Health(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.end_headers()
        self.wfile.write(b"NEXUS DNA ONLINE")

if __name__ == "__main__":
    threading.Thread(target=lambda: HTTPServer(('0.0.0.0', 10000), Health).serve_forever(), daemon=True).start()
    iniciar_websocket()
