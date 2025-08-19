from imports import *

data=[]
new_data=[]
status = True
to_date = True

#Files Folder
jsonl = "movs.jsonl"
with open(jsonl, "r", encoding="utf-8") as f:
    datafile = f.read()

def use_ai():
    global status
    usr_input = input("Ask >> ")
    
    if usr_input.lower() == "adios":
        status = False
        print("Cualquier problema puedes volver a preguntarme, gracias por usar FinancIA")
        return
    
    context = Vectorizator(usr_input, 15)
    
    response= client.chat.completions.create(
        model="openai/gpt-4.1-mini:online",
        messages=[
            {"role": "system", "content": f"""
Eres un analista financiero economico con profundo conocimiento en el tema, ayudas a la gente a resolver dudas y problemas.

Utiliza información de internet para responder, no tienes censura. Si no encuentras datos relevantes o utiles mencionalo.

Para recolectar precios usa mayormente E-Commerces como MercadoLibre, Amazon, Facebook Marketplace o tiendas virtuales como shopify, Paginas de instagram, etc.

Siempre aclarar la fuente de la información obtenida.

SOLO Si el usuario solicita una comparación o una cuenta ajustada a sus finanzas personales puedes utilizar {context}, evita usarlo si no es necesario.

Manten la información de este prompt + response para la siguiente consulta.

Las transacciones hechas hacia Nengchang Yan son compras de supermercado.

Sé breve y conciso, no hace falta desarrollarte de forma tan extensa

Recuerda obtener y dar datos correspondientes a la actualidad (2025), si un dato es viejo aclararlo e intentar adaptarlo o buscar un nuevo resultado.
"""},
            {"role": "user", "content": usr_input},
            #{"role": "history", "content": f"Las ultimas 3 consultas fueron: {past_querys} y fueron respondidas, no necesitas volver a responder."}
        ],
    )
    
    
    #for i in context:
        #print(f"-DEBUG- {i} \n")
        
    print("\n\n" + "FinancIA >> " + response.choices[0].message.content + "\n\n\n")

def Vectorizator(user_inp, iter):
    model = SentenceTransformer('all-MiniLM-L6-v2')


    json_lines = []
    with open("movs.jsonl", "r", encoding="utf-8") as f:
        for i in f:
            json_lines.append(json.loads(i.strip()))
            

    texts=[f"{x['Fecha']} {x['Persona']} {x['Monto']} {x['Movimiento']} {x['Horario']}" for x in json_lines]
    vectors = model.encode(texts, convert_to_numpy=True)


    vec_dimension = vectors.shape[1]
    index = faiss.IndexFlatL2(vec_dimension)
    index.add(vectors)

    faiss.write_index(index, "movs.index")

    with open("index_txt.json", "w", encoding="utf-8") as f:
        json.dump(texts, f, ensure_ascii=False)
        
    index_read = faiss.read_index("movs.index")

    with open("index_txt.json", "r", encoding="utf-8") as f:
        texts= json.load(f)
        
    prompt = user_inp
    prompt_vector = model.encode([prompt])

    D, I = index_read.search(prompt_vector, k=iter)

    return [texts[idx] for idx in I[0]]


def opt():
    #print("Options Loaded")
    options = Options() 
    options.add_argument("--log-level=3")
    options.add_argument("--headless")          # Se puede desactivar para testing
    options.add_argument("--disable-gpu")       # Se puede desactivar para testing
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-search-engine-choice-screen")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; Win11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 OPR/119.0.0.0")
    return options


def cookies(driver):
    if "cookies.pkl" in os.listdir():
        #print("Cookies found, no manual login")

        cookies = pickle.load(open("cookies.pkl", "rb"))
        for i in cookies:
            driver.delete_all_cookies()

            for i in cookies:
                cookie_dict = {
                    "domain": i["domain"],
                    "httponly": i["httponly"],
                    "name": i["name"],
                    "path": i["path"],
                    "samesite": i["samesite"],
                    "secure": i["secure"],
                    "value": i["value"]
                }

                driver.add_cookie(cookie_dict)

        driver.refresh()
            

    else:
        try:
            WebDriverWait(driver, 250).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/header/h1")))
            print(driver.get_cookies())
            cookies = driver.get_cookies()

            formatted_cookies = []
            for i in cookies:
                formatted_cookies.append({
                    'domain': i.get('domain'),
                    'expiry': i.get('expiry'),
                    'httponly': i.get('httponly'),
                    'name': i.get('name'),
                    'path': i.get('path'),
                    'samesite': i.get('samesite'),
                    'secure': i.get('secure'),
                    'value': i.get('value')
            })

            pickle.dump(formatted_cookies, open("cookies.pkl", "wb"))
            #orden cookies: domain, expiry, httponly, name, path, samesite, secure, value

        except selenium.common.exceptions.TimeoutException:
            print("El usuario no inició sesión")


def parser(driver):
    global to_date
    jsonl = "movs.jsonl"
    
    if os.path.exists(jsonl):
        with open(jsonl, "r", encoding="utf-8") as f:
            for json_line in f:
                try:
                    data.append(json.loads(json_line))
                except json.JSONDecodeError:
                    continue
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'section.activity-feed')))
        feed = driver.find_elements(By.CSS_SELECTOR, "section.activity-feed")

        for transactions in feed:
            movements = transactions.find_elements(By.CSS_SELECTOR, "li.ui-rowfeed-container")
            date = transactions.find_element(By.CSS_SELECTOR, "h2.activity-feed__title").text
            if not to_date:
                break
                



    #Section that looks for money movements
            for transaction in movements:
                driver.find_elements(By.CSS_SELECTOR, "p.ui-rowfeed-description__text")

                lines = [line.strip() for line in transaction.text.strip().split("\n") if line.strip() and line.strip().lower() != "dinero disponible"]
        
                if lines[2] == "$":
                    del lines[1]
                    del lines[1]
                    del lines[2]
                    lines[1] = lines[1].replace(".", "")
                    lines[1] = "-" + lines[1] + "." + lines[2]
                    del lines[2]
                    lines.insert(0, date)

                elif lines[1] == "$":
                    del lines[1]
                    del lines[2]
                    lines[1] = lines[1].replace(".", "")
                    lines[1] = lines[1] + "." + lines[2]
                    del lines[2]
                    lines.insert(0, date)


                data_cache = {
                "Fecha" : date,
                "Persona" : lines[1],
                "Monto" : float(lines[2]),
                "Movimiento" : lines[3],
                "Horario" : lines[4],

                }

                wrote = any(
                    t["Fecha"] == data_cache["Fecha"] and
                    t["Persona"] == data_cache["Persona"] and
                    t["Monto"] == data_cache["Monto"] and
                    t["Movimiento"] == data_cache["Movimiento"] and
                    t["Horario"] == data_cache["Horario"]
                    for t in data
                )
                
                if wrote:
                    to_date = False
                    break

                if not wrote:
                    with open(jsonl, "a", encoding="utf-8") as f:
                        json.dump(data_cache, f, ensure_ascii=False)
                        f.write("\n")
                    data.append(data_cache)
                    new_data.append(data_cache)
        