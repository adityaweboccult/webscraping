# This will scrape the featured companies run final_clutch_scrape.py to get non featured companies.

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




TOTAL_PAGES = 1
COMPANIES_PER_PAGE = 1000
CITY = "uk"
folder_name = "5_fifth_09th_November"
EXCEL_SAVING_PATH = f"excel_shared_to_scrape/{folder_name}/clutch/{CITY}_excels"
MAIN_EXCEL_PATH = f"{EXCEL_SAVING_PATH}/main_clutch_featured.xlsx"

print("Saving the data into", EXCEL_SAVING_PATH)
if not os.path.exists(EXCEL_SAVING_PATH):
    os.mkdir(EXCEL_SAVING_PATH)

current_page = "https://clutch.co/uk/developers/artificial-intelligence?1"

columns = ["Name","Website","Rating","Strength","Social Links","Founded Year","Time Zone","Services","Focus Areas"]
main_df = pd.DataFrame(columns=columns)

display = Display(visible=0, size=(800, 600))
display.start()

# options = Options()
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# options = webdriver.ChromeOptions()
# options.add_argument('--ignore-ssl-errors=yes')
# options.add_argument('--ignore-certificate-errors')
# driver = webdriver.Chrome(options=options)


# from selenium.webdriver import DesiredCapabilities

# options = webdriver.ChromeOptions()
# options.add_argument('--allow-insecure-localhost') # differ on driver version. can ignore. 
# caps = options.to_capabilities()
# caps["acceptInsecureCerts"] = True
# driver = webdriver.Chrome(desired_capabilities=caps)
# page_url_dict = dict()




# for current_page in all_pages[:total_pages]:
for page in range(TOTAL_PAGES):

    print("Running Page", page+1)

    # print("Running page", current_page_number+1)

    # op = webdriver.ChromeOptions()
    # op.add_argument('--headless')
    # driver = webdriver.Chrome(options=op)
    driver = webdriver.Chrome()
    

    print("Current Page URL",current_page)
    driver.get(current_page)

    pagination_driver = driver.find_elements(by = By.XPATH  , value = "//a[@class='page-link']")
    
    # //ul[@class='pagination justify-content-center']/li[1]

    all_pages = [current_page.get_attribute("href") for current_page in pagination_driver]
    page_number = [current_page.text for current_page in pagination_driver]

    

    company_names_driver = driver.find_elements(by = By.XPATH, value = "//a[@class='ppc-website-link']")
    company_websites_driver = driver.find_elements(by = By.XPATH, value = "//a[@class='ppc-website-link']")
    inside_company_driver = driver.find_elements(by = By.XPATH, value = "//div[@class='company prompt-target col-md-12 prompt-target-new-bookmark']/div/a[1]")

    # company_names_driver = driver.find_elements(by = By.XPATH, value = "//a[@class='company_title directory_profile']")
    # company_websites_driver = driver.find_elements(by = By.XPATH, value = "//a[@class='website-link__item']")
    # inside_company_driver = driver.find_elements(by = By.XPATH, value = "//a[@class='company_title directory_profile']")


    company_names = []
    company_websites = []


    temp_company_inside_urls = []

    total_companies = len(company_names_driver)

    ratings = []
    people_strength = []

    all_social_links = []
    founded_year = []
    time_zones = []
    services = []
    focus_areas = []

    # ratings = [None]*total_companies
    # people_strength = [None]*total_companies

    # all_social_links = [None]*total_companies
    # founded_year = [None]*total_companies
    # time_zones = [None]*total_companies
    # services = [None]*total_companies
    # focus_areas = [None]*total_companies

    # index = 1
    # i = 1
    for name,website,inside_company in zip(company_names_driver,company_websites_driver,inside_company_driver):
        company_inside_url = inside_company.get_attribute("href")
        temp_company_inside_urls.append(company_inside_url)


        company_names.append(name.text)
        company_websites.append(website.get_attribute("href"))


        # index+= 1

            
    print(f"Total Companies", len(company_names))

    driver.close()


    # sleep(5)

    # exit()

    try :

        COMPANIES_PER_PAGE = min(COMPANIES_PER_PAGE,total_companies)
            
        total_possible_social_media = 3


        i = 0

        for company_url in temp_company_inside_urls[:COMPANIES_PER_PAGE]:


            # op = webdriver.ChromeOptions()
            # op.add_argument('headless')
            # driver = webdriver.Chrome(options=op)

            try:
                company_url = company_url.split("#")[0]
            except:
                pass
            driver = webdriver.Chrome()

            print(company_url)
            driver.get(company_url)

            # about_driver = driver.find_elements(by = By.XPATH, value = "//div[@class='profile-summary__text cropped-summary-text shown']")
            # about_driver = driver.find_element(by = By.XPATH, value = "//div[@id='profile-summary-text']")
            # content = driver.execute_script("return document.getElementById('p').innerHTML")

            # content = about_driver.get_attribute('innerHTML')
            # print(content.strip())
            # print(about_driver.text)


            # Getting ratings

            try:
                # rating_driver = driver.find_element(by = By.XPATH, value = "/html/body/main/div[2]/section[1]/section[2]/div[1]/dl/dd/div/span")
                rating_driver = driver.find_element(by = By.XPATH, value = "//span[@class='sg-rating__number']")
                
                rating = float(rating_driver.text)
            except:
                rating = "Not Available"

            # ratings[i] = rating
            ratings.append(rating)


            strength_and_founded_year_driver = driver.find_elements(by = By.XPATH, value = "//li[@class='profile-summary__detail sg-text sg-tooltip']/span[2]")
            # Getting strengths and founded_year

            try:

                strength = strength_and_founded_year_driver[-2].text
                
                # strength_driver = driver.find_element(by=By.XPATH, value = "//li[@class='profile-summary__detail sg-text sg-tooltip'][3]")
                # strength = strength_driver.text
            except:
                strength = "Not Available"

            # people_strength[i] = strength
            people_strength.append(strength)


            # Finding the Founded year
            try:
                year = strength_and_founded_year_driver[-1].text.split()[1]
                
                # founded_year_driver = driver.find_element(by = By.XPATH, value = "//li[@class='profile-summary__detail sg-text sg-tooltip'][4]")
                year = int(year)

            except:
                year = "Not Available"

            # year = int(founded_year_driver.text.split()[1])    
            # founded_year[i] = year
            founded_year.append(year)


            # Getting the social links
            # print("finding Social links")
            current_social_link = ""
            social_counter = 1
            social_links = []

            while 1:
                try:
                    # social_media_links_driver = driver.find_element(by = By.XPATH, value=f"//div[@class='profile-social profile-social__wrap ']/a[{index}]")

                    social_media_links_driver = driver.find_element(by = By.XPATH, value=f"//div[@class='profile-summary__social']/div/a[{social_counter}]")
                    
                    current_social_link = social_media_links_driver.get_attribute("href")
                    social_links.append(current_social_link)

                except:
                    break
                    # current_social_link = "Not available"
                    # pass
                social_counter += 1
                
            if len(social_links) == 0:
                social_links = "Not Available"
            # all_social_links[i] = social_links
            # print(all_social_links[i])
            all_social_links.append(social_links)
            
            
            


            #Finding Time zone
            time_zone_tags = ["dt","dd"]
            time_zone_count = 1
            temp_time_zones = []
            while 1:
                try:
                    time_zone_driver_abb = driver.find_element(by = By.XPATH, value = f"//div[@class='profile-modal--list']/dl[{time_zone_count}]/dt")

                    time_zone_driver = driver.find_element(by = By.XPATH, value = f"//div[@class='profile-modal--list']/dl[{time_zone_count}]/dd")

                    # time_zone_driver_abb = driver.find_element(by = By.XPATH, value = f"/html/body/main/div[2]/section[1]/div/div/div/div/dl[{time_zone_count}]/dt")
                    # time_zone_driver = driver.find_element(by = By.XPATH, value = f"/html/body/main/div[2]/section[1]/div/div/div/div/dl[{time_zone_count}]/dd")

                    time_zone = " ".join([time_zone_driver_abb.get_attribute("innerHTML"),
                                        time_zone_driver.get_attribute("innerHTML")])
                except:
                    # print("Breaking Time zone")
                    break
                time_zone_count += 1

                temp_time_zones.append(time_zone)
            if len(temp_time_zones) == 0:
                temp_time_zones = "Not Available"
            # time_zones[i] = (temp_time_zones)
            time_zones.append(temp_time_zones)


            # Finding Service Provided
            temp_services = []
            service_counter = 1
            while 1:
                try:


                    service_provided_driver = driver.find_element(by = By.XPATH, value = f"//ul[@id='legend_list']/li[{service_counter}]") 
                    # if rating == "Not Available":
                    #     service_provided_driver = driver.find_element(by = By.XPATH, value=f"/html/body/main/div[2]/section[1]/section[2]/div[4]/ul/li[{service_counter}]")
                    # else:
                    #     service_provided_driver = driver.find_element(by = By.XPATH, value=f"/html/body/main/div[2]/section[1]/section[3]/div[4]/ul/li[{service_counter}]")
                    temp_services.append(service_provided_driver.text.replace("\n"," "))
                    
                except:
                    break

                service_counter += 1
            if len(temp_services) == 0:
                temp_services = "Not Available"
            # services[i] = temp_services
            services.append(temp_services)
            # print(services)
            

            #Finding focus 
            temp_focus = []
            focus_counter = 1   
            while 1:
                try:


                    focus_driver = driver.find_element(by=By.XPATH, value=f"//div[@id='focus-chart_dropdown-list']/div[{focus_counter}]/label/span")


                    # if rating == "Not Available":
                    #     focus_driver = driver.find_element(by=By.XPATH, value=f"/html/body/main/div[2]/section[1]/section[2]/div[1]/div/div[{focus_counter}]/label/span")
                    # else:
                    #     focus_driver = driver.find_element(by = By.XPATH, value=f"/html/body/main/div[2]/section[1]/section[3]/div[4]/div[3]/div/div[{focus_counter}]/label/span")
                    focus_area = focus_driver.get_attribute("innerHTML").replace("&amp;","&").replace("\n"," ")
                    temp_focus.append(focus_area)
                
                except:
                    break
                focus_counter += 1
            if len(temp_focus) == 0:
                temp_focus = "Not Available"
            # focus_areas[i] = temp_focus
            focus_areas.append(temp_focus)

            driver.close()
            sleep(1)
            i+=1

            continue

            # Finding About
            # driver.close()
            # sleep(5)
            # driver = webdriver.Chrome()

            driver.implicitly_wait(10)
            # driver.find_element(by=By.XPATH, value = "//button[@id='read_more']").click()                  # Clicking the read more button
            # driver.find_element(by=By.ID, value = "read_more").click()                  # Clicking the read more button

            sleep(2)
            profile_summary_driver = driver.find_element(by = By.ID, value = "profile-summary-text")

            print(profile_summary_driver.get_attribute("innerHTML"))






            
        # sleep(5)

        df = pd.DataFrame(columns=columns)
        df["Rating"] = ratings
        df["Strength"] = people_strength
        df["Social Links"] = all_social_links
        df["Founded Year"] = founded_year
        df["Time Zone"] = time_zones
        df["Services"] = services
        df["Focus Areas"] = focus_areas
        df["Name"] = company_names[:COMPANIES_PER_PAGE]
        df["Website"] = company_websites[:COMPANIES_PER_PAGE]

        
        
        # main_df.append(df)
        main_df = pd.concat([main_df, df], axis=0)

        main_df.to_excel(MAIN_EXCEL_PATH)
        df.to_excel(f"{EXCEL_SAVING_PATH}/featured_clutch_page_{page+1}.xlsx")


    except:
        df = pd.DataFrame(columns=columns)
        df["Rating"] = ratings
        df["Strength"] = people_strength
        df["Social Links"] = all_social_links
        df["Founded Year"] = founded_year
        df["Time Zone"] = time_zones
        df["Services"] = services
        df["Focus Areas"] = focus_areas
        df["Name"] = company_names[:COMPANIES_PER_PAGE]
        df["Website"] = company_websites[:COMPANIES_PER_PAGE]

        # main_df.append(df)
        print(df.head())

        main_df = pd.concat([main_df, df], axis=0)



        # main_df.to_excel(f"{EXCEL_SAVING_PATH}/main_clutch.xlsx")
        # df.to_excel(f"{EXCEL_SAVING_PATH}/Page_{page}.xlsx")

        main_df.to_excel(MAIN_EXCEL_PATH)
        df.to_excel(f"{EXCEL_SAVING_PATH}/featured_clutch_page_{page+1}.xlsx")

    try:
        next_index = page_number.index("next")
        current_page = all_pages[next_index]
    except:
        print("No Next Page")
        display.stop()
        exit()

print("Saving the main excel at location",MAIN_EXCEL_PATH)
display.stop()