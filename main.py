import os, json, threading, websocket, time
from http.server import HTTPServer, BaseHTTPRequestHandler
from supabase import create_client

# CONFIGURAÇÕES TÉCNICAS
URL = "https://tpotbyekboefgbgmckp.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRwb3RieWVrYm9lZmdjYmdtY2twIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjgwNzU2OCwiZXhwIjoyMDgyMzgzNTY4fQ.F7J0g_iTIE_7oxXsGpObSsRq7AApc1y7pvpLmYjQcgk"
supabase = create_client(URL, KEY)

# O DNA NÃO ACEITA NÚMEROS INVENTADOS [cite: 2025-12-29]
memoria_residuo = []

def processar_vitoria_real(numero):
    global memoria_residuo
    # Configuração de Cores Exatas [cite: 2025-12-28]
    vermelhos = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]
    cor = "Verde" if numero == 0 else ("Vermelho" if numero in vermelhos else "Preto")
    terminal = numero % 10
    alvo = 6 

    # Lógica de Pagamento Parcelado (Substituição por Decomposição) [cite: 2025-12-29]
    if numero == alvo:
        res = "Green Direto ✅"
        memoria_residuo = []
    elif 0 < numero < alvo:
        memoria_residuo.append(numero)
        if sum(memoria_residuo) == alvo:
            res = "Green por Soma Parcelada ✅"
            memoria_residuo = []
        else:
            res = "Roleta iniciou pagamento picado"
    else:
        res = "Monitoramento Normal"
        memoria_residuo = []

    payload = {
        "numero": numero, 
        "terminal": terminal, 
        "resultado": res, 
        "cor": cor, 
        "estrategia": "Mega Roulette Real"
    }

    try:
        supabase.table("resultados_nexus").insert(payload).execute()
        print(f"💎 NÚMERO REAL DA MESA: {numero}")
    except:
        pass

def on_message(ws, message):
    data = json.loads(message)
    # BLOQUEIO TOTAL: Só processa se o sinal vier da Mega Roulette [cite: 2025-12-29]
    if data.get("slug") == "pragmatic-mega-roulette":
        resultado_fatiado = data.get("result")
        if resultado_fatiado is not None:
            # Envia para processamento sem delay [cite: 2025-12-29]
            threading.Thread(target=processar_vitoria_real, args=(int(resultado_fatiado),)).start()

def monitor_sinal():
    while True:
        try:
            # Conexão Turbo sem quedas [cite: 2025-12-29]
            ws = websocket.WebSocketApp("wss://api.revesbot.com.br/ws",
                on_open=lambda ws: ws.send(json.dumps({"action": "subscribe", "slug": "pragmatic-mega-roulette"})),
                on_message=on_message)
            ws.run_forever(ping_interval=10)
        except:
            time.sleep(2)

class RenderHealth(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.end_headers()
        self.wfile.write(b"SISTEMA REAL-TIME ATIVO")

if __name__ == "__main__":
    print("🛰️ CONECTANDO AOS SATÉLITES DA PRAGMATIC...")
    threading.Thread(target=lambda: HTTPServer(('0.0.0.0', int(os.environ.get("PORT", 10000))), RenderHealth).serve_forever(), daemon=True).start()
    monitor_sinal()
