const SB_URL = "https://tpotbyekboefgbgmckp.supabase.co";
const SB_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRwb3RieWVrYm9lZmdjYmdtY2twIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjY4MDc1NjgsImV4cCI6MjA4MjM4MzU2OH0.rlZzMH0EWY54gk9MNolp_KTC2DYFxkb3P7KtPw_aYWw";
const supabaseClient = supabase.createClient(SB_URL, SB_KEY);

let ultimoId = null;

async function atualizarEspelhamento() {
    const { data } = await supabaseClient
        .from('resultados_nexus')
        .select('*')
        .order('id', { ascending: false })
        .limit(1);

    if (data && data.length > 0 && data[0].id !== ultimoId) {
        ultimoId = data[0].id;
        const reg = data[0];
        
        // Atualiza a tela com o DNA de Luxo [cite: 2025-12-28, 2025-12-29]
        document.getElementById('numero-atual').innerText = reg.numero;
        document.getElementById('status-ciclo').innerText = reg.resultado;
        
        // Cores Reais: 0 Verde, parcelas Vermelho/Preto [cite: 2025-12-28, 2025-12-29]
        const display = document.getElementById('numero-atual');
        display.style.color = (reg.cor === "Vermelho") ? "#FF3131" : 
                             (reg.cor === "Verde") ? "#00FF66" : "#FFFFFF";
    }
}

setInterval(atualizarEspelhamento, 5000);
