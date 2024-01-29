from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pyvirtualdisplay import Display

from time import sleep
import pandas as pd
import os


COMPANIES_PER_PAGE = 1000
TOTAL_PAGES = 10
CITY = "uk"
folder_name = "5_fifth_09th_November"
EXCEL_SAVING_PATH = f"excel_shared_to_scrape/{folder_name}/goodfirm/{CITY}_excels"
MAIN_EXCEL_PATH = f"{EXCEL_SAVING_PATH}/main_good_firm_v1.xlsx"

print("Saving the data into", EXCEL_SAVING_PATH)

display = Display(visible=0, size=(800, 600))
display.start()

current_page = "https://www.goodfirms.co/artificial-intelligence/uk"
# current_page = "https://www.goodfirms.co/artificial-intelligence/texas?page=2"

if not os.path.exists(EXCEL_SAVING_PATH):
    os.makedirs(EXCEL_SAVING_PATH)

columns = ["Name","Website","Rating","Strength","About","Social Links","Founded Year","Services","Focus Areas"]
main_df = pd.DataFrame(columns=columns)


for page in range(TOTAL_PAGES):
    print("Running Page", page+1)

    # driver = webdriver.Chrome()

    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


    is_end_page = False

    driver = webdriver.Chrome()
        

    print("Current Page URL",current_page)
    driver.get(current_page)

    try:        
        next_page = driver.find_element(by = By.XPATH, value = "//li[@class='next-page']/a").get_attribute("href")
        # next_page = current_page.replace("?")
        print("Next page", next_page)
        current_page = next_page

    except:
        is_end_page = True

    # pagination_driver = driver.find_elements(by = By.XPATH  , value = "//a[@class='page-link']")

    # //ul[@class='pagination justify-content-center']/li[1]

    # all_pages = [current_page.get_attribute("href") for current_page in pagination_driver]
    # page_number = [current_page.text for current_page in pagination_driver]

 


    company_names_driver = driver.find_elements(by = By.XPATH, value = "//div[@class='firm-header-wrapper']/h3/a")
    inside_websites_driver = driver.find_elements(by = By.XPATH, value = "//a[@class='visit-profile']")
    company_websites_driver = driver.find_elements(by = By.XPATH, value = "//a[@class='visit-website web-url list-blue-link']")

    # inside_company_driver = driver.find_elements(by = By.XPATH, value = "//a[@class='company_title directory_profile']")


    company_names = [current.text for current in company_names_driver]
    inside_company_websites = [current.get_attribute("href") for current in inside_websites_driver]
    company_websites = [current.get_attribute("href") for current in company_websites_driver]



    for i in range(len(inside_company_websites)-1):     # Comparing the adjacent url to remove the redundant urls
        try:
                
            current_url = inside_company_websites[i].split("#")[0]
            next_url = inside_company_websites[i+1].split("#")[0]

            if current_url == next_url:
                inside_company_websites.remove(current_url)
        except:
            pass

    # print(company_names)
    # print(company_websites)

    # print(company_names)
    # print(company_websites)




    total_companies = len(company_names)
    print("total Companies", total_companies)

    ratings = []
    people_strength = []

    all_social_links = []
    founded_year = []
    time_zones = []
    services = []
    focus_areas = []
    abouts = []

    driver.close()
    sleep(3)

    try :

        COMPANIES_PER_PAGE = min(COMPANIES_PER_PAGE,total_companies)
            
        total_possible_social_media = 3

        i = 0

        for company_url in inside_company_websites[:COMPANIES_PER_PAGE]:

            

            # op = webdriver.ChromeOptions()
            # op.add_argument('headless')
            # driver = webdriver.Chrome(options=op)
            driver = webdriver.Chrome()

            try:
                company_url = company_url.split("#")[0]
            except:
                company_url = company_url

            print(company_url)
            driver.get(company_url)

            # Getting ratings

            try:
                # rating_driver = driver.find_element(by = By.XPATH, value = "/html/body/main/div[2]/section[1]/section[2]/div[1]/dl/dd/div/span")
                rating_driver = driver.find_element(by = By.XPATH, value = "//span[@class='review-rating']")
                rating = float(rating_driver.text)
            except:
                rating = "Not Available"

            # ratings[i] = rating
            ratings.append(rating)



            # Getting Strengths
            try:

                strength_driver = driver.find_element(by=By.XPATH, value = "//div[@class='profile-employees custom_tooltip']/span")
                strength = strength_driver.text
                
            except:
                strength = "Not Available"

            # people_strength[i] = strength
            people_strength.append(strength)


            # Finding the Founded year
            try:
                founded_year_driver = driver.find_element(by= By.XPATH, value = "//div[@class='profile-founded custom_tooltip']/span")
                year = founded_year_driver.text
                
                year = int(year)

            except:
                year = "Not Available"

            # year = int(founded_year_driver.text.split()[1])    
            # founded_year[i] = year
            founded_year.append(year)

            current_social_link = ""
            social_counter = 1
            social_links = []

            while 1:
                try:
                    # social_media_links_driver = driver.find_element(by = By.XPATH, value=f"//div[@class='profile-social profile-social__wrap ']/a[{index}]")

                    social_media_links_driver = driver.find_element(by = By.XPATH, value=f"//div[@class='social-profile']/a[{social_counter}]")
                    
                    current_social_link = social_media_links_driver.get_attribute("href")
                    social_links.append(current_social_link)
                except:
                    # current_social_link = "Not available"
                    break
                social_counter += 1
                
                
            if len(social_links) == 0:
                social_links = "Not Available"
            # all_social_links[i] = social_links
            # print(all_social_links[i])
            all_social_links.append(social_links)


            # Finding Service Provided
            temp_services = []
            service_counter = 1
            while 1:
                try:

                    service_provided_driver = driver.find_element(by = By.XPATH, value = f"//div[@class='focus-container service-focus-container']/div[1]/div[{service_counter}]") 
                    service_name = service_provided_driver.get_attribute("data-content").replace("\n"," ").replace("<i>","").replace("</i>", "")
                    service_per = service_provided_driver.text
                    temp_services.append(" ".join([service_name, service_per]))
                    # temp_services.append(service_provided_driver.get_attribute("data-content").replace("\n"," ").replace("<i>","").replace("</i>", ""))
                    # temp_services.append(service_provided_driver.text.replace("\n"," "))
                    
                except:
                    break

                service_counter += 1

            if len(temp_services) == 0:
                temp_services = "Not Available"
            # services[i] = temp_services
            services.append(temp_services)


            # Getting Focus content
            temp_focus = []
            focus_counter = 1   
            while 1:
                try:
                    focus_driver = driver.find_element(by=By.XPATH, value=f"//div[@class='industry-focus-container']/div[1]/div[{focus_counter}]")
                    focus_name = focus_driver.get_attribute("data-content").replace("\n"," ").replace("<i>","").replace("</i>", "")
                    focus_per = focus_driver.text
                    temp_focus.append(" ".join([focus_name, focus_per]))
                
                except:
                    break
                focus_counter += 1
            if len(temp_focus) == 0:
                temp_focus = "Not Available"
            # focus_areas[i] = temp_focus
            focus_areas.append(temp_focus)


            # Getting About

            # Clicking on the read more button to load all the about content
            try:             
                driver.implicitly_wait(5)
                # print("We need to click the Read more")  
                driver.find_element(by=By.XPATH, value = "//button[@class='read-more-summary']").click() 
                # print("Clicked on Read More")
            except:
                pass


            temp_about = []
            about_counter = 1
            while 1:
                try:
                    about_driver = driver.find_element(by = By.XPATH, value = f"//div[@class='profile-summary']/p[{about_counter}]")
                    temp_about.append(about_driver.text)
                except:
                    break
                
                about_counter += 1

            if len(temp_about) == 0:
                temp_about = "Not Available"
            abouts.append(temp_about)

            

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
        df["Rating"] = ratings
        df["Strength"] = people_strength
        df["Social Links"] = all_social_links
        df["Founded Year"] = founded_year
        df["Services"] = services
        df["Focus Areas"] = focus_areas
        df["Name"] = company_names[:COMPANIES_PER_PAGE]
        df["Website"] = company_websites[:COMPANIES_PER_PAGE]
        df["About"] = abouts

        # main_df.append(df)
        main_df = pd.concat([main_df, df], axis=0)

        main_df.to_excel(MAIN_EXCEL_PATH)
        df.to_excel(f"{EXCEL_SAVING_PATH}/goodfirm_page_{page+1}_v2.xlsx")

    if is_end_page:
        print("Reached End of the Pages")
        break
    

display.stop()

