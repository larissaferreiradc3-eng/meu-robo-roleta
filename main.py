import os
from supabase import create_client

# CONFIGURAÇÃO UNIFICADA
SUPABASE_URL = "https://tpotbyekboefgbgmckp.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRwb3RieWVrYm9lZmdjYmdtY2twIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjgwNzU2OCwiZXhwIjoyMDgyMzgzNTY4fQ.F7J0g_iTIE_7oxXsGpObSsRq7AApc1y7pvpLmYjQcgk"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def simular_performance_dna():
    print("\n🚀 INICIANDO MODO SIMULAÇÃO: Validando DNA de Soma...")
    
    # BUSCA OS DADOS REAIS DO SEU BANCO
    try:
        # Mudança para a tabela correta 'resultados_nexus'
        response = supabase.table("resultados_nexus").select("numero").order("id", desc=True).limit(200).execute()
        dados = [r['numero'] for r in response.data]
        print(f"✅ {len(dados)} números carregados para análise.")
    except Exception as e:
        print(f"❌ Erro ao acessar banco: {e}")
        return

    v_d3 = [25, 27, 30, 32, 34, 36] # Vermelhos D3
    p_d2 = [13, 15, 17, 20, 22, 24] # Pretos D2
    acertos = 0
    total_gatilhos = 0

    # Percorre o histórico (do mais antigo para o mais novo)
    for i in range(len(dados) - 10, 5, -1):
        # Gatilho Larissa: V_D3 -> P_D2 -> P_D2
        if dados[i] in v_d3 and dados[i-1] in p_d2 and dados[i-2] in p_d2:
            total_gatilhos += 1
            
            # Cálculo do Alvo por Soma (DNA Larissa) [cite: 2025-12-29]
            alvo = dados[i] + dados[i-1] + dados[i-2]
            while alvo > 36:
                alvo = sum(int(d) for d in str(alvo))
            
            # Checa se o Alvo ou 0 saiu nas próximas 4 casas (1+3 gales)
            vitoria = False
            for gale in range(1, 5):
                if i-2-gale >= 0:
                    resultado_futuro = dados[i-2-gale]
                    # Green Direto ou 0 (Verde sempre ganha no DNA) [cite: 2025-12-28]
                    if resultado_futuro == alvo or resultado_futuro == 0:
                        vitoria = True
                        break
            
            if vitoria: acertos += 1

    taxa = (acertos / total_gatilhos * 100) if total_gatilhos > 0 else 0
    
    print(f"\n--- 📊 RELATÓRIO DE PERFORMANCE NEXUS ---")
    print(f"🎯 Gatilhos Identificados: {total_gatilhos}")
    print(f"✅ Acertos (Incluindo 0 e Soma): {acertos}")
    print(f"📈 Taxa de Assertividade: {taxa:.2f}%")
    print(f"-----------------------------------------\n")

if __name__ == "__main__":
    simular_performance_dna()
