import streamlit as st
from google.genai import types

from config_app import MODEL_NAME, client

##### FUNÇÕES E CLASSES
def process_prompt(prompt):
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Erro ao processar o prompt: {e}"

def process_image(image_data, prompt):
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[
                types.Part.from_bytes(
                    data=image_data,
                    mime_type=image_data.type
                ),
                'Imagem com conteúdo textual'
            ]
        )
        return response.text
    except Exception as e:
        return f"Erro ao processar a imagem: {e}"
    
def process_multiple_images(image_files, prompt):
    try:
        contents = [prompt]
        for image_file in image_files:
            image_bytes = image_file.read()
            contents.append(
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=image_file.type
                )
            )
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=contents
        )
        return response.text
    except Exception as e:
        return f"Erro ao processar múltiplas imagens: {e}"

def process_pdf(uploaded_pdf, prompt):
    pdf_bytes = uploaded_pdf.read()
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[
                prompt, 
                types.Part.from_bytes(
                    data=pdf_bytes,
                    mime_type=uploaded_pdf.type,
                )
            ]
        )
        
        return response.text
    except Exception as e:
        return f"Erro ao processar o PDF: {e}"


#################### CONSTRUÇÃO DO APP ####################
st.markdown("""
    <p style='text-align: center; color: orange; font-weight: bold; font-size: 40px;'>NutrIA-Helper 🤖</p>
    """, 
    unsafe_allow_html=True)

st.markdown("""
    <p style='text-align: center;'>
    "Seu assistente de IA nutricional"
    </p>
    <p style='text-align: center;'>
    Pergunte, envie fotos e PDFs e aprenda com o NutrIA-Helper 📊
    </p>   
    """, 
    unsafe_allow_html=True)

cols_image = st.columns([1, 3, 1]) # Ajuste as proporções conforme necessário
with cols_image[1]:
    st.image(image='./images/boas-vindas-nutri-helper.png', width=None) # Remova a largura fixa aqui

##### INPUTS
input_option = st.radio(
    "Selecione a forma de entrada:",
    ["Apenas Texto", "Upload de Imagens", "Capturar uma Imagem a partir da Câmera", "Usar PDF"],
)

uploaded_images = None
picture = None
uploaded_pdf = None
user_prompt = ""

if input_option == "Apenas Texto":
    user_prompt = st.text_input("Insira seu prompt:", "")
elif input_option == "Upload de Imagens":
    uploaded_images = st.file_uploader("Selecione as imagens", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    user_prompt = st.text_input("Insira seu prompt:", "")
elif input_option == "Capturar uma Imagem a partir da Câmera":
    picture = st.camera_input("Tire uma foto")
    user_prompt = st.text_input("Insira seu prompt:", "")
elif input_option == "Usar PDF":
    uploaded_pdf = st.file_uploader("Upload PDF (opcional)", type="pdf")
    user_prompt = st.text_input("Insira seu prompt:", "")

submit_button = st.button("Analisar")


##### AÇÕES
# Ações (o restante do seu código permanece semelhante)
if submit_button:
    if user_prompt:
        if uploaded_images:
            if uploaded_images:
                response_text = process_multiple_images(uploaded_images, user_prompt)
            else:
                st.warning("Por favor, selecione as imagens para upload.")
        elif picture:
            image_bytes = picture.read()
            response_text = process_image(image_bytes, user_prompt)
        elif uploaded_pdf:
            response_text = process_pdf(uploaded_pdf, user_prompt)
        else:
            response_text = process_prompt(user_prompt)

        st.write("Resposta do Modelo:")
        st.write(response_text)
    else:
        st.warning("Por favor, insira um prompt.")