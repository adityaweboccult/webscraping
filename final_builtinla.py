from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyvirtualdisplay import Display

from time import sleep
import pandas as pd
import os
from tqdm import tqdm

# This variable should be greater than the total companies present in a single page, e.g. if we know maximum that maximu could be present is 20 then this variable should be greater than 20
COMPANIES_PER_PAGE = 1000

# Total pages to scrape
#Total Pages 9
TOTAL_PAGES = 10
CITY = "colorado"
EXCEL_SAVING_PATH = f"excel_shared_to_scrape/third/builtinla/{CITY}"

print("Saving excel file to",EXCEL_SAVING_PATH)

main_link = "https://www.builtincolorado.com/companies/type/artificial-intelligence-companies"


# EXCEL_SAVING_PATH = "excel_shared_to_scrape/second/buitinla/buitinla_excels"


# Inorder to use the virtual display, the website pop will not open 
display = Display(visible=0, size=(800, 600))
display.start()


if not os.path.exists(EXCEL_SAVING_PATH):
    os.makedirs(EXCEL_SAVING_PATH)

# The data that is present in this website
columns = ["Name","Website","Strength","About","Founded Year","Focus Areas"]
# The data frame in which we will merge all the scraped pages data
main_df = pd.DataFrame(columns=columns)


# The starting page, here we have to give the website link as below given format
#give the website name with ?page=<page_no>
# current_page = "https://www.builtinla.com/companies/type/artificial-intelligence-companies?page=1" 

# for page in range(7,8):
for page in range(TOTAL_PAGES+1):
# 

    print("Running Page", page)

    # initializing driver
    driver = webdriver.Chrome()
    
    current_page = f"{main_link}?page={page}"
    print("Current Page URL",current_page)
    # accessing the website
    driver.get(current_page)
    driver.maximize_window()

    # try:
        
    #     next_page = driver.find_element(by = By.XPATH, value = "//li[@class='next-page']/a").get_attribute("href")
    #     print("Next page", next_page)
    #     current_page = next_page

    # except:
    #     is_end_page = True

    # pagination_driver = driver.find_elements(by = By.XPATH  , value = "//a[@class='page-link']")

    # //ul[@class='pagination justify-content-center']/li[1]

    # all_pages = [current_page.get_attribute("href") for current_page in pagination_driver]
    # page_number = [current_page.text for current_page in pagination_driver]

 


    # company_names_and_website_driver = driver.find_elements(by = By.XPATH, value = "//h2[@class='company-name']/div/a")
    # company_names_and_website_driver = driver.find_elements(by = By.XPATH, value = "//h2[@class='company-name']/div/a")
    
    # inside_websites_driver = driver.find_elements(by = By.XPATH, value = "//a[@class='visit-profile']")
    # company_websites_driver = driver.find_elements(by = By.XPATH, value = "//a[@class='visit-website web-url list-blue-link']")


    sleep(5)
    try:
        #pressing the rejecl all button, it is the first pop up
        driver.find_element(by = By.XPATH, value = "//button[@class='ot-pc-refuse-all-handler']").click()
    except:
        print("No reject button")

    sleep(3)

    inside_company_driver = driver.find_elements(by = By.XPATH, value = "//a[@class='company-logo-link']")

    # print(inside_company_driver)

    # company_names = [current.text for current in company_names_and_website_driver]
    inside_company_websites = [current.get_attribute("href") for current in inside_company_driver]
    # company_websites = [current.get_attribute("href") for current in company_websites_driver]

    # print(inside_company_websites)




    total_companies = len(inside_company_websites)
    print("total Companies", total_companies)
    print(inside_company_websites)
    # print(inside_company_websites)

    ratings = []
    people_strength = []

    all_social_links = []
    founded_year = []
    time_zones = []
    services = []
    focus_areas = []
    abouts = []
    company_websites = []
    company_names = []



    driver.close()
    sleep(5)

    try :

        COMPANIES_PER_PAGE = min(COMPANIES_PER_PAGE,total_companies)
            

        i = 0

        # for company_url in inside_company_websites[12:13]:
        # for company_url in inside_company_websites[2:3]:
            # company_url = "https://www.builtinla.com/company/aerospace-corporation"
        for company_url in tqdm(inside_company_websites[:COMPANIES_PER_PAGE]):

            

            # op = webdriver.ChromeOptions()
            # op.add_argument('headless')
            # driver = webdriver.Chrome(options=op)
            driver = webdriver.Chrome()

            # try:
            #     company_url = company_url.split("#")[0]
            # except:
            #     company_url = company_url

            print(company_url)
            driver.get(company_url)
            driver.maximize_window()

            sleep(12)

            try:
                driver.find_element(by = By.XPATH, value = "//button[@class='ot-pc-refuse-all-handler']").click()
            except:
                print("No reject button")

            sleep(1)
                
                # //button[@class="ot-pc-refuse-all-handler"]
            




            # Getting Company Name

            
            try:
                name_driver = driver.find_element(by = By.XPATH, value = "//div[@class='header-title']/h2")
                company_names.append(name_driver.text)
            except:
                company_names.append("Not Available")
                
            sleep(1)

            # Getting Company website

            try:
                website_driver = driver.find_element(by = By.XPATH, value = "//a[@class='info-item company-website-link']")
                company_websites.append(website_driver.get_attribute("href"))
            except:
                company_websites.append("Not Available")
        

            # Getting ratings

            # try:
            #     # rating_driver = driver.find_element(by = By.XPATH, value = "/html/body/main/div[2]/section[1]/section[2]/div[1]/dl/dd/div/span")
            #     rating_driver = driver.find_element(by = By.XPATH, value = "//span[@class='review-rating']")
            #     rating = float(rating_driver.text)
            # except:
            #     rating = "Not Available"

            # # ratings[i] = rating
            # ratings.append(rating)


            sleep(1)
            # Getting Strengths
            try:

                strength_driver = driver.find_elements(by=By.XPATH, value = "//div[@class='info-group employees']/p/span[2]")
                # print("Strength Driver",strength_driver)
                # print("The lenght of the strenght driver is ",len(strength_driver))

                # strength_driver = driver.find_element(by=By.XPATH, value = "//div[@class='info-group employees']/p[2]/span[2]")
                if len(strength_driver) > 1:
                    # print("Inside if strenght")
                    strength = strength_driver[1].text.replace("'","")
                else:          
                    # print("Inside strenght else")
                    
                    # print(strength_driver[0].text)
                    strength = strength_driver[0].text.replace("'","")
            except:
                strength = "Not Available"

            print(strength)

            # people_strength[i] = strength
            people_strength.append(strength)


            sleep(1)

            # Finding the Founded year
            try:
                founded_year_driver = driver.find_element(by= By.XPATH, value = "//div[@class='info-group founded']/p/span[2]")
                year = founded_year_driver.text
                
                year = int(year)

            except:
                year = "Not Available"

            # year = int(founded_year_driver.text.split()[1])    
            # founded_year[i] = year
            founded_year.append(year)

            # continue


            # Getting Focus content
            temp_focus = []
            focus_counter = 1   
            while 1:
                try:
                    focus_driver = driver.find_element(by=By.XPATH, value=f"//div[@class='industries']/ul/li[{focus_counter}]")
                    # focus_name = focus_driver.get_attribute("data-content").replace("\n"," ").replace("<i>","").replace("</i>", "")
                    focus_name = focus_driver.text
                    temp_focus.append(focus_name)
                
                except:
                    break
                focus_counter += 1
            if len(temp_focus) == 0:
                temp_focus = "Not Available"
            # focus_areas[i] = temp_focus
            focus_areas.append(temp_focus)

            sleep(5)

            # Getting About
            temp_about = []
            is_page_available = True

            # Clicking on the read more button to load all the about content
            try:             
                driver.implicitly_wait(5)
                sleep(2)
                print("Trying to click the Read more")  
                driver.find_element(by=By.XPATH, value = "//button[@class='b-expand']").click()
                sleep(2)
                
                # driver.find_element(by=By.CLASS_NAME, value = 'b-expand').click()

                
                about_driver = driver.find_element(by = By.XPATH, value = f"//p[@class='full-description mb-3 expanded clamp']/span")
                # temp_about.append(about_driver.text)
                print("Clicked on Read More")
            except:
                try:                        
                    sleep(2)
                    print("No read more button available")
                    # driver.find_element(by=By.CLASS_NAME, value = 'b-expand').click()
                    about_driver = driver.find_element(by = By.XPATH, value = f"//p[@class='full-description mb-3']/span")
                
                except:
                    sleep(2)
                    print("There is Read more button but not able to click, retrying")
                    counter = 1
                    while 1:
                        print(f"Try {counter}")
                        if counter <= 5:
                                
                            try:
                                driver.find_element(by=By.XPATH, value = "//button[@class='b-expand']").click()
                                sleep(3)
                            except:
                                pass
                            counter += 1
                        else:
                            break
                    print("Taking the available content")
                    try:
                        about_driver = driver.find_element(by = By.XPATH, value = f"//p[@class='full-description mb-3 clamp']/span")
                    except:
                        is_page_available = False

            if is_page_available:
                    

                # temp_about.append(about_driver.text)
                if about_driver.text == "":
                    temp_about = "Not Available"
                else:
                    temp_about = about_driver.text
                abouts.append(temp_about)
            else:
                abouts.append("Page not Availale")

            # temp_about = []
            # about_counter = 1
            # while 1:
            #     try:
            #         about_driver = driver.find_element(by = By.XPATH, value = f"//div[@class='profile-summary']/p[{about_counter}]")
            #         temp_about.append(about_driver.text)
            #     except:
            #         break
                
            #     about_counter += 1

            # if len(temp_about) == 0:
            #     temp_about = "Not Available"
            # abouts.append(temp_about)

            

            driver.close()
            sleep(5)


        # df = pd.DataFrame(columns=columns)
        # df["Rating"] = ratings
        # df["Strength"] = people_strength
        # df["Social Links"] = all_social_links
        # df["Founded Year"] = founded_year
        # df["Services"] = services
        # df["Focus Areas"] = focus_areas
        # df["Name"] = company_names[:COMPANIES_PER_PAGE]
        # df["Website"] = company_websites[:COMPANIES_PER_PAGE]
        # df["About"] = abouts

        
        
        # # main_df.append(df)
        # main_df = pd.concat([main_df, df], axis=0)

        # main_df.to_excel(f"{EXCEL_SAVING_PATH}/main_goodfirm_test.xlsx")
        # df.to_excel(f"{EXCEL_SAVING_PATH}/Page_0.xlsx")

    finally:
        df = pd.DataFrame(columns=columns)
        # df["Rating"] = ratings
        df["Strength"] = people_strength
        # df["Social Links"] = all_social_links
        df["Founded Year"] = founded_year
        # df["Services"] = services
        df["Focus Areas"] = focus_areas
        df["Name"] = company_names[:COMPANIES_PER_PAGE]
        df["Website"] = company_websites[:COMPANIES_PER_PAGE]
        df["About"] = abouts

        # main_df.append(df)
        main_df = pd.concat([main_df, df], axis=0)

        main_df.to_excel(f"{EXCEL_SAVING_PATH}/main_buitinla_test.xlsx")
        df.to_excel(f"{EXCEL_SAVING_PATH}/Page_{page}.xlsx")

    # try:
    #     # https://www.builtinla.com/companies/type/artificial-intelligence-companies?page=10
    #     url = current_page.split("page=")[0]
    #     next_page = "".join([url,"page="+str(page+2)])
    #     print(next_page)
    #     driver = webdriver.Chrome()
    #     driver.get(next_page)
    #     current_page = next_page
    #     sleep(5)
    #     driver.close()
    #     print("Switching to Page", page + 2)
    #     sleep(5)

    # except:
    #     driver.close()
    #     print("Reached End of the Pages")
    #     break
    

display.stop()

