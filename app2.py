import streamlit as st
from groq import Groq
import yt_dlp
import os

# --- Configuração da Interface (Streamlit) ---
st.set_page_config(page_title="Analisador de Copys TikTok", page_icon="📝", layout="centered")

st.title("📝 Analisador de Roteiros e Ganchos")
st.markdown("Cole o link do TikTok para transcrever o áudio e extrair a estrutura de retenção perfeita.")

# SISTEMA DE SEGURANÇA DE CHAVE
# Se você colocar sua chave nos "Secrets" do Streamlit, o app usa ela direto. 
# Se não colocar, ele pede para o usuário digitar uma chave na tela.
if "GROQ_API_KEY" in st.secrets:
    api_key = st.secrets["GROQ_API_KEY"]
else:
    api_key = st.text_input("Cole sua API Key da Groq aqui (gsk_...):", type="password")

url_tiktok = st.text_input("Link do vídeo do TikTok:")

# --- O Prompt Especialista em TikTok ---
prompt_analise = """
Você é um Engenheiro de Retenção e Copywriter sênior focado em crescimento no TikTok.
Sua missão é pegar a transcrição do vídeo e transformá-la em um TEMPLATE DE ESTRUTURA VIRAL pronto para ser copiado e adaptado.

Gere o relatório formatado rigorosamente seguindo esta estrutura:

## 🪝 1. O GANCHO CAMPEÃO (0 a 3 segundos)
* **Texto Exato Usado:** "[Cole aqui a frase exata do criador]"
* **Gatilho Mental Dominante:** (Ex: curiosidade, dor urgente, quebra de padrão)
* **Análise de Ritmo:** Por que esse texto forçou o usuário a parar o scroll?

## 📈 2. A CONSTRUÇÃO (Buildup)
* **Estratégia de Retenção:** Como o criador segurou o interesse logo após o gancho? (Ele fez uma promessa? Gerou um mistério?).
* **Sugestão de Quebra de Padrão:** Indique em qual segundo exato deste bloco você deve colocar um corte, zoom ou inserção de texto na tela para reter o público.

## 💎 3. A ENTREGA (Outcome)
* **Resumo da Entrega:** Como o vídeo entregou o valor prometido de forma rápida e sem enrolação? 
* **Fórmula do Conteúdo:** Extraia a lógica por trás da explicação (Ex: Problema -> Solução Direta, Antes -> Depois).

## 📢 4. CHAMADA PARA AÇÃO (CTA)
* **Comando Final:** Qual comando foi dado?
* **Otimização de Algoritmo:** Sugira como reescrever essa CTA focando estritamente em **Salvar** ou **Compartilhar** (que são as métricas que mais distribuem vídeos hoje).

---

## 🛠️ SUAS 3 VARIAÇÕES PRONTAS PARA USAR
Crie 3 roteiros curtos (Ganchos + Construção) idênticos à estrutura desse vídeo, prontos para o usuário preencher, aplicados a 3 nichos diferentes e lucrativos.
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

if st.button("Analisar Roteiro 🚀"):
    if not api_key:
        st.warning("⚠️ Por favor, insira uma chave da Groq válida.")
    elif not url_tiktok:
        st.warning("⚠️ Cole um link do TikTok para analisar.")
    else:
        with st.spinner('Baixando o áudio do vídeo...'):
            caminho_video = baixar_video(url_tiktok)
            
        if caminho_video is None:
            st.error("❌ Erro ao acessar o vídeo. O link pode estar quebrado ou o TikTok bloqueou o acesso.")
        else:
            try:
                client = Groq(api_key=api_key)
                
                with st.spinner('Ouvindo e transcrevendo o vídeo...'):
                    with open(caminho_video, "rb") as file:
                        transcricao = client.audio.transcriptions.create(
                            file=(caminho_video, file.read()),
                            model="whisper-large-v3",
                            response_format="text",
                            language="pt"
                        )
                
                st.subheader("🗣️ Texto Transcrito do Vídeo:")
                st.info(transcricao)
                
                with st.spinner('Destrinchando a estrutura perfeita do TikTok...'):
                    chat_completion = client.chat.completions.create(
                        messages=[{"role": "user", "content": f"{prompt_analise}\n\nTexto:\n{transcricao}"}],
                        model="llama-3.3-70b-versatile",
                    )
                    resposta = chat_completion.choices[0].message.content
                
                st.success("Análise de Estrutura Concluída!")
                st.markdown("---")
                st.markdown(resposta)
                
                os.remove(caminho_video)
                
            except Exception as e:
                st.error(f"❌ Erro na análise: {e}")
                if os.path.exists(caminho_video):
                    os.remove(caminho_video)