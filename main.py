from imports import *
from funcs import *
import funcs
import imports

def main():
    global DEBUG
    
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

    
    print(r"""
  ______ _                        _____          
 |  ____(_)                      |_   _|   /\    
 | |__   _ _ __   __ _ _ __   ___  | |    /  \   
 |  __| | | '_ \ / _` | '_ \ / __| | |   / /\ \  
 | |    | | | | | (_| | | | | (__ _| |_ / ____ \ 
 |_|    |_|_| |_|\__,_|_| |_|\___|_____/_/    \_\ V 1.5.1                        
 """)
    
    print("If it's the first time starting FinancIA it will last a little bit more to load...")
    
    if input("\n\n Press Enter to continue... ").lower() == "deb":
        imports.DEBUG = True
        print("\n-DEBUG- DEBUG Mode")
    
    if imports.DEBUG:
        print("-DEBUG- Starting MP")
        
    options = opt()

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    if "cookies.pkl" in os.listdir():
        driver.get('https://www.mercadopago.com.ar')
    else:
        driver.get("www.mercadolibre.com/jms/mla/lgz/login?platform_id=MP&go=https%3A%2F%2Fwww.mercadopago.com.ar%2F&loginType=explicit")

    cookies(driver)

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="drawer-trigger"]')))
    
    inter_caps_list = driver.find_elements(By.CSS_SELECTOR, "span.andes-money-amount__fraction")
    cents_caps_list = driver.find_elements(By.CSS_SELECTOR, 'span[class*="andes-money-amount__cents--superscript-"]')
    
    imports.cap = float(inter_caps_list[0].text.replace(".","") + "." + cents_caps_list[0].text)
    imports.saves = float(inter_caps_list[3].text.replace(".","") + "." + cents_caps_list[3].text)
    if imports.DEBUG:
        print("\n-DEBUG- INTER_CAP " + inter_caps_list[0].text)
        print("-DEBUG- CENTS_CAP " + cents_caps_list[0].text)
        print("-DEBUG- IMPORTS_CAP " + str(imports.cap))
        print("-DEBUG- VAR TYPE " + str(type(imports.cap)))
        
        print("\n-DEBUG- CENTS_SAVE " + cents_caps_list[3].text)
        print("-DEBUG- INTER_SAVE " + inter_caps_list[3].text.replace(".", ""))
        print("-DEBUG- IMPORTS_SAVE " + str(imports.saves))
        print("-DEBUG- VAR TYPE " + str(type(imports.saves)) + "\n")
        

    driver.get("https://www.mercadopago.com.ar/activities#from-section=menu")
    
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="appDesktop"]')))
    
    pages_btns = driver.find_elements(By.CSS_SELECTOR, "li.andes-pagination__button")
    
    max_page= 0
    if imports.DEBUG:
        print("-DEBUG- Starting Data Extraction")

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
            print("Page number doesn't exists.")
            break
        except NoSuchElementException:
            print("All transactions received.")

    driver.close()
    if imports.DEBUG:
        print("-DEBUG- Data obtained, cleaning Terminal...")
    time.sleep(10)
    
    os.system("cls")
    while funcs.status:
        use_ai()
        
    time.sleep(15)
    

if __name__ == "__main__":
    main()