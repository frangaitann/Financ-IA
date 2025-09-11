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


cap = 0
saves = 0
DEBUG = False

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
)

parsing_cli = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
)

