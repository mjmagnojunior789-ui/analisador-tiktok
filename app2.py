import streamlit as st
from groq import Groq
import yt_dlp
import os
from duckduckgo_search import DDGS  # Sistema de busca integrado e gratuito

# --- 1. Configuração da Página e Tema Escuro Premium ---
st.set_page_config(
    page_title="HookLab // Analisador de Ganchos", 
    page_icon="⚡", 
    layout="centered"
)

# Injeção de CSS para customizar as cores, botões e fontes
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
st.markdown("<p style='text-align: center; color: #94A3B8; font-size: 1.1rem;'>Mapeamento Estrutural Rígido com Rastreamento de Meta em Tempo Real.</p>", unsafe_allow_html=True)
st.markdown("---")

# --- 3. Área de Credenciais e Inputs ---
if "GROQ_API_KEY" in st.secrets:
    api_key = st.secrets["GROQ_API_KEY"]
else:
    api_key = st.text_input("Chave de Acesso (Groq API Key):", type="password", placeholder="gsk_...")

url_tiktok = st.text_input("Link do vídeo do TikTok:", placeholder="https://www.tiktok.com/@username/video/...")

nome_jogo = st.text_input("Para qual JOGO você quer clonar essa estrutura?", placeholder="Ex: Minecraft, Valorant, GTA V...")

# --- 4. O PROMPT BRUTO E RÍGIDO (Foco Algoritmo) ---
prompt_analise = """
Você é um Diretor de Retenção Algorítmica e Analista de Dados sênior especializado no ecossistema do TikTok.
Sua análise deve ser BRUTA, DIRETA e Puramente ESTRUTURAL. Ignore elogios ou textos subjetivos. Foque na mecânica fria que dita o gráfico de retenção e as métricas atuais que valorizam tempo de tela e compartilhamento.

Desmonte a transcrição fornecida exatamente sob esta estrutura rígida:

## 🧮 1. A EQUAÇÃO DO GANCHO (0 a 3s)
* **Texto Bruto Usado:** "[Frase exata dita]"
* **Mecânica do Scroll-Stopper:** Qual foi o gatilho exato (Quebra de expectativa, Alerta de dopamina, Inveja ou Medo)? Por que o cérebro do usuário travou o dedo ao ler isso?
* **Densidade de Palavras:** O ritmo foi acelerado ou teve pausas calculadas?

## 📐 2. O ESQUELETO DA COPY (Blueprint Abstrato)
Transforme o roteiro do vídeo inteiro em uma fórmula reutilizável substituindo os elementos específicos por tags genéricas entre colchetes. 
*Exemplo de formato esperado:* `[GANCHO: Afirmação Chocante] + [PROVOCAÇÃO: Você está fazendo errado] + [PROVA: Olha o que acontece] + [ENTREGA: Passo 1, Passo 2] + [CTA de Loop]`.
Crie a linha de montagem exata deste vídeo para que eu possa apenas preencher os espaços em branco.

## 📉 3. PONTOS CRÍTICOS DE RETENÇÃO (Métricas Atuais)
* **Retenção de Meio:** Como o roteiro evitou a queda livre no gráfico após os 5 segundos? 
* **Gatilho de SEO de Busca:** Quais palavras-chave fortes de nicho foram repetidas estrategicamente no texto para forçar o TikTok a indexar esse vídeo na barra de pesquisa?
* **O Mecanismo de Loop / Compartilhamento:** Como o final foi amarrado para fazer o usuário reassistir (Loop limpo) ou salvar o vídeo imediatamente?

---

"""

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
                
                # --- NOVO RECURSO: Busca na Internet pelas informações reais do Jogo ---
                contexto_jogo = ""
                if nome_jogo:
                    with st.spinner(f'Rastreando a internet por dados e metas atuais de {nome_jogo}...'):
                        try:
                            with DDGS() as ddgs:
                                # Faz uma varredura buscando guias, atualizações e mecânicas do jogo digitado
                                busca = list(ddgs.text(f"{nome_jogo} game dicas meta atual mecanicas", max_results=3))
                                contexto_jogo = "\n".join([f"- {res['body']}" for res in busca])
                        except Exception:
                            contexto_jogo = "Não foi possível coletar dados ao vivo da internet. Use sua base de conhecimento atualizada."

                with st.spinner('Quebrando roteiro e injetando dados do meta...'):
                    if nome_jogo:
                        instrucao_jogo = f"""
## 🛠️ CLONES ROTEIRIZADOS PARA O JOGO: {nome_jogo.upper()}
**Informações Reais do Jogo coletadas ao vivo da Internet:**
{contexto_jogo}

Sua missão agora é pegar o esqueleto (Blueprint) abstrato extraído do vídeo de exemplo e preencher as lacunas gerando 3 scripts prontos para gravar aplicados ao jogo **{nome_jogo}**. 
Use OBRIGATORIAMENTE os dados coletados acima: cite armas do meta atual, bugs reais conhecidos, mecânicas reais, frustrações verdadeiras dos jogadores ou termos técnicos corretos desse jogo. Os roteiros precisam parecer escritos por um jogador profissional.

* **Script 1 (Foco em Curiosidade/Descoberta/Meta)**
* **Script 2 (Foco em Dor/Erro Comum que faz o player perder)**
* **Script 3 (Foco em Tática Secreta/Recompensa Rápida)**
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
