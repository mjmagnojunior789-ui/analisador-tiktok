import streamlit as st
from groq import Groq
import yt_dlp
import os

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
        box-shadow: 0 6px 20px rgba(124, 58, 237, 0.5) !important;
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
st.markdown("<p style='text-align: center; color: #94A3B8; font-size: 1.1rem;'>Engenharia reversa e inteligência de copy para ganchos do TikTok.</p>", unsafe_allow_html=True)
st.markdown("---")

# --- 3. Área de Credenciais e Inputs ---
if "GROQ_API_KEY" in st.secrets:
    api_key = st.secrets["GROQ_API_KEY"]
else:
    api_key = st.text_input("Chave de Acesso (Groq API Key):", type="password", placeholder="gsk_...")

url_tiktok = st.text_input("Link do vídeo do TikTok:", placeholder="https://www.tiktok.com/@username/video/...")

# NOVO RECURSO: Segunda caixa para especificar o jogo
nome_jogo = st.text_input("Para qual JOGO você quer aplicar essa estrutura? (Opcional):", placeholder="Ex: Minecraft, GTA V, Valorant, Free Fire...")

# --- 4. O Prompt Especialista Adaptável ---
prompt_analise = """
Você é um Engenheiro de Retenção e Copywriter sênior focado em crescimento no TikTok e no nicho de Gaming.
Sua missão é pegar a transcrição do vídeo e transformá-la em um TEMPLATE DE ESTRUTURA VIRAL pronto para ser copiado e adaptado.

Gere o relatório formatado rigorosamente seguindo esta estrutura:

## 🪝 1. O GANCHO CAMPEÃO (0 a 3 segundos)
* **Texto Exato Usado:** "[Cole aqui a frase exata do criador]"
* **Gatilho Mental Dominante:** (Ex: curiosidade, dor urgente, quebra de padrão)
* **Análise de Ritmo:** Por que esse texto forçou o usuário a parar o scroll?

## 📈 2. A CONSTRUÇÃO (Buildup)
* **Estratégia de Retenção:** Como o criador segurou o interesse logo após o gancho?
* **Sugestão de Quebra de Padrão:** Indique em qual segundo exato deste bloco você deve colocar um corte, zoom ou inserção de texto na tela para reter o público.

## 💎 3. A ENTREGA (Outcome)
* **Resumo da Entrega:** Como o vídeo entregou o valor prometido de forma rápida e sem enrolação? 
* **Fórmula do Conteúdo:** Extraia a lógica por trás da explicação (Ex: Problema -> Solução Direta, Antes -> Depois).

## 📢 4. CHAMADA PARA AÇÃO (CTA)
* **Comando Final:** Qual comando foi dado?
* **Otimização de Algoritmo:** Sugira como reescrever essa CTA focando estritamente em Salvar ou Compartilhar (que são as métricas que mais distribuem vídeos hoje).

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
if st.button("Analisar Estrutura 🚀"):
    if not api_key:
        st.warning("⚠️ Por favor, insira uma chave válida.")
    elif not url_tiktok:
        st.warning("⚠️ Cole um link do TikTok para começar.")
    else:
        with st.spinner('Baixando áudio do TikTok...'):
            caminho_video = baixar_video(url_tiktok)
            
        if caminho_video is None:
            st.error("❌ O link pode estar quebrado ou o TikTok bloqueou o acesso temporariamente.")
        else:
            try:
                client = Groq(api_key=api_key)
                
                with st.spinner('Processando áudio e gerando transcrição...'):
                    with open(caminho_video, "rb") as file:
                        transcricao = client.audio.transcriptions.create(
                            file=(caminho_video, file.read()),
                            model="whisper-large-v3",
                            response_format="text",
                            language="pt"
                        )
                
                with st.spinner('Decodificando a estrutura e criando as variações...'):
                    # Ajusta dinamicamente a parte final do prompt baseado no jogo digitado
                    if nome_jogo:
                        instrucao_jogo = f"""
## 🛠️ SUAS 3 VARIAÇÕES ADAPTADAS PARA O JOGO: {nome_jogo.upper()}
Crie 3 roteiros curtos (Ganchos + Construção) idênticos à estrutura desse vídeo, mas aplicados inteiramente ao contexto, dores, memes ou curiosidades do jogo **{nome_jogo}** para que o usuário possa apenas gravar.
"""
                    else:
                        instrucao_jogo = """
## 🛠️ SUAS 3 VARIAÇÕES PRONTAS PARA USAR
Crie 3 roteiros curtos (Ganchos + Construção) idênticos à estrutura desse vídeo, prontos para o usuário preencher, aplicados a 3 nichos genéricos diferentes e lucrativos.
"""
                    
                    prompt_final = prompt_analise + instrucao_jogo
                    
                    chat_completion = client.chat.completions.create(
                        messages=[{"role": "user", "content": f"{prompt_final}\n\nTexto transcrito do vídeo:\n{transcricao}"}],
                        model="llama-3.3-70b-versatile",
                    )
                    resposta = chat_completion.choices[0].message.content
                
                # --- Organização em Abas ---
                st.markdown("### 📊 Resultados Encontrados")
                aba_analise, aba_texto = st.tabs(["✨ Estrutura da Copy", "🗣️ Transcrição Completa"])
                
                with aba_analise:
                    st.markdown(resposta)
                    
                with aba_texto:
                    st.info(transcricao)
                
                os.remove(caminho_video)
                
            except Exception as e:
                st.error(f"❌ Erro interno: {e}")
                if os.path.exists(caminho_video):
                    os.remove(caminho_video)
