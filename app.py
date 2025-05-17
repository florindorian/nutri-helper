import streamlit as st
from google import genai
import os
from dotenv import load_dotenv

from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import cv2
from PIL import Image
import io
from google.genai import types


from config_app import MODEL_NAME, client

##### FUNÇÕES E CLASSES
class VideoTransformer(VideoTransformerBase):
    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        return img

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
                    mime_type='image/*',
                ),
                'Imagem com conteúdo textual'
            ]
        )
        return response.text
    except Exception as e:
        return f"Erro ao processar a imagem: {e}"

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
    <p style='text-align: center; color: orange; font-weight: bold; font-size: 40px;'>Nutri-Helper</p>
    """, 
    unsafe_allow_html=True)

st.markdown("""
    <p style='text-align: center;'>
    "Seu assistente de IA nutricional"
    </p>
    <p style='text-align: center;'>
    Pergunte, envie fotos e PDFs e aprenda com o Nutri-Helper
    </p>   
    """, 
    unsafe_allow_html=True)

cols_image = st.columns([1, 3, 1]) # Ajuste as proporções conforme necessário
with cols_image[1]:
    st.image(image='./images/boas-vindas-nutri-helper.png', width=None) # Remova a largura fixa aqui

##### INPUTS
user_prompt = st.text_input("Insira seu prompt:", "")

use_image = st.checkbox("Usar Imagem")
use_pdf = st.checkbox("Usar PDF")
use_camera = st.checkbox("Usar Camera")

uploaded_pdf = None
picture = None

if use_image:
    picture = st.camera_input("Tire uma foto")

if use_pdf:
    uploaded_pdf = st.file_uploader("Upload PDF (opcional)", type="pdf")

if use_camera:
  webrtc_streamer(key="webcam", video_transformer_factory=VideoTransformer)

submit_button = st.button("Analisar")


##### AÇÕES
if submit_button:
    if user_prompt:
        if picture:
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