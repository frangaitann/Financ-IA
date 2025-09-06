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

    options = opt()

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    
    print(r"""
  ______ _                        _____          
 |  ____(_)                      |_   _|   /\    
 | |__   _ _ __   __ _ _ __   ___  | |    /  \   
 |  __| | | '_ \ / _` | '_ \ / __| | |   / /\ \  
 | |    | | | | | (_| | | | | (__ _| |_ / ____ \ 
 |_|    |_|_| |_|\__,_|_| |_|\___|_____/_/    \_\ V 1.4.0                        
 """)
    
    print("If it's the first time starting FinancIA it will last a little bit more to load...")
    
    if input("\n\n Press Enter to continue... ").lower() == "deb":
        imports.DEBUG = True
        DEBUG = True
        print("\n-DEBUG- DEBUG Mode")
    
    if DEBUG:
        print("-DEBUG- Starting MP")

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
    if DEBUG:
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
    if DEBUG:
        print("-DEBUG- Data obtained, cleaning Terminal...")
    time.sleep(10)
    
    os.system("cls")
    while funcs.status:
        use_ai()
        
    time.sleep(15)
    

if __name__ == "__main__":
    main()