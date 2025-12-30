import os
import threading
from flask import Flask, render_template_string
import time
import random

# 1. Configuração do Servidor Web para o Render
app = Flask(__name__)

# Template HTML unificado com a identidade visual NEXUS
INDEX_HTML = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>NEXUS IA - Surpass Yourself</title>
    <style>
        :root {
            --bg-dark: #050505;
            --nexus-blue: #00d4ff;
            --nexus-orange: #ff4e00;
            --nexus-green: #00ff41;
            --text-main: #ffffff;
        }
        body {
            background-color: var(--bg-dark);
            color: var(--text-main);
            font-family: 'Inter', sans-serif;
            display: flex;
            justify-content: center;
            padding: 20px;
        }
        .container {
            width: 100%;
            max-width: 1000px;
            background: rgba(15, 15, 15, 0.95);
            border: 1px solid rgba(0, 212, 255, 0.2);
            border-radius: 20px;
            padding: 30px;
            text-align: center;
        }
        .logo {
            font-size: 3.5rem;
            letter-spacing: 8px;
            background: linear-gradient(135deg, var(--nexus-blue), var(--nexus-orange));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 900;
            margin: 0;
        }
        .scan-btn {
            width: 300px;
            height: 90px;
            background: transparent;
            border: 2px solid var(--nexus-blue);
            border-radius: 50px;
            color: white;
            font-size: 1.2rem;
            font-weight: bold;
            cursor: pointer;
            transition: 0.4s;
            margin: 40px 0;
        }
        .scan-btn:hover {
            border-color: var(--nexus-orange);
            box-shadow: 0 0 30px var(--nexus-orange);
        }
        .history-grid {
            display: grid;
            grid-template-columns: repeat(10, 1fr);
            gap: 6px;
            margin-top: 30px;
        }
        .num-box {
            aspect-ratio: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            border-radius: 4px;
            background: #111;
        }
        .red { background: #ff2a2a; }
        .green { background: #00ff41; color: #000; }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="logo">NEXUS</h1>
        <p style="letter-spacing: 4px; color: rgba(255,255,255,0.5);">SURPASS YOURSELF</p>
        
        <button class="scan-btn" onclick="analisar()">GERAR ANÁLISE IA</button>
        
        <div id="resultado" style="display:none; padding: 20px; border-left: 4px solid var(--nexus-green); background: rgba(255,255,255,0.03); margin-bottom: 20px;">
            <h3 style="color: var(--nexus-green); margin:0;">ALVO DETECTADO</h3>
            <p id="predicao" style="font-size: 1.5rem;"></p>
        </div>

        <div class="history-grid" id="grid"></div>
    </div>

    <script>
        function analisar() {
            const btn = document.querySelector('.scan-btn');
            btn.innerText = "SINCROIZANDO VETORES...";
            setTimeout(() => {
                document.getElementById('resultado').style.display = 'block';
                document.getElementById('predicao').innerText = "2ª COLUNA + PROTEÇÃO NO 0";
                btn.innerText = "GERAR ANÁLISE IA";
            }, 2000);
        }

        // Popular histórico inicial
        const grid = document.getElementById('grid');
        for(let i=0; i<100; i++) {
            const n = Math.floor(Math.random()*37);
            const box = document.createElement('div');
            box.className = 'num-box ' + (n==0 ? 'green' : ([1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36].includes(n) ? 'red' : ''));
            box.innerText = n;
            grid.appendChild(box);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(INDEX_HTML)

# 2. Lógica da IA em Segundo Plano (Motores NERA, ESTELAR, CDC)
def bot_ia_worker():
    print("🚀 Motores NERA, ESTELAR e CDC/DNA Iniciados...")
    while True:
        # Aqui entra sua lógica de captura de dados da roleta
        # E validação com a Regra das 4 Casas
        time.sleep(10) 

if __name__ == "__main__":
    # Inicia o Bot em uma thread separada
    threading.Thread(target=bot_ia_worker, daemon=True).start()
    
    # Inicia o Servidor Flask na porta exigida pelo Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
