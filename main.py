import websocket
import json
import os
from supabase import create_client, Client

# Configuração com suas chaves fornecidas
SUPABASE_URL = "https://tpotbyekboefgcbgmckp.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." # Sua Key Completa
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# DNA INALTERÁVEL [cite: 2025-12-29]
DNA_MEMORIA = {
    "HISTORICO": [],
    "RESIDUO_PARCELADO": 0,
    "ALVO_ATUAL": None,
    "STRAT": "Aguardando..."
}

def processar_rodada(n):
    t = n % 10
    DNA_MEMORIA["HISTORICO"].append(n)
    if len(DNA_MEMORIA["HISTORICO"]) > 200: DNA_MEMORIA["HISTORICO"].pop(0)

    # Lógica de Pagamento Parcelado [cite: 2025-12-29]
    if DNA_MEMORIA["ALVO_ATUAL"]:
        soma = DNA_MEMORIA["RESIDUO_PARCELADO"] + n
        if soma == DNA_MEMORIA["ALVO_ATUAL"]:
            enviar_supabase(n, t, "DNA Estelar", "Green por Soma ✅")
            DNA_MEMORIA["ALVO_ATUAL"] = None
            DNA_MEMORIA["RESIDUO_PARCELADO"] = 0
            return
        elif n < 12: # Identifica parcela
            DNA_MEMORIA["RESIDUO_PARCELADO"] = soma
            enviar_supabase(n, t, "Monitoramento", "Pagamento Parcelado...")
            return

    # Gatilho CDC / NERA [cite: 2025-12-29]
    # (Inserir aqui sua lógica específica de alvo)
    DNA_MEMORIA["ALVO_ATUAL"] = 12 # Exemplo
    enviar_supabase(n, t, "Geometria Gabriel", "Alvo: 12")

def enviar_supabase(n, t, est, res):
    # Cores conforme o DNA [cite: 2025-12-28, 2025-12-29]
    cor = "Verde" if n == 0 else ("Vermelho" if n in [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36] else "Preto")
    payload = {"numero": n, "terminal": t, "estrategia": est, "resultado": res, "cor": cor}
    supabase.table("resultados_nexus").insert(payload).execute()

def on_message(ws, message):
    dados = json.loads(message)
    if dados.get("slug") == "pragmatic-mega-roulette-brazilian":
        processar_rodada(dados.get("result"))

ws = websocket.WebSocketApp("wss://api.revesbot.com.br/ws", on_message=on_message)
ws.run_forever()
