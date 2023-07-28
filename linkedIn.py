from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import parameters, csv, os.path, time
from random import randint
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

current = 1

def save_log(text):
    with open('connections.csv', 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(text)

# Functions
def search_and_send_request(keywords, till_page, ignore_list=[]):
    for page in range(1, till_page + 1):
        print('\nINFO: Checking on page %s' % (page))
        query_url = 'https://www.linkedin.com/search/results/people/?keywords=' + keywords + '&origin=GLOBAL_SEARCH_HEADER&page=' + str(page)
        driver.get(query_url)
        time.sleep(5)
        html = driver.find_element(By.TAG_NAME, 'html')
        html.send_keys(Keys.END)
        time.sleep(5)
        linkedin_urls = driver.find_elements(By.CLASS_NAME, 'reusable-search__result-container')
        print('INFO: %s connections found on page %s' % (len(linkedin_urls), page))
        for index, result in enumerate(linkedin_urls):
            text = result.text.split('\n')[0]
            if text in ignore_list or text.strip() in ignore_list:
                print("%s ) IGNORED: %s" % (index, text))
                continue
            connection_action = result.find_elements(By.CLASS_NAME, 'artdeco-button__text')
            if connection_action:
                connection = connection_action[0]
            else:
                print("%s ) BUTTON_OFF: %s" % (index, text))
                continue

            if connection.text == 'Connect' or connection.text == 'Follow' or connection.text == 'Pending':
                coordinates = connection.location_once_scrolled_into_view  # returns dict of X, Y coordinates
                driver.execute_script("window.scrollTo(%s, %s);" % (coordinates['x'], coordinates['y']))
                time.sleep(5)
                # connection.click()
                try:   

                    if driver.find_elements(By.CLASS_NAME, 'entity-result__item')[index]:
                        # driver.find_elements(By.CLASS_NAME, 'artdeco-button--primary')[0].click()
                        driver.find_elements(By.CLASS_NAME, 'entity-result__item')[index].find_elements(By.CLASS_NAME, 'app-aware-link')[0].send_keys(Keys.CONTROL, Keys.ENTER)
                        time.sleep(randint(2,5))
                        driver.switch_to.window(driver.window_handles[1])
                        time.sleep(randint(30,60))
                        driver.execute_script("window.scrollTo(0, 2000)")
                        time.sleep(randint(10,20))
                        driver.close()

                        driver.switch_to.window(driver.window_handles[0])

                        visited_profile = [
                        "Perfil visitado!",    
                        result.text.split("\n")[0],
                        result.text.split("\n")[1],
                        result.text.split("\n")[2],
                        result.text.split("\n")[3],
                        result.text.split("\n")[4],
                        result.text.split("\n")[5],
                        result.text.split("\n")[6],
                        result.text.split("\n")[7],
                        result.text.split("\n")[8],
                        ]
                        
                        save_log(visited_profile)
                        print("%s ) VISITED_PROFILE: %s" % (index, text))

                        continue
                    
                    # driver.find_elements(By.CLASS_NAME, 'artdeco-modal__dismiss')[0].click()
                    # print("%s ) CANT: %s" % (index, text))
                except Exception as e:
                    print('%s ) ERROR: %s' % (index, text))
                time.sleep(5)

            # elif connection.text == 'Follow':
            #     try:
            #         coordinates = connection.location_once_scrolled_into_view  # returns dict of X, Y coordinates
            #         driver.execute_script("window.scrollTo(%s, %s);" % (coordinates['x'], coordinates['y']))
            #         time.sleep(5)
            #         connection.click()
            #         time.sleep(5)
            #         if driver.find_elements(By.CLASS_NAME, 'artdeco-button--primary')[0].is_enabled():
            #             driver.find_elements(By.CLASS_NAME, 'artdeco-button--primary')[0].click()
                        
            #             save_log([text])
            #             print("%s ) SENT: %s" % (index, text))
            #         else:
            #             driver.find_elements(By.CLASS_NAME, 'artdeco-modal__dismiss')[0].click()
            #             print("%s ) CANT: %s" % (index, text))
            #     except Exception as e:
            #         print('%s ) ERROR: %s' % (index, text))
            #     time.sleep(5)
            
            elif connection.text == 'Accept':    
                try:
                    coordinates = connection.location_once_scrolled_into_view  # returns dict of X, Y coordinates
                    driver.execute_script("window.scrollTo(%s, %s);" % (coordinates['x'], coordinates['y']))
                    time.sleep(5)
                    connection.click()
                    time.sleep(5)
                    if driver.find_elements(By.CLASS_NAME, 'artdeco-button--primary')[0].is_enabled():
                        
                        new_contact_accept = [{
                            "name": result.text.split("\n")[0],
                            "connection": result.text.split("\n")[3],
                            "office": result.text.split("\n")[4],
                            "location": result.text.split("\n")[5],
                            "outhers": [
                                result.text.split("\n")[6],
                                result.text.split("\n")[7],
                                result.text.split("\n")[8]
                            ]
                        }]

                        new_contact_accept_csv = [
                            "Conexão com contato aceita!",
                            result.text.split("\n")[0],
                            result.text.split("\n")[1],
                            result.text.split("\n")[2],
                            result.text.split("\n")[3],
                            result.text.split("\n")[4],
                            result.text.split("\n")[5],
                            result.text.split("\n")[6],
                            result.text.split("\n")[7],
                            result.text.split("\n")[8],
                            ]
                        
                        save_log(new_contact_accept_csv)
                        print("%s ) CONNECTED: %s" % (index, text))

                        continue
                    else:
                        driver.find_elements(By.CLASS_NAME, 'artdeco-modal__dismiss')[0].click()
                        print("%s ) CANT: %s" % (index, text))
                except Exception as e:
                    print('%s ) ERROR: %s' % (index, text))
                time.sleep(5)
            
            else:
                if text:
                    print("%s ) IGNORED: %s" % (index, text))
                else:
                    print("%s ) ERROR: You might have reached limit" % (index))

try:
    # Login
    # Selenium argumentos
    dir_path = os.getcwd()
    profile = os.path.join(dir_path, "profile", "wpp")
    options = Options()
    #options.add_argument('headless')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument("disable-infobars")
    options.add_argument("disable-gpu")
    options.add_argument("log-level=3")
    options.add_argument(r"user-data-dir={}".format(profile))
    # driver = webdriver.Chrome('chromedriver.exe', options=options)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get('https://www.linkedin.com/login')
    time.sleep(4)

    # Adds the cookie into current browser context
    try:
        driver.find_element('id', 'username')
        driver.find_element('id', 'username').send_keys(parameters.linkedin_username)
        driver.find_element('id', 'password').send_keys(parameters.linkedin_password)
        time.sleep(2)
        driver.find_element('xpath', '//*[@type="submit"]').click()
    except:
        pass

    # CSV file loging
    file_name = parameters.file_name
    file_exists = os.path.isfile(file_name)

    ignore_list = parameters.ignore_list
    if ignore_list:
        ignore_list = [i.strip() for i in ignore_list.split(',') if i]
    else:
        ignore_list = []

    # Search
    search_and_send_request(keywords=parameters.keywords, till_page=parameters.till_page,
                            ignore_list=ignore_list)
except KeyboardInterrupt:
    print("\n\nINFO: User Canceled\n")
except Exception as e:
    print('ERROR: Unable to run, error - %s' % (e))
finally:
    # Close browser
    driver.quit()
