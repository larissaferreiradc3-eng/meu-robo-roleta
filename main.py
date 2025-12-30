def processar_dna_nexus(historico):
    # historico[0] é o mais recente
    if len(historico) < 10: return None

    # --- 1. LÓGICA DE SOMA (LARISSA) ---
    v_d3 = [25, 27, 30, 32, 34, 36]
    p_d2 = [13, 15, 17, 20, 22, 24]
    
    if historico[2] in v_d3 and historico[1] in p_d2 and historico[0] in p_d2:
        soma = historico[0] + historico[1] + historico[2]
        if soma > 36:
            soma = sum(int(d) for d in str(soma))
        return {
            "estrategia": "SOMA ESTELAR",
            "alvo": soma,
            "protecao": [0, 21],
            "obs": "Entrar Alvo + Vizinhos de Race"
        }

    # --- 2. LÓGICA TERMINAL (GABRIEL) ---
    if historico[2] == historico[3]: # Repetição detectada (Gatilho)
        gatilho = historico[1]
        alvo_x = historico[0]
        # Validação das 4 casas e Prova Real de 100rd deve ser checada aqui
        return {
            "estrategia": "TERMINAL CDC",
            "alvo": f"Terminais de {alvo_x}",
            "protecao": [0]
        }

    # --- 3. MONITOR DE PARCELAMENTO (DNA) ---
    # Se o último sinal foi 6 e caiu 3, mantém o alerta para o complemento
    # (Esta parte deve ser integrada ao banco de dados de 'memória de espera')

    return None
