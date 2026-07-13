import streamlit as st
from groq import Groq
import yt_dlp
import os
import requests  # Para conectar com a API da Steam
from duckduckgo_search import DDGS

# --- 1. Configuração da Página e Tema Escuro Premium ---
st.set_page_config(
    page_title="HookLab // Analisador de Ganchos", 
    page_icon="⚡", 
    layout="centered"
)

st.markdown("""
    <style>
    .stApp {
        background-color: #0B0E14;
        color: #E2E8F0;
    }
    .stTextInput input {
        background-color: #1A1F2C !important;
        color: #FFFFFF !important;
        border: 1px solid #2D3748 !important;
        border-radius: 8px !important;
    }
    .stTextInput input:focus {
        border-color: #7C3AED !important;
        box-shadow: 0 0 0 1px #7C3AED !important;
    }
    .stButton>button {
        background: linear-gradient(135deg, #7C3AED 0%, #4F46E5 100%) !important;
        color: white !important;
        border: none !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3) !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px) !important;
    }
    .stAlert {
        background-color: #1A1F2C !important;
        border: 1px solid #3B82F6 !important;
        border-radius: 8px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. Cabeçalho Principal ---
st.markdown("<h1 style='text-align: center; color: #FFFFFF; font-family: system-ui;'>⚡ Hook<span style='color: #7C3AED;'>Lab</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94A3B8; font-size: 1.1rem;'>Mapeamento Estrutural Rígido // Engine de Dados Multi-Plataforma.</p>", unsafe_allow_html=True)
st.markdown("---")

# --- 3. Área de Credenciais e Inputs ---
if "GROQ_API_KEY" in st.secrets:
    api_key = st.secrets["GROQ_API_KEY"]
else:
    api_key = st.text_input("Chave de Acesso (Groq API Key):", type="password", placeholder="gsk_...")

url_tiktok = st.text_input("Link do vídeo do TikTok:", placeholder="https://www.tiktok.com/@username/video/...")

nome_jogo = st.text_input("Para qual JOGO você quer clonar essa estrutura?", placeholder="Ex: Valorant, Elden Ring, Rainbow Six, Fortnite...")

# --- PROMPT BRUTO E RÍGIDO ---
prompt_analise = """
Você é um Diretor de Retenção Algorítmica e Analista de Dados sênior especializado no ecossistema do TikTok e nicho de Gaming.
Sua análise deve ser BRUTA, DIRETA e Puramente ESTRUTURAL. Ignore elogios ou textos subjetivos. Foque na mecânica fria que dita o gráfico de retenção e as métricas atuais que valorizam tempo de tela e compartilhamento.

Desmonte a transcrição fornecida exatamente sob esta estrutura rígida:

## 🧮 1. A EQUAÇÃO DO GANCHO (0 a 3s)
* **Texto Bruto Usado:** "[Frase exata dita]"
* **Mecânica do Scroll-Stopper:** Qual foi o gatilho exato (Quebra de expectativa, Alerta de dopamina, Inveja ou Medo)? Por que o cérebro do usuário travou o dedo ao ler isso?
* **Densidade de Palavras:** O ritmo foi acelerado ou teve pausas calculadas?

## 📐 2. O ESQUELETO DA COPY (Blueprint Abstrato)
Transforme o roteiro do vídeo inteiro em uma fórmula reutilizável substituindo os elements específicos por tags genéricas entre colchetes. 
*Exemplo de formato esperado:* `[GANCHO: Afirmação Chocante] + [PROVOCAÇÃO: Você está fazendo errado] + [PROVA: Olha o que acontece] + [ENTREGA: Passo 1, Passo 2] + [CTA de Loop]`.
Crie a linha de montagem exata deste vídeo para que eu possa apenas preencher os espaços em branco.

## 📉 3. PONTOS CRÍTICOS DE RETENÇÃO (Métricas Atuais)
* **Retenção de Meio:** Como o roteiro evitou a queda livre no gráfico após os 5 segundos? 
* **Gatilho de SEO de Busca:** Quais palavras-chave fortes de nicho foram repetidas estrategicamente no texto para forçar o TikTok a indexar esse vídeo na barra de pesquisa?
* **O Mecanismo de Loop / Compartilhamento:** Como o final foi amarrado para fazer o usuário reassistir (Loop limpo) ou salvar o vídeo imediatamente?

---

"""

# --- Funções de Coleta de Dados ---
def buscar_dados_oficiais_steam(jogo):
    """Consulta a API oficial da Steam Store para extrair metadados reais do jogo"""
    try:
        url_busca = f"https://store.steampowered.com/api/storesearch/?term={jogo}&l=brazilian"
        res_busca = requests.get(url_busca, timeout=5).json()
        if res_busca.get("items"):
            appid = res_busca["items"][0]["id"]
            url_detalhes = f"https://store.steampowered.com/api/appdetails?appids={appid}&l=brazilian"
            res_detalhes = requests.get(url_detalhes, timeout=5).json()
            if res_detalhes.get(str(appid), {}).get("success"):
                dados = res_detalhes[str(appid)]["data"]
                descricao = dados.get("short_description", "")
                generos = ", ".join([g["description"] for g in dados.get("genres", [])])
                return f"- [DATABASE STEAM] Descrição Oficial: {descricao} | Categorias/Gêneros: {generos}\n"
    except Exception:
        pass
    return ""

def baixar_video(url):
    opcoes_ytdlp = {
        'outtmpl': 'video_temp.mp4', 
        'format': 'bestaudio/best',
        'quiet': True,
        'noplaylist': True
    }
    try:
        with yt_dlp.YoutubeDL(opcoes_ytdlp) as ydl:
            ydl.download([url])
        return "video_temp.mp4"
    except Exception as e:
        return None

# --- 5. Execução do Aplicativo ---
if st.button("Destrinchar Estrutura Algorítmica 🚀"):
    if not api_key:
        st.warning("⚠️ Por favor, insira uma chave válida.")
    elif not url_tiktok:
        st.warning("⚠️ Cole um link do TikTok para começar.")
    else:
        with st.spinner('Extraindo dados do TikTok...'):
            caminho_video = baixar_video(url_tiktok)
            
        if caminho_video is None:
            st.error("❌ O link falhou ou o TikTok barrou a requisição.")
        else:
            try:
                client = Groq(api_key=api_key)
                
                with st.spinner('Decodificando áudio...'):
                    with open(caminho_video, "rb") as file:
                        transcricao = client.audio.transcriptions.create(
                            file=(caminho_video, file.read()),
                            model="whisper-large-v3",
                            response_format="text",
                            language="pt"
                        )
                
                # --- BIG DATA GAMING: Agregação de Dados das Plataformas ---
                contexto_gaming = ""
                if nome_jogo:
                    with st.spinner(f'Conectando com as redes da Steam, Riot, Epic e Ubisoft...'):
                        # 1. Puxa dados estruturados se o jogo estiver na Steam
                        contexto_gaming += buscar_dados_oficiais_steam(nome_jogo)
                        
                        # 2. Faz uma varredura cirúrgica nos portais oficiais de Patch Notes (Riot, Epic, Ubisoft)
                        try:
                            with DDGS() as ddgs:
                                query_plataformas = f"{nome_jogo} (site:playvalorant.com OR site:ubisoft.com OR site:epicgames.com OR site:leagueoflegends.com OR site:fortnite.com) patch notes atualizacao meta balanceamento"
                                busca_portais = list(ddgs.text(query_plataformas, max_results=3))
                                for res in busca_portais:
                                    contexto_gaming += f"- [LAUNCHER PORTAL DATA] {res['body']}\n"
                        except Exception:
                            pass

                with st.spinner('Injetando telemetria de jogo na fórmula algorítmica...'):
                    if nome_jogo:
                        instrucao_jogo = f"""
## 🛠️ CLONES ROTEIRIZADOS ULTRA-ESPECÍFICOS: {nome_jogo.upper()}
**DADOS AGREGADOS DIRETAMENTE DOS BANCOS DA STEAM / RIOT / EPIC / UBISOFT:**
{contexto_gaming}

Sua missão agora é pegar o esqueleto (Blueprint) abstrato extraído do vídeo de exemplo e preencher as lacunas gerando 3 scripts prontos para gravar aplicados inteiramente ao jogo **{nome_jogo}**.

**REGRAS RÍGIDAS DE GERAÇÃO:**
1. É PROIBIDO usar termos genéricos ou colchetes vazios nos roteiros finais (ex: Não use "[insira seu item aqui]"). Baseando-se estritamente nos dados extraídos acima da Steam/Riot/Epic/Ubisoft, você deve escolher itens reais, armas reais, agentes/campeões reais, mapas reais, alterações de patches recentes ou gírias reais da comunidade competitiva desse jogo e inseri-los diretamente no texto falado.
2. O texto deve soar 100% natural para um jogador nativo e experiente desse jogo.

Gere os 3 scripts seguindo estritamente esta estrutura:

### 🎮 Script 1 (Foco em Curiosidade / Meta Atual do Jogo)
* **Elementos Reais Injetados:** [Liste quais dados de patches, armas ou itens oficiais coletados você embutiu neste script]
* **Roteiro Pronto para Gravar:** 
"..."

### 🎮 Script 2 (Foco em Dor / Erro Crítico que faz a comunidade perder ou passar raiva)
* **Elementos Reais Injetados:** [Liste quais mecânicas frustrantes, erros de mecânica ou problemas reais de gameplay você embutiu]
* **Roteiro Pronto para Gravar:** 
"..."

### 🎮 Script 3 (Foco em Tática Secreta / Recompensa Rápida / Build)
* **Elementos Reais Injetados:** [Liste qual combo, spot de mapa, tática de pro-player ou build específica você embutiu]
* **Roteiro Pronto para Gravar:** 
"..."
"""
                    else:
                        instrucao_jogo = """
## 🛠️ 3 CLONES ESTRUTURAIS PRONTOS
Crie 3 variações de scripts curtos clonando a exata estrutura mecânica do exemplo, usando placeholders como [Tema], [Problema] e [Solução] para que eu possa preencher com o nicho que eu quiser.
"""
                    
                    prompt_final = prompt_analise + instrucao_jogo
                    
                    chat_completion = client.chat.completions.create(
                        messages=[{"role": "user", "content": f"{prompt_final}\n\nTranscrição para processamento:\n{transcricao}"}],
                        model="llama-3.3-70b-versatile",
                        temperature=0.2, 
                    )
                    resposta = chat_completion.choices[0].message.content
                
                # --- Organização em Abas ---
                st.markdown("### 📊 Engenharia Reversa")
                aba_analise, aba_texto = st.tabs(["⚡ Fórmula Rígida", "🗣️ Texto de Origem"])
                
                with aba_analise:
                    st.markdown(resposta)
                    
                with aba_texto:
                    st.info(transcricao)
                
                os.remove(caminho_video)
                
            except Exception as e:
                st.error(f"❌ Falha no processamento: {e}")
                if os.path.exists(caminho_video):
                    os.remove(caminho_video)
