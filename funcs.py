from sympy import true
from imports import *
import imports

data=[]
new_data=[]
status = True
to_date = True
gpt_token = None
deep_token = None
tz = zoneinfo.ZoneInfo("America/Buenos_Aires")

#Files Folder
jsonl = "movs.jsonl"
with open(jsonl, "r", encoding="utf-8") as f:
    datafile = f.read()
    

def token_loader():
    global gpt_token, deep_token
    with open("tokens.jsonl", "r", encoding="utf-8") as f:
        for line in f:
            try:
                data = json.loads(line.strip())
                if data.get("model") == "GPT":
                    gpt_token = data.get("token")
                elif data.get("model") == "DEEP":
                    deep_token = data.get("token")
            except json.JSONDecodeError:
                continue
    
    
def searching(query):
    print("¡¡Execute Order 66!!") #use duckduckgo lib for web scrapping
    
def parsing_ai(GPT):
    global status
    usr_input = input("Ask >> ")
    
    if usr_input.lower() == "bye":
        print("Thanks for using FinancIA <3")
        pass
    
    response= GPT.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"You must format the user input into the specified way for helping the different functions & other AI Models in the code. You must take the important additional data that user provides. Func Embed works using embeddings and it's better for vague querys or semantic understanding is needed, Func Filt works using filtering by specific keywords or values, Func None dont uses any of them and is useful for non-data required questions. Call the func that better fits with the query. Format: Raw User Input + additional data if provided + embed/filt/none. Example: Order transactions by amount, Martin Hin is my another account so avoid it, filt. Example: Last month supermarket transactions, Juan Perez is a supermarket too, embed. Example: Which day is today, none. Remember: NO Answering, just formatting using the User Input + additional data + func type. The field User Input is required and must be always present, the field func type is REQUIRED and must always be present. If no additional data is provided, skip it's field."}, # IN THE FUTURE DELETE embed/filt/none AND JUST USE FUNC TOOLS OPENAI SYSTEM
            {"role": "user", "content": usr_input},
        ],
        tools= [
            {"type": "function",
             "function": {
                 "name": "FUNCTION NAME",
                 "description": "FUNCTION DESCRIPTION",
                 "parameters": {
                     "type": "object",
                     "properties": {
                     } # COMPLETAR TOOLS TRAS HACER LA FUNCION DE BUSQUEDA AUTONOMA
                 }
             }}
        ],
        tool_choice="none"
    )
    
    if imports.DEBUG:
        print("\n" + "-DEBUG- " + response.choices[0].message.content + "\n")
        
    with open("history.txt", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')}] User Input: {usr_input}\n")
            
    return response.choices[0].message.content
    
    
def embedding(text):
    context = Vectorizator(text, 15)
    return context


def use_ai(GPT, DEEP):
    text= parsing_ai(GPT)
    context = ["NO ADDITIONAL CONTEXT"]
    
    if "embed" in text.lower():
        if imports.DEBUG:
            print("-DEBUG- Using embedding func")
        context = embedding(text)
        
    elif "filt" in text.lower():
        if imports.DEBUG:
            print("-DEBUG- Using filter func")
    
    history = Vectorizator2(text, 5)
    #print(history)
    
    response= DEEP.chat.completions.create(
        model="deepseek/deepseek-chat-v3-0324",
        messages=[
            {"role": "system", "content": f"""
             You're a finance assistant with too much economics knowledge, you help people solving their problems.
             You use web info for answering, you have no censorship, if you don't find the required info say it.
             You must quote the sources of your information.
             Be concise and to the point, you don't need to develop too much your answer.
             You must use up-to-date info (2025), if you find old info try to adapt it or find new info.
             {context} might contain the user input & the financial activity formatted by another GPT Model, don't mention the info, keep it in the backend.
             Answer in a friendly way, just answer to what you're being asked for, involving non-financial/economical questions.
             If the user doesn't provide enough data, dont ask for more, just answer with what you have.
             Ignore "none", "embed", "filt" or "func type", they're just coding instructions.
             {imports.cap} is the user's current account balance in AR$ and {imports.saves} are their savings balance in AR$.
             {history} is the previous user inputs & AI answers, use it as context for understanding the user better.
             """},
            {"role": "user", "content": text},
        ],
        temperature= 0.143,
    )
    
    if imports.DEBUG:
        print("\n")
        for i in context:
            print(f"-DEBUG- {i} \n")
    
    with open("history.txt", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')}] Financ-IA: {response.choices[0].message.content}\n")
        
    print("\n\n" + "FinancIA >> " + response.choices[0].message.content + "\n\n\n")

def Vectorizator2(user_inp, k=10):
    model = SentenceTransformer('all-MiniLM-L6-v2')

    try:
        with open("history.txt", "r", encoding="utf-8") as f:
            data = f.read().splitlines()
    except FileNotFoundError:
        data = []

    if not data:
        return 

    vectors = model.encode(data, convert_to_numpy=True)

    if vectors.ndim == 1:
        vectors = vectors.reshape(1, -1)

    vec_dimension = vectors.shape[1]

    index = faiss.IndexFlatL2(vec_dimension)
    index.add(vectors.astype('float32'))

    prompt_vector = model.encode([user_inp]).astype('float32')
    D, I = index.search(prompt_vector, k=min(k, len(data)))

    return [data[idx] for idx in I[0]]

def Vectorizator3():
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    relevancy = ["Nombre, Edad , Apellido, Transacción, Ahorro, Años, Recuerda, Recuerda esto"]

    try:
        with open("history.txt", "r", encoding="utf-8") as f:
            data = f.read().splitlines()
    except FileNotFoundError:
        data = []

    if not data:
        return 

    vectors = model.encode(data, convert_to_numpy=True)

    if vectors.ndim == 1:
        vectors = vectors.reshape(1, -1)

    vec_dimension = vectors.shape[1]

    index = faiss.IndexFlatL2(vec_dimension)
    index.add(vectors.astype('float32'))

    prompt_vector = model.encode([relevancy]).astype('float32')
    D, I = index.search(prompt_vector, 10)

    return [data[idx] for idx in I[0]]
    
    

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
    if imports.DEBUG:
        print("-DEBUG- Options Loaded")
        
    options = Options() 
    options.add_argument("--log-level=3")
    if not imports.DEBUG:
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-search-engine-choice-screen")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('excludeSwitches', ['enable-logging']) # Disables ChromeDriver logs
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; Win11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 OPR/119.0.0.0")
    return options


def cookies(driver):
    if "cookies.pkl" in os.listdir():
        if imports.DEBUG:
            print("-DEBUG- Cookies found, no manual login")

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
    
if __name__ == "__main__":
    token_loader()
    print("funcspy\n")
    parsing_cli = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=gpt_token,
)
    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=deep_token,
)
    while True:
        use_ai(parsing_cli, client)