const _supabase = supabase.createClient('SUA_URL', 'SUA_KEY');

async function monitorarSistema() {
    setInterval(async () => {
        const { data, error } = await _supabase
            .from('resultados_nexus')
            .select('*')
            .order('created_at', { ascending: false });

        if (data) {
            renderizarHistorico(data.slice(0, 100)); // Pega os últimos 100 [cite: 2025-12-29]
            renderizarLogs(data.slice(0, 20));
            calcularAssertividade(data);
        }
    }, 2000);
}

function renderizarHistorico(lista) {
    const container = document.getElementById('live-history');
    container.innerHTML = lista.map(n => `
        <div class="ball ${n.cor}">${n.numero}</div>
    `).join('');
}

function renderizarLogs(lista) {
    const tbody = document.getElementById('log-body');
    tbody.innerHTML = lista.map(s => `
        <tr class="${s.resultado.includes('Green') ? 'row-green' : 'row-loss'}">
            <td>${s.numero}</td>
            <td>${s.estrategia}</td>
            <td>${s.resultado}</td>
            <td>${new Date(s.created_at).toLocaleTimeString()}</td>
        </tr>
    `).join('');
}

function calcularAssertividade(lista) {
    const greens = lista.filter(s => s.resultado.includes('Green')).length;
    const total = lista.length;
    const rate = total > 0 ? ((greens / total) * 100).toFixed(1) : 0;
    
    document.getElementById('win-rate').innerText = `${rate}%`;
    document.getElementById('total-greens').innerText = greens;
    document.getElementById('total-losses').innerText = total - greens;
}

monitorarSistema();
