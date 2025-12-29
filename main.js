const _supabase = supabase.createClient('https://tpotbyekboefgcbgmckp.supabase.co', 'SUA_KEY_FORNECIDA');

async function syncDashboard() {
    const { data, error } = await _supabase
        .from('resultados_nexus')
        .select('*')
        .order('created_at', { ascending: false });

    if (data) {
        // Histórico Automático de 100 Números
        const historyContainer = document.getElementById('live-history');
        historyContainer.innerHTML = data.slice(0, 100).map(item => `
            <div class="ball ${item.cor}">${item.numero}</div>
        `).join('');

        // Cálculo de Assertividade (Greens vs Total)
        const total = data.length;
        const greens = data.filter(s => s.resultado.includes('Green')).length;
        const rate = total > 0 ? ((greens / total) * 100).toFixed(1) : "0.0";

        document.getElementById('win-rate').innerText = `${rate}%`;
        document.getElementById('count-greens').innerText = greens;
        document.getElementById('count-losses').innerText = total - greens;

        // Saúde das Estratégias (Destaque para CDC e Estelar)
        const stratHealth = document.getElementById('strategy-health');
        stratHealth.innerHTML = `
            <div class="strat-item">CDC Gabriel: <span>Estável</span></div>
            <div class="strat-item">Estelar: <span>Em Operação</span></div>
        `;
    }
}

// Atualização rápida a cada 2 segundos
setInterval(syncDashboard, 2000);
