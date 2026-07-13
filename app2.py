import streamlit as st
from groq import Groq
import yt_dlp
import os
import requests
import re
from duckduckgo_search import DDGS

# --- 1. Configuração da Página e Tema Escuro Premium ---
st.set_page_config(
    page_title="HookLab // Central de Inteligência", 
    page_icon="⚡", 
    layout="wide"  # Mudado para wide para aproveitar melhor o espaço com os novos menus
)

# Injeção de CSS Avançado para customizar a Sidebar e os Menus de Seleção
st.markdown("""
    <style>
    /* Fundo global e textos */
    .stApp {
        background-color: #0B0E14;
        color: #E2E8F0;
    }
    /* Estilização da Barra Lateral (Sidebar) */
    [data-testid="stSidebar"] {
        background-color: #0D111A !important;
        border-right: 1px solid #1E293B;
    }
    /* Customização dos Inputs e Menus Selectbox */
    .stTextInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: #1A1F2C !important;
        color: #FFFFFF !important;
        border: 1px solid #2D3748 !important;
        border-radius: 8px !important;
    }
    /* Botão Principal com Degradê Premium */
    .stButton>button {
        background: linear-gradient(135deg, #7C3AED 0%, #4F46E5 100%) !important;
        color: white !important;
        border: none !important;
        padding: 14px 28px !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3) !important;
        font-size: 1.1rem !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(124, 58, 237, 0.5) !important;
    }
    .stAlert {
        background-color: #1A1F2C !important;
        border: 1px solid #3B82F6 !important;
        border-radius: 8px !important;
    }
    /* Ajuste de títulos internos das Abas */
    .stTabs [data-baseweb="tab"] {
        color: #94A3B8 !important;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        color: #7C3AED !important;
        border-bottom-color: #7C3AED !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. PAINEL LATERAL DE CONFIGURAÇÃO (SaaS Style) ---
st.sidebar.markdown("<h2 style='color: #FFFFFF; font-family: system-ui;'>⚙️ Parâmetros do Meta</h2>", unsafe_allow_html=True)
st.sidebar.markdown("Configure as especificações do algoritmo abaixo antes de disparar o motor.")

categoria_jogo = st.sidebar.selectbox(
    "Gênero/Categoria do Jogo:",
    ["FPS / Tiro Competitivo", "RPG / Soulslike / Open World", "Battle Royale", "Sandbox / Minecraft / Roblox", "MOBA / Estratégia", "Terror / Survival", "Simuladores / Corrida"]
)

tema_roteiro = st.sidebar.selectbox(
    "Linha de Abordagem do Roteiro:",
    ["Técnico / Meta Atual e Builds", "Cômico / Humor, Memes e Desventuras", "Lore / Mistérios e Storytelling Oculto", "Desafios Extremos / Hardcore", "Dicas de Pro-Player para Iniciantes"]
)

duracao_alvo = st.sidebar.select_slider(
    "Duração Alvo (Algoritmo Atual):",
    options=["Curto (<30 segundos)", "Padrão Viral (1 minuto)", "Long-form Retenção (+2 minutos)"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("<p style='color: #475569; font-size: 0.8rem; text-align: center;'>HookLab PRO v2.5 // Engine 2026</p>", unsafe_allow_html=True)


# --- 3. PAINEL PRINCIPAL ---
st.markdown("<h1 style='text-align: center; color: #FFFFFF; font-family: system-ui;'>⚡ Hook<span style='color: #7C3AED;'>Lab</span> PRO</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94A3B8; font-size: 1.1rem;'>Engine de Dados, Auditoria de Perfis e Clonagem Algorítmica Estrutural.</p>", unsafe_allow_html=True)
st.markdown("---")

# Área de Credenciais e Inputs Primários
if "GROQ_API_KEY" in st.secrets:
    api_key = st.secrets["GROQ_API_KEY"]
else:
    api_key = st.text_input("Chave de Acesso (Groq API Key):", type="password", placeholder="gsk_...")

url_tiktok = st.text_input("Link do vídeo de exemplo do TikTok:", placeholder="https://www.tiktok.com/@username/video/...")

col1, col2 = st.columns(2)
with col1:
    arroba_criador = st.text_input("Criador (@arroba ou Nome do Perfil):", placeholder="Ex: @alanzoka, @tavares")
with col2:
    nome_jogo = st.text_input("Jogo alvo ou Link da Steam:", placeholder="Ex: Valorant, Elden Ring, Warzone...")

# --- 4. O PROMPT DE AUDITORIA ULTRA-RÍGIDO ---
prompt_analise = """
Você é um Diretor de Retenção Algorítmica, Analista de Dados e Engenheiro de Marcas focado no ecossistema do TikTok.
Sua análise deve ser BRUTA, DIRETA e Puramente ESTRUTURAL. Ignore elogios. Foque na mecânica fria que dita o gráfico de retenção, retenção estável de primeiro quadrante e conversão de visualizações em seguidores fiéis.

Desmonte os dados fornecidos exatamente sob esta estrutura rígida:

## 🧮 1. A EQUAÇÃO DO GANCHO (0 a 3s)
* **Texto Bruto Usado no Vídeo:** "[Frase exata dita]"
* **Mecânica do Scroll-Stopper:** Qual foi o gatilho exato (Quebra de expectativa, Alerta de dopamina, Inveja ou Medo)? Por que o cérebro do usuário travou o dedo ao ler isso?
* **Densidade de Palavras:** O ritmo foi acelerado ou teve pausas calculadas?

## 📐 2. O ESQUELETO DA COPY (Blueprint Abstrato)
Transforme o roteiro do vídeo inteiro em uma fórmula reutilizável substituindo os elementos específicos por tags genéricas entre colchetes. 
Crie a linha de montagem exata deste vídeo para que eu possa apenas preencher os espaços em branco.

## 📉 3. PONTOS CRÍTICOS DE RETENÇÃO & SEO
* **Retenção de Meio:** Como o roteiro evitou a queda livre no gráfico após os 5 segundos? 
* **Gatilho de SEO de Busca:** Quais palavras-chave fortes de nicho foram repetidas estrategicamente no texto para forçar o TikTok a indexar esse vídeo na barra de pesquisa?
* **O Mecanismo de Loop / Compartilhamento:** Como o final foi amarrado para fazer o usuário reassistir (Loop limpo) ou salvar o vídeo imediatamente?

## 🚨 4. FILTRO DE SEGURANÇA E DIRETRIZES DE MODERAÇÃO
* **Palavras de Risco Identificadas:** Quais termos na transcrição correm o risco de disparar o filtro de moderação do áudio automatizado do TikTok (ex: matar, roubado, hack, bug).
* **Dicionário de Camuflagem:** Crie uma tabela rápida substituindo os termos perigosos identificados por palavras limpas e seguras para o algoritmo.

## 👤 5. AUDITORIA DE PERFIL & DIAGNÓSTICO DE AUTORIDADE
Baseando-se nos dados históricos do criador fornecidos:
* **Arquétipo Atual do Perfil:** Classifique a presença digital desse criador.
* **O que PODE Melhorar:** Aponte de forma rígida quais falhas estruturais de roteiro ou posicionamento esse criador costuma cometer.
* **Blindagem de Retenção:** Indique a estratégia exata que perfis de mais de 1 milhão de seguidores usam para manter a base engajada neste exato nicho.

---

"""

# --- Funções Avançadas de Coleta de Dados ---
def buscar_dados_oficiais_steam(entrada):
    appid = None
    if "store.steampowered.com/app/" in entrada:
        try:
            match = re.search(r"/app/(\d+)", entrada)
            if match:
                appid = match.group(1)
        except Exception:
            pass
            
    if not appid:
        try:
            url_busca = "https://store.steampowered.com/api/storesearch/"
            res_busca = requests.get(url_busca, params={"term": entrada, "l": "brazilian"}, timeout=5).json()
            if res_busca.get("items"):
                appid = res_busca["items"][0]["id"]
        except Exception:
            pass
            
    if appid:
        try:
            url_detalhes = "https://store.steampowered.com/api/appdetails"
            res_detalhes = requests.get(url_detalhes, params={"appids": appid, "l": "brazilian"}, timeout=5).json()
            if res_detalhes.get(str(appid), {}).get("success"):
                dados = res_detalhes[str(appid)]["data"]
                nome_real = dados.get("name", entrada)
                descricao = dados.get("short_description", "")
                generos = ", ".join([g["description"] for g in dados.get("genres", [])])
                texto_retorno = f"- [DATABASE STEAM OFICIAL] Nome Identificado: {nome_real} | Descrição Técnica: {descricao} | Categorias: {generos}\n"
                return nome_real, texto_retorno
        except Exception:
            pass
            
    return entrada, ""

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
if st.button("Disparar Engenharia Reversa & Clonagem Avançada 🚀"):
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
                
                with st.spinner('Decodificando áudio de amostra...'):
                    with open(caminho_video, "rb") as file:
                        transcricao = client.audio.transcriptions.create(
                            file=(caminho_video, file.read()),
                            model="whisper-large-v3",
                            response_format="text",
                            language="pt"
                        )
                
                # --- BIG DATA GAMING & CREATOR SCRAPING ---
                contexto_gaming = ""
                contexto_perfil = ""
                nome_final_jogo = nome_jogo if nome_jogo else "Jogo Genérico"
                
                if arroba_criador:
                    with st.spinner(f'Escaneando pegada digital de {arroba_criador}...'):
                        try:
                            with DDGS() as ddgs:
                                query_perfil = f"{arroba_criador} site:tiktok.com estilo de video conteudo"
                                try:
                                    busca_perfil = list(ddgs.text(keywords=query_perfil, max_results=3))
                                except TypeError:
                                    busca_perfil = list(ddgs.text(query_perfil, max_results=3))
                                for res in busca_perfil:
                                    contexto_perfil += f"- [HISTÓRICO DO CRIADOR] {res['body']}\n"
                        except Exception:
                            pass
                
                if nome_jogo:
                    with st.spinner(f'Mapeando telemetria e metas de {nome_jogo}...'):
                        nome_final_jogo, dados_steam = buscar_dados_oficiais_steam(nome_jogo)
                        contexto_gaming += dados_steam
                        try:
                            with DDGS() as ddgs:
                                query_plataformas = f"{nome_final_jogo} (site:playvalorant.com OR site:ubisoft.com OR site:epicgames.com OR site:leagueoflegends.com OR site:fortnite.com) patch notes atualizacao"
                                try:
                                    busca_portais = list(ddgs.text(keywords=query_plataformas, max_results=3))
                                except TypeError:
                                    busca_portais = list(ddgs.text(query_plataformas, max_results=3))
                                for res in busca_portais:
                                    contexto_gaming += f"- [LAUNCHER DATA] {res['body']}\n"
                        except Exception:
                            pass

                with st.spinner('Processando matriz de roteirização avançada com novos menus...'):
                    # INJEÇÃO CIRÚRGICA DOS PARÂMETROS SELECIONADOS NOS MENUS DO SITE
                    instrucao_final = f"""
## 🎯 6. MATRIZ DE ROTEIRIZAÇÃO VARIADA (Fórmula Clonal Adaptada com Filtros Avançados)
**FILTROS DE DIRECIONAMENTO OBRIGATÓRIOS DO LAYOUT:**
* **Gênero/Categoria Alvo:** {categoria_jogo}
* **Abordagem/Tom Exigido:** {tema_roteiro}
* **Tempo/Estrutura de Ritmo:** {duracao_alvo}

**REGRA CRÍTICA E ABSOLUTA DE CLONAGEM:** Descarte por completo o assunto do vídeo original anexado. É terminantemente PROIBIDO fazer um roteiro sobre o assunto do exemplo. Você vai clonar EXATAMENTE E APENAS a fôrma, a cadência e a ordem das tags de retenção extraídas na Etapa 2 (Blueprint).

O assunto real e exclusivo dos 3 novos roteiros deve ser focado no universo do jogo **{nome_final_jogo}**, adaptando o texto falado e o ritmo para respeitar a Categoria ({categoria_jogo}), o Tom ({tema_roteiro}) e a Duração desejada ({duracao_alvo}). Use as gírias corretas do nicho e dados coletados.

**Dados de Contexto do Criador:**
{contexto_perfil if contexto_perfil else "(Mantenha o arquétipo ideal.)"}

**Dados de Contexto Técnico do Jogo Alvo ({nome_final_jogo.upper()}):**
{contexto_gaming if contexto_gaming else "(Use sua base integrada de dados do jogo.)"}

Crie 3 opções de roteiros inéditos para o jogo **{nome_final_jogo}**, clonando a fôrma da Etapa 2 e respeitando as configurações acima:

### 📈 Opção 1: Linha de Retenção Cinestésica (Foco em Entretenimento Rápido / Viralização de Massa)
* *Diretriz de Ajuste do Filtro:* Molde a fôrma de gancho do vídeo base aplicando ao tom "{tema_roteiro}" e categoria "{categoria_jogo}".
* *Elementos Reais do Jogo Injetados:* [Liste quais elementos você usou]
* *Roteiro Pronto para Gravar:*
"..."

### 💎 Opção 2: Linha de Autoridade Inabalável (Foco em Alto Valor / Salvamentos e SEO de Busca)
* *Diretriz de Ajuste do Filtro:* Adapte o desenvolvimento e entrega do vídeo base focando na duração "{duracao_alvo}" e ensinando um elemento forte de "{nome_final_jogo}".
* *Elementos Reais do Jogo Injetados:* [Liste as mecânicas reais embutidas]
* *Roteiro Pronto para Gravar:*
"..."

### 📣 Opção 3: Linha de Engajamento Polarizado (Foco em Compartilhamento e Loops nos Comentários)
* *Diretriz de Ajuste do Filtro:* Aplique o ritmo de finalização e loops do vídeo base criando uma polêmica/discussão forte com o tom "{tema_roteiro}".
* *Elementos Reais do Jogo Injetados:* [Liste os pontos do meta embutidos]
* *Roteiro Pronto para Gravar:*
"..."
"""
                    
                    prompt_final = prompt_analise + instrucao_final
                    
                    chat_completion = client.chat.completions.create(
                        messages=[{"role": "user", "content": f"{prompt_final}\n\nTranscrição base para engenharia reversa:\n{transcricao}"}],
                        model="llama-3.3-70b-versatile",
                        temperature=0.2, 
                    )
                    resposta = chat_completion.choices[0].message.content
                
                # --- Organização em Abas ---
                st.markdown("### 📊 Inteligência de Conteúdo")
                aba_analise, aba_texto = st.tabs(["⚡ Auditoria & Matriz Pronta", "🗣️ Transcrição Base"])
                
                with aba_analise:
                    st.markdown(resposta)
                    
                with aba_texto:
                    st.info(transcricao)
                
                os.remove(caminho_video)
                
            except Exception as e:
                st.error(f"❌ Falha no processamento: {e}")
                if os.path.exists(caminho_video):
                    os.remove(caminho_video)
