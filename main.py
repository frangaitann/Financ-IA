from imports import *
from funcs import *
import funcs

# EL HIJO DE MIL PUTAS DE LAUTY, SE DIO CUENTA QUE SI YO TENGO UN PRESTAMO O ALGO A PAGAR A UNA FECHA FUTURA DENTRO DEL MISMO MES EL BOT NO LA ANALIZARÁ YA QUE EL PAGO NO FUE HECHO: POR ESTO MISMO HAY QUE CATEGORIZAR LOS INGRESOS Y EGRESOS EN "COMPRAS" "SERVICIOS" "COBROS" "PRESTAMOS O CREDITOS" "TRANSFERENCIAS"

# SUMA TOTAL DA ERROR, NO PONER APPEND.NEW_DATA PORQUE CONVIERTE DATA EN LISTA Y ARROJA ERROR

# AGREGAR QUE PUEDA LEER EL CAPITAL QUE SE POSEÉ ACTUALMENTE

# AGREGAR HISTORIAL A LA IA PARA RECORDAR CONTEXTO DE LA CHARLA

# VER COMO CATEGORIZAR NENGCHAN YAN COMO VECTOR RELACIONADO A LAS COMPRAS

# HACER WEB SCRAPPING + EMBEDDING PARA CONSULTAR DATOS ONLINE, el :online NO FUNCIONA CORRECTAMENTE

# En resumidas cuentas, el response debe separarse en EL coloquial (el que lee el usuario) y el de busqueda (el que busca con la API de duckduckgo) para responder al usuario y al mismo tiempo buscar la respuesta


def main():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

    #print("Starting Navigator")

    options = opt()

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    
    print(r"""
  ______ _                        _____          
 |  ____(_)                      |_   _|   /\    
 | |__   _ _ __   __ _ _ __   ___  | |    /  \   
 |  __| | | '_ \ / _` | '_ \ / __| | |   / /\ \  
 | |    | | | | | (_| | | | | (__ _| |_ / ____ \ 
 |_|    |_|_| |_|\__,_|_| |_|\___|_____/_/    \_\ V 1.0.0                        
 """)
    
    print("Si es la primera vez que abres FinancIA tardará unos minutos en cargar...")
    #print("Starting MP")
    if "cookies.pkl" in os.listdir():
        driver.get('https://www.mercadopago.com.ar')
    else:
        driver.get("www.mercadolibre.com/jms/mla/lgz/login?platform_id=MP&go=https%3A%2F%2Fwww.mercadopago.com.ar%2F&loginType=explicit")

    cookies(driver)

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="drawer-trigger"]')))

    driver.get("https://www.mercadopago.com.ar/activities#from-section=menu")
    
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="appDesktop"]')))
    
    pages_btns = driver.find_elements(By.CSS_SELECTOR, "li.andes-pagination__button")
    
    max_page= 0
    #print("Obtaining transactions data...")
    for i in pages_btns:
        try:
            btn_text = i.text.strip()
            if btn_text.isdigit():
                page_number = int(btn_text)
                if page_number > max_page:
                    max_page = page_number
        except:
            pass
    
    current_page = 1
 
    for i in range(1, max_page+1):
        if funcs.to_date == False:
            break
        try:
            parser(driver)
            
            next_page = driver.find_element(By.XPATH, f"//li[@class='andes-pagination__button']//a[text()='{current_page+1}']")
            current_page +=1
            next_page.click()
        except ValueError:
            print("El numero de pagina no existe")
            break
        except NoSuchElementException:
            print("Todos los movimientos han sido obtenidos")

    driver.close()
    #print("Data obtained, cleaning Terminal...")
    time.sleep(10)
    
    os.system("cls")
    while funcs.status:
        use_ai()
        
    time.sleep(15)
    

if __name__ == "__main__":
    main()