const { chromium } = require('playwright-extra');
const stealth = require('puppeteer-extra-plugin-stealth')();
const { createClient } = require('@supabase/supabase-js');

chromium.use(stealth);

// O GitHub vai preencher essas variáveis sozinho através dos "Secrets"
const supabaseUrl = process.env.SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_KEY;
const supabase = createClient(supabaseUrl, supabaseKey);

async function iniciar() {
    console.log("🚀 Buscando novo token na Blaze...");
    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();

    page.on('request', async (request) => {
        const url = request.url();
        // Filtra o link da Pragmatic que contém o histórico
        if (url.includes('statisticHistory') && url.includes('JSESSIONID')) {
            console.log("✅ Novo link encontrado!");
            
            const { error } = await supabase
                .from('configuracoes')
                .update({ valor_link: url, updated_at: new Date() })
                .eq('id', 1);

            if (!error) {
                console.log("🔥 Supabase atualizado com sucesso.");
                process.exit(0); // Fecha o script com sucesso
            }
        }
    });

    try {
        // Link da sala da roleta na Blaze
        await page.goto('https://blaze.com/pt/games/mega-roulette', { waitUntil: 'networkidle', timeout: 60000 });
        await new Promise(r => setTimeout(r, 20000)); // Espera 20s para o jogo carregar
    } catch (e) {
        console.error("❌ Erro ao acessar Blaze:", e.message);
        process.exit(1);
    } finally {
        await browser.close();
    }
}

iniciar();
