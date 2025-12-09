import streamlit as st
import google.generativeai as genai

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Mi App IA", page_icon="📱")

st.title("🤖 Chat Privado")

# CONFIGURACIÓN DE LA LLAVE DE SEGURIDAD
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("Falta la API Key. Configúrala en Streamlit Secrets.")
    st.stop()

# HISTORIAL DE CHAT
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# INPUT DEL USUARIO
if prompt := st.chat_input("Escribe tu mensaje..."):
    # Guardar y mostrar mensaje usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # LÓGICA DE GEMINI
    try:
        # --- AQUÍ VA TU PERSONALIZACIÓN ---
        # Si tienes instrucciones de sistema en AI Studio, ponlas aquí dentro:
        instrucciones = """
        Eres un asistente útil y amable.
        """
        # ----------------------------------
        
        model = genai.GenerativeModel(
            model_name='gemini-2.5-flash', # ¡NUEVO NOMBRE DE MODELO!
            system_instruction=instrucciones
        )
        
        with st.chat_message("assistant"):
            with st.spinner('Pensando...'):
                response = model.generate_content(prompt)
                st.markdown(response.text)
        
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        
    except Exception as e:
        st.error(f"Error de conexión: {e}")
