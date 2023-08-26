from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyvirtualdisplay import Display
import undetected_chromedriver as uc


from time import sleep
import pandas as pd
import os
from tqdm import tqdm

COMPANIES_PER_PAGE = 1000

# Total pages to scrape
#Total Pages 9
TOTAL_PAGES = 1
CITY = "utah"
EXCEL_SAVING_PATH = f"excel_shared_to_scrape/third/futurology/{CITY}"

print("Saving excel file to",EXCEL_SAVING_PATH)

main_link = "https://futurology.life/57-most-innovative-utah-based-artificial-intelligence-companies/"



# Inorder to use the virtual display, the website pop will not open 
display = Display(visible=0, size=(800, 600))
display.start()


if not os.path.exists(EXCEL_SAVING_PATH):
    os.makedirs(EXCEL_SAVING_PATH)

# The data that is present in this website
columns = ["Name","Website","Social Links"]
# The data frame in which we will merge all the scraped pages data
main_df = pd.DataFrame(columns=columns)



for page in range(TOTAL_PAGES+1):
# 

    print("Running Page", page+1)

    # initializing driver
    # driver = webdriver.Chrome()
    driver = uc.Chrome()
    
    current_page = f"{main_link}?page={page}"
    print("Current Page URL",current_page)
    # accessing the website
    driver.get(current_page)
    # driver.maximize_window()
    sleep(17)

    try:
        # TODO : This xpath might be wrong need to check
        driver.find_element(by = By.XPATH, value = "//img[@src='https://i0.wp.com/www.futurology.us/wp-content/uploads/cp_modal/modal_get_interviewed_cp_id_44c6a/cross-1.png?fit=22%2C22&ssl=1']").click()
    except:
        print("No pop up")

    sleep(5)

    inside_company_urls_driver = driver.find_elements(by = By.XPATH, value="//div[@class='wp-block-cover__inner-container is-layout-flow wp-block-cover-is-layout-flow']/p[1]/a[1]")
    company_websites_driver = driver.find_elements(by = By.XPATH, value="//div[@class='wp-block-cover__inner-container is-layout-flow wp-block-cover-is-layout-flow']/p[1]/a[2]")

    inside_company_urls = [current.get_attribute("href") for current in inside_company_urls_driver]
    company_websites = [current.get_attribute("href") for current in company_websites_driver]

    print("Total companies in the current page is ", len(inside_company_urls))

    sleep(5)

    driver.close()
    print("Closed the current page")
    sleep(10)


    company_names = []
    # company_websites = []
    final_social_links = []

    COMPANIES_PER_PAGE = min(COMPANIES_PER_PAGE,len(inside_company_urls))

    for i,company_url in enumerate(inside_company_urls):

        print("Website number",i+1)
        print("Company Url", company_url)


        driver = uc.Chrome()
        # driver = webdriver.Chrome()
        print("Opening the company url")

        sleep(5)

        try:
            driver.get(company_url)
            sleep(30)

            try:
                name_driver = driver.find_element(by = By.XPATH, value = "//h1[@class='profile-name']")
                name = name_driver.text
            except:
                name = "Not Available"

            # Getting company url

            # try:
            #     company_url_driver = driver.find_elements(by = By.XPATH, value = "//a[@class='component--field-formatter link-accent ng-star-inserted']")

            #     url = company_url_driver[0].get_attribute("href")
            # except:
            #     url = "Not Available"

            # print("Found company url")

            # company_websites.append(url)

            # sleep(2)

            # Getting social links

            social_link_counter = 1
            temp_social_links = []

            for k in range(1,5):
                try:
                    social_link_driver = driver.find_element(by = By.XPATH, value=f"//fields-card[@class='ng-star-inserted'][{k}]/ul/li[{social_link_counter}]/field-formatter/link-formatter/a")

                    print("The social is at ",k)
                    break
                except:
                    pass


            while 1:
                try:
                    social_link_driver = driver.find_element(by = By.XPATH, value=f"//fields-card[@class='ng-star-inserted'][{k}]/ul/li[{social_link_counter}]/field-formatter/link-formatter/a")
                    social_link = social_link_driver.get_attribute("href")
                except:
                    break


                temp_social_links.append(social_link)

                social_link_counter += 1

            if temp_social_links == []:
                final_social_links.append("Not Available")
            else:
                final_social_links.append(temp_social_links)

            print("Found social link")
            sleep(2)

            company_names.append(name)
        except:
            print("The url is not opening",company_url)

        finally:
            print("Company names",company_names)
            driver.close()

            with open(os.path.join(EXCEL_SAVING_PATH,"company_names.txt"),"w+") as f:
                for name in company_names:
                    f.write(name)
                    f.write("\n")
                    
                # f.writelines(company_names)

            

                # f.writelines(company_websites)
            with open(os.path.join(EXCEL_SAVING_PATH,"final_social_links.txt"),"w+") as f:
                for link in final_social_links:
                    # for l in link:
                    f.write(str(link))
                    f.write("\n")

    with open(os.path.join(EXCEL_SAVING_PATH,"company_websites.txt"),"w+") as f:
        for website in company_websites:
            f.writelines(website)
            f.write("\n")

    df = pd.DataFrame(columns=columns)
    df["Name"] = company_names[:COMPANIES_PER_PAGE]
    df["Website"] = company_websites[:COMPANIES_PER_PAGE]
    # df["Rating"] = ratings
    df["Social Links"] = final_social_links
    # df["Services"] = services

    # main_df.append(df)
    main_df = pd.concat([main_df, df], axis=0)

    main_df.to_excel(f"{EXCEL_SAVING_PATH}/main_futurology_test.xlsx")
    df.to_excel(f"{EXCEL_SAVING_PATH}/Page_{page}.xlsx")  

display.stop()