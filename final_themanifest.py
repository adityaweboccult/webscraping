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


COMPANIES_PER_PAGE = 1000
TOTAL_PAGES = 3
CITY = "texas"
EXCEL_SAVING_PATH = f"excel_shared_to_scrape/third/themanifest/{CITY}_excels"
MAIN_EXCEL_PATH = f"{EXCEL_SAVING_PATH}/main_themanisfest.xlsx"
main_link = "https://themanifest.com/artificial-intelligence/companies/austin"



print("Saving the excel files to ", EXCEL_SAVING_PATH)

# Inorder to use the virtual display, the website pop will not open 
display = Display(visible=0, size=(800, 600))
display.start()


if not os.path.exists(EXCEL_SAVING_PATH):
    os.makedirs(EXCEL_SAVING_PATH)


# The data that is present in this website
columns = ["Name","Website","About","Rating","Strength","Social Links","Founded Year","Time Zone","Services","Focus Areas"]
# The data frame in which we will merge all the scraped pages data
main_df = pd.DataFrame(columns=columns)


# The starting page, here we have to give the website link as below given format
#give the website name with ?page=<page_no>




for page in range(TOTAL_PAGES):

    print("Running Page", page)

    # initializing driver
    driver = webdriver.Chrome()

    current_page = f"{main_link}?page={page}" 
        
    print("Current Page URL",current_page)
    # accessing the website
    driver.get(current_page)
    # driver.maximize_window()

    complete_data = dict()

    company_name_website_driver = driver.find_elements(by = By.XPATH, value="//a[@class='track-website-visit']")
    about_driver = driver.find_elements(by = By.XPATH, value = "//div[@class='provider-summary']")
    strength_driver = driver.find_elements(by = By.XPATH, value = "//ul[@class='provider-card__details provider-details']/li[2]/span")

    


    company_names = [current.text for current in company_name_website_driver]
    company_websites = [current.get_attribute("href") for current in company_name_website_driver]
    company_abouts = [current.text for current in about_driver]
    company_strengths = [current.text for current in strength_driver]

    total_companies = len(company_names)
    print("Total Companies",len(company_names))

    for i in range(len(company_name_website_driver)):
        name = company_names[i].lower()
        website = company_websites[i]
        about = company_abouts[i]
        strength = company_strengths[i]
        complete_data[name] = [name,website,about,strength]



    

   
    inside_urls_driver = driver.find_elements(by = By.XPATH , value = "//a[@class='provider-rating__overall-reviews-link track-review-click']")

    inside_urls = [current.get_attribute("href") for current in inside_urls_driver]

    print("Companies with detail",len(inside_urls))

    COMPANIES_PER_PAGE = min(COMPANIES_PER_PAGE,total_companies)


    driver.close()
    sleep(5)

    company_with_detail = []
    ratings = []
    people_strength = []
    all_social_links = []
    founded_year = []
    time_zones = []
    services = []
    focus_areas = []
    abouts = []

    for company_url in inside_urls[:COMPANIES_PER_PAGE]:


        try:
            company_url = company_url.split("#")[0]
        except:
            pass

        print("Current company URL:",company_url)
        driver = webdriver.Chrome()
        driver.get(company_url)


        # Getiing company name

        try:
            name = driver.find_element(by = By.XPATH, value = "//h1[@class='profile-header__title']/a").text
        except:
            name = "No Company Name"

        company_with_detail.append(name.lower())

        try:
            # rating_driver = driver.find_element(by = By.XPATH, value = "/html/body/main/div[2]/section[1]/section[2]/div[1]/dl/dd/div/span")
            rating_driver = driver.find_element(by = By.XPATH, value = "//span[@class='sg-rating__number']")
            
            rating = float(rating_driver.text)
        except:
            rating = "Not Available"

        # ratings[i] = rating
        ratings.append(rating)

        # Getting strengths and founded_year
        strength_and_founded_year_driver = driver.find_elements(by = By.XPATH, value = "//li[@class='profile-summary__detail sg-text sg-tooltip']/span[2]")

        try:

            strength = strength_and_founded_year_driver[-2].text
            
            # strength_driver = driver.find_element(by=By.XPATH, value = "//li[@class='profile-summary__detail sg-text sg-tooltip'][3]")
            # strength = strength_driver.text
        except:
            strength = "Not Available"

        # people_strength[i] = strength

        people_strength.append(strength.replace(" employees",""))
        # print(people_strength)

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


        # Finding    Provided
        temp_services = []
        service_counter = 1
        while 1:
            try:
                service_provided_driver = driver.find_element(by = By.XPATH, value = f"//ul[@id='legend_list']/li[{service_counter}]") 
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
        sleep(2)


    final_ratings = []
    final_people_strength = []
    final_founded_year = []
    final_all_social_links = []
    final_time_zones = []
    final_services = []
    final_focus_areas = []
    final_abouts = []

    detail_company_counter = 0
    print("Company With detail",company_with_detail)
    for i in range(total_companies):

        # complete_data[name] = [name,website,about,strength]
        temp_name = company_names[i].lower()
        # print(temp_name)

        if temp_name in company_with_detail:

            # print(f"{temp_name} is present in detail company")
            current_rating = ratings[detail_company_counter]
            current_strength = people_strength[detail_company_counter]
            current_founded_year = founded_year[detail_company_counter]
            current_social_link = all_social_links[detail_company_counter]
            current_time_zone = time_zones[detail_company_counter]
            current_service = services[detail_company_counter]
            current_focus_area = focus_areas[detail_company_counter]
            
            detail_company_counter += 1

        else:
            current_rating = "Not available"
            current_strength = complete_data[temp_name][3].replace(" employees","")
            current_founded_year = "Not available"
            current_social_link = "Not available"
            current_time_zone = "Not available"
            current_service = "Not available"
            current_focus_area = "Not available"

        final_ratings.append(current_rating)
        final_people_strength.append(current_strength)
        final_all_social_links.append(current_social_link)
        final_founded_year.append(current_founded_year)
        final_time_zones.append(current_time_zone)
        final_services.append(current_service)
        final_focus_areas.append(current_focus_area)
        final_abouts.append(complete_data[temp_name][2])

    df = pd.DataFrame(columns=columns)
    df["Rating"] = final_ratings
    df["Strength"] = final_people_strength
    df["Social Links"] = final_all_social_links
    df["Founded Year"] = final_founded_year
    df["Time Zone"] = final_time_zones
    df["Services"] = final_services
    df["Focus Areas"] = final_focus_areas
    df["About"] = final_abouts
    df["Name"] = company_names[:COMPANIES_PER_PAGE]
    df["Website"] = company_websites[:COMPANIES_PER_PAGE]

    
    
    # main_df.append(df)
    main_df = pd.concat([main_df, df], axis=0)

    main_df.to_excel(MAIN_EXCEL_PATH)
    df.to_excel(f"{EXCEL_SAVING_PATH}/themanifest_page_{page}.xlsx")


        
display.stop()

