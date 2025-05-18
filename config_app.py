import streamlit as st
from google import genai
import os
from dotenv import load_dotenv

from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import cv2
from PIL import Image
import io
from google.genai import types

load_dotenv()

##### CONFIGURAÇÕES DA API
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
MODEL_NAME = 'gemini-2.5-flash-preview-04-17' # 'gemini-2.0-flash-exp'

client = genai.Client(api_key=GOOGLE_API_KEY)