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
import selenium.common.exceptions, datetime, selenium.webdriver, os, glob, time, pickle, json, faiss, requests, numpy as np, pandas as pd, zoneinfo
from io import StringIO

cap = None
saves = None
DEBUG = False

