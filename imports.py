from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, TimeoutException, InvalidArgumentException, ElementClickInterceptedException
from pywinauto import Desktop
from openai import OpenAI
from sentence_transformers import SentenceTransformer
import selenium.common.exceptions
import selenium.webdriver
import os
import glob
import time
import pickle
import json
import faiss
import requests
import numpy as np
import pandas as pd
from io import StringIO

DEBUG = False

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="KEY_HERE", # MUST USE YOUR OWN OPENROUTER KEY
)

parsing_cli = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="KEY_HERE", # MUST USE YOUR OWN OPENROUTER KEY
)

