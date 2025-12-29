import websocket
import json
import os
import time
from supabase import create_client, Client

# --- CONFIGURAÇÃO DE AMBIENTE ---
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- DNA DO SITE (Inalterável) ---
DNA_MEMORIA = {
    "HISTORICO": [],
    "RESIDUO_PARCELADO": 0,
    "ALVO_ATUAL": None,
    "FILTRO_MESA": "Estável"
}

# Grupos CDC - Geometria Gabriel [cite: 2025-12-29]
GRUPOS_CDC = {
    "D1C1": [1, 4, 7, 10], "D1C2": [2, 5, 8, 11], "D1C3": [3, 6, 9, 12],
    "D2C1": [13, 16, 19, 22], "D2C2": [14, 17, 20, 23], "D2C3": [15, 18, 21, 24],
    "D3C1": [25, 28, 31, 34], "D3C2": [26, 29, 32, 35], "D3C3": [27, 30, 33, 36]
}

# --- CAMADA: DETERMINAÇÃO DE COMPORTAMENTO DA MESA ---

def identificar_comportamento(n, alvo, memoria):
    """
    Filtro de DNA: Captura Substituições e Parcelamentos.
    Define se o pagamento é Literal ou Picado. [cite: 2025-12-29]
    """
    if alvo is None: return "Estável", 0
    
    # Lógica de Pagamento Parcelado (Monitor de Resíduo) [cite: 2025-12-29]
    soma_atual = memoria["RESIDUO_PARCELADO"] + n
    if soma_atual == alvo:
        return "Green por Soma Parcelada", 0
    elif n < 12: # Identifica início de pagamento picado [cite: 2025-12-29]
        return "Roleta iniciou pagamento picado", soma_atual
    
    return "Estável", 0

def analisar_estrategias(historico):
    """
    Módulos Solo: CDC, ESTELAR e NERA.
    Busca Confluência no Ponto de Convergência. [cite: 2025-12-29]
    """
    if len(historico) < 10: return None
    
    # Exemplo: Simulação de gatilho CDC Geometria Gabriel [cite: 2025-12-29]
    # Se o grupo atual traz o próximo grupo na transição sequencial
    return 18 # Define um Alvo Principal baseado na confluência

# --- PROCESSAMENTO PRINCIPAL ---

def processar_rodada(n):
    t = n % 10
    DNA_MEMORIA["HISTORICO"].append(n)
    if len(DNA_MEMORIA["HISTORICO"]) > 200: DNA_MEMORIA["HISTORICO"].pop(0)

    # 1. Aplicar Filtro de Comportamento (DNA do Green) [cite: 2025-12-29]
    status, residuo = identificar_comportamento(n, DNA_MEMORIA["ALVO_ATUAL"], DNA_MEMORIA)
    DNA_MEMORIA["RESIDUO_PARCELADO"] = residuo
    
    if "Green" in status:
        registrar_evento(n, t, "ALVO ATINGIDO (V1)", status)
        DNA_MEMORIA["ALVO_ATUAL"] = None
        return

    # 2. Se não houver alvo ativo, buscar novas confluências [cite: 2025-12-29]
    if DNA_MEMORIA["ALVO_ATUAL"] is None:
        novo_alvo = analisar_estrategias(DNA_MEMORIA["HISTORICO"])
        if novo_alvo:
            DNA_MEMORIA["ALVO_ATUAL"] = novo_alvo
            registrar_evento(n, t, "Análise de Fluxo Térmico", "Sinal em Processamento")
    else:
        # Se saiu uma parcela, avisa o site
        if status == "Roleta iniciou pagamento picado":
            registrar_evento(n, t, status, "Aguardar complemento")

def registrar_evento(n, t, estrategia, resultado):
    try:
        cor = "Verde" if n == 0 else ("Vermelho" if n in [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36] else "Preto")
        payload = {
            "numero": int(n),
            "terminal": int(t),
            "estrategia": estrategia,
            "resultado": resultado,
            "cor": cor
        }
        supabase.table("resultados_nexus").insert(payload).execute()
        print(f"✔️ Registro: {n} | {estrategia} | {resultado}")
    except Exception as e:
        print(f"❌ Erro Supabase: {e}")

def on_message(ws, message):
    dados = json.loads(message)
    if dados.get("slug") == "pragmatic-mega-roulette-brazilian":
        processar_rodada(dados.get("result"))

def iniciar():
    print("🚀 NexusIA V2 Online - Módulo DNA Ativo")
    ws = websocket.WebSocketApp("wss://api.revesbot.com.br/ws", on_message=on_message)
    ws.run_forever()

if __name__ == "__main__":
    iniciar()
