import os, json, threading, websocket, time
from http.server import HTTPServer, BaseHTTPRequestHandler
from supabase import create_client

# CONFIGURAÇÕES OFICIAIS DO SEU PROJETO
URL = "https://tpotbyekboefgbgmckp.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRwb3RieWVrYm9lZmdjYmdtY2twIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjgwNzU2OCwiZXhwIjoyMDgyMzgzNTY4fQ.F7J0g_iTIE_7oxXsGpObSsRq7AApc1y7pvpLmYjQcgk"
supabase = create_client(URL, KEY)

# MEMÓRIA DE ACÚMULO PARA O DNA DE PARCELAMENTO [cite: 2025-12-29]
memoria_residuo = []

def processar_dados_reais(numero):
    global memoria_residuo
    # DNA de Cores Profissional [cite: 2025-12-28, 2025-12-29]
    vermelhos = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]
    cor = "Verde" if numero == 0 else ("Vermelho" if numero in vermelhos else "Preto")
    terminal = numero % 10 # Regra de Terminal (3 a 6 vezes) [cite: 2025-12-29]
    alvo = 6 

    # Lógica de Pagamento Parcelado (Substituição por Decomposição) [cite: 2025-12-29]
    if numero == alvo:
        resultado_dna = "Green Direto ✅"
        memoria_residuo = []
    elif 0 < numero < alvo:
        memoria_residuo.append(numero)
        if sum(memoria_residuo) == alvo:
            resultado_dna = "Green por Soma Parcelada ✅"
            memoria_residuo = []
        else:
            resultado_dna = "Roleta iniciou pagamento picado" # Monitor de Acúmulo [cite: 2025-12-29]
    else:
        resultado_dna = "Monitoramento Normal"
        memoria_residuo = []

    # Envia o dado REAL para o seu Supabase [cite: 2025-12-30]
    payload = {
        "numero": numero, 
        "terminal": terminal, 
        "resultado": resultado_dna, 
        "cor": cor, 
        "estrategia": "Mega Roulette - Real Time"
    }
    
    try:
        supabase.table("resultados_nexus").insert(payload).execute()
        print(f"✅ DADO REAL CAPTURADO: {numero} | {resultado_dna} | Terminal: {terminal}")
    except Exception as e:
        print(f"❌ Erro ao salvar no banco: {e}")

def on_message(ws, message):
    try:
        data = json.loads(message)
        # Filtro exclusivo para a MEGA ROULETTE (Sem números aleatórios!) [cite: 2025-12-29]
        if data.get("slug") == "pragmatic-mega-roulette":
            num_real = data.get("result")
            if num_real is not None:
                # Dispara o processamento sem travar a recepção [cite: 2025-12-29]
                threading.Thread(target=processar_dados_reais, args=(int(num_real),)).start()
    except Exception as e:
        print(f"Erro no processamento da API: {e}")

def conectar_sinal_real():
    while True:
        try:
            # Conexão direta com o fornecedor de dados da roleta [cite: 2025-12-29]
            ws = websocket.WebSocketApp("wss://api.revesbot.com.br/ws",
                on_open=lambda ws: ws.send(json.dumps({"action": "subscribe", "slug": "pragmatic-mega-roulette"})),
                on_message=on_message)
            ws.run_forever(ping_interval=10, ping_timeout=5)
        except:
            print("Tentando reconectar ao sinal real...")
            time.sleep(2)

# Servidor de Saúde para o Render [cite: 2025-12-30]
class Health(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.end_headers()
        self.wfile.write(b"NEXUS REAL-TIME ONLINE")

if __name__ == "__main__":
    print("🚀 NEXUS IA: Conectando à Mega Roulette Real...")
    threading.Thread(target=lambda: HTTPServer(('0.0.0.0', int(os.environ.get("PORT", 10000))), Health).serve_forever(), daemon=True).start()
    conectar_sinal_real()
