import os, json, threading, websocket, time
from http.server import HTTPServer, BaseHTTPRequestHandler
from supabase import create_client

# CONFIGURAÇÕES DNA [cite: 2025-12-29]
URL = "https://tpotbyekboefgbgmckp.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRwb3RieWVrYm9lZmdjYmdtY2twIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjgwNzU2OCwiZXhwIjoyMDgyMzgzNTY4fQ.F7J0g_iTIE_7oxXsGpObSsRq7AApc1y7pvpLmYjQcgk"
supabase = create_client(URL, KEY)

memoria_residuo = [] 

def processar_dna_mega(numero):
    global memoria_residuo
    vermelhos = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]
    cor = "Verde" if numero == 0 else ("Vermelho" if numero in vermelhos else "Preto")
    terminal = numero % 10
    alvo = 6 
    
    # Lógica DNA de Parcelamento [cite: 2025-12-29]
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

    payload = {"numero": numero, "terminal": terminal, "resultado": res, "cor": cor, "estrategia": "Mega Roulette DNA"}
    try:
        supabase.table("resultados_nexus").insert(payload).execute()
        print(f"📡 SINAL ENVIADO: {numero} | {res}")
    except: pass

def on_message(ws, message):
    data = json.loads(message)
    if data.get("slug") == "pragmatic-mega-roulette":
        num = data.get("result")
        if num is not None:
            # Processamento Instantâneo sem Delay [cite: 2025-12-29]
            threading.Thread(target=processar_dna_mega, args=(int(num),)).start()

def iniciar_websocket():
    while True:
        try:
            ws = websocket.WebSocketApp("wss://api.revesbot.com.br/ws",
                on_open=lambda ws: ws.send(json.dumps({"action": "subscribe", "slug": "pragmatic-mega-roulette"})),
                on_message=on_message)
            ws.run_forever(ping_interval=10)
        except: time.sleep(2)

if __name__ == "__main__":
    print("🚀 MOTOR MEGA DNA ONLINE")
    iniciar_websocket()
