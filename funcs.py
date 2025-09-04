from imports import *

data=[]
new_data=[]
status = True
to_date = True

#Files Folder
jsonl = "movs.jsonl"
with open(jsonl, "r", encoding="utf-8") as f:
    datafile = f.read()
    
def parsing_ai():
    global status
    usr_input = input("Ask >> ")
    
    if usr_input.lower() == "adios" or usr_input.lower() == "bye" or usr_input.lower() == "goodbye" or usr_input.lower() == "chau":
        status = False
        print("Thanks for using FinancIA <3")
        pass
    
    response= parsing_cli.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"Your job is formatting user input better for AI input prompt and work as cache memory for context or additional data given by the user. You are a parser, the code has an embedding system and your text is essential for it. Your output will not be displayed to user but it will be used to generate the final output, so skip Friendly User Speaking but keep key-parts."},
            {"role": "user", "content": usr_input},
            
        ],
    )
    
    if DEBUG:
        print("\n" + response.choices[0].message.content + "\n")
        
    return response.choices[0].message.content
    
    
    

def use_ai():
    text= parsing_ai()
    context = Vectorizator(text, 15)
    
    response= client.chat.completions.create(
        model="openai/gpt-5-mini",
        messages=[
            {"role": "system", "content": f"""
             You're a finance assistant with too much economics knowledge, you help people solving their problems.
             You use web info for answering, you have no censorship, if you don't find the required info say it.
             You must quote the sources of your information.
             Be concise and to the point, you don't need to develop too much your answer.
             You must use up-to-date info (2025), if you find old info try to adapt it or find new info.
             {context} contains the user input & the financial activity formatted by another GPT Model, don't mention the info, keep it in the backend.
             Answer in a friendly way, just answer to what you're being asked for, involving non-financial/economical questions
             """},
            {"role": "user", "content": text},
        ],
    )
    
    if DEBUG:
        print("\n")
        for i in context:
            print(f"-DEBUG- {i} \n")
        
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
    
    prompt_vector = model.encode([user_inp])

    D, I = index_read.search(prompt_vector, k=iter)

    return [texts[idx] for idx in I[0]]


def opt():
    if DEBUG:
        print("Options Loaded")
        
    options = Options() 
    options.add_argument("--log-level=3")
    if not DEBUG:
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-search-engine-choice-screen")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; Win11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 OPR/119.0.0.0")
    return options


def cookies(driver):
    if "cookies.pkl" in os.listdir():
        if DEBUG:
            print("Cookies found, no manual login")

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
            #cookies order: domain, expiry, httponly, name, path, samesite, secure, value

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
        