# Run this code and them run the final_wellfound_preprocessing.py to preprocess the txt file obtained and create the excel file by running final_wellfound_preprocessing.py file.


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pyvirtualdisplay import Display
import undetected_chromedriver as uc

from time import sleep
import pandas as pd
import os

# we have total 15 pages
COMPANIES_PER_AGE = 1000
TOTAL_PAGES = 3
# max we have 15 pages
# CURRENT_PAGE = 1

CITY = "texas"
EXCEL_SAVING_PATH = f"excel_shared_to_scrape/third/wellfound/{CITY}_excels"
SAVING_PATH = f"excel_shared_to_scrape/third/wellfound/{CITY}_txts"
# Downloaded page url or the actual url
MAIN_PAGE = f"/home/wot-aditya/Aditya/Web Scraping/excel_shared_to_scrape/third/wellfound/well_found_page3.html"
next_page_link = None


# EXCEL_SAVING_PATH = "excel_shared_to_scrape/second/wellfound_los_angeles"
# SAVING_PATH = "excel_shared_to_scrape/second/wellfound/wellfound_los_angeles_txts"

SAVE_TXTS = True

print("Saving Files to ", EXCEL_SAVING_PATH)

# display = Display(visible=0, size=(800, 600))
# display.start()


if not os.path.exists(EXCEL_SAVING_PATH):
    os.makedirs(EXCEL_SAVING_PATH)


if not os.path.exists(SAVING_PATH):
    os.makedirs(SAVING_PATH)

columns = ["Name", "Website", "Rating", "Strength", "About",
           "Social Links", "Founded Year", "Services", "Focus Areas"]
main_df = pd.DataFrame(columns=columns)



for CURRENT_PAGE in range(3,TOTAL_PAGES+1):

    print("Running page number", CURRENT_PAGE)
    if next_page_link == None:
        print("Next page is none")

        current_page = f"{MAIN_PAGE}?page={CURRENT_PAGE}"

        # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

        # is_end_page = False

        driver = webdriver.Chrome()
        # driver = uc.Chrome()

        print("Current Page URL", current_page)
        # driver.get("file:///"+MAIN_PAGE)
        driver.get(current_page)
    sleep(20)

    # try:

    #     next_page_driver = driver.find_elements(by=By.XPATH, value = "//li[@class='styles_next__Dugw4']/a")[0]
    #     next_page_driver.click()

    #     next_page_link = "Present"
    #     print("Clicked on the next page")

    # except:
    #     print("Error in clicking next page")
    # sleep(10)

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

    company_names_driver = driver.find_elements(
        by=By.XPATH, value="//header[@class='text-dark-aaaa font-medium antialiased text-lg']")

    # company_names_driver = driver.find_elements(by = By.XPATH, value = "//header[@class='text-dark-aaaa font-medium antialiased text-lg']/div[1]")

    sleep(5)
    inside_websites_driver = driver.find_elements(
        by=By.XPATH, value="//a[@class='styles_component__UCLp3 styles_defaultLink__eZMqw !no-underline']")
    sleep(5)
    strength_driver = driver.find_elements(
        by=By.XPATH, value="//dl[@class='flex flex-wrap gap-10 text-sm']/div[2]/dd")
    sleep(5)
    company_websites_driver = driver.find_elements(
        by=By.XPATH, value="  //dl[@class='flex flex-wrap gap-10 text-sm']/div[1]/dd/a")
    sleep(5)

    read_more_driver = driver.find_elements(
        by=By.XPATH, value="  //button[@class='styles_component__7ZpRT styles_readMore____NV2']")

    # tags_driver = driver.find_elements(by = By.XPATH, value = "//ul[@class='styles_component__5DMnC !pl-1']/li[6]")
    # //ul[@class="styles_component__5DMnC !pl-1"]/li[6]

    # inside_company_driver = driver.find_elements(by = By.XPATH, value = "//a[@class='company_title directory_profile']")

    company_names = []
    for name in company_names_driver:
        try:
            name = name.text.split("\n")[0]
        except:
            name = name.text
        company_names.append(name)

    # company_names = [current.text for current in company_names_driver]
    inside_company_websites = [current.get_attribute(
        "href") for current in inside_websites_driver]
    people_strength = [current.text for current in strength_driver]
    company_websites = [current.get_attribute(
        "href") for current in company_websites_driver]

    print(f"Total companies in the current page {len(company_names)}")
    print(company_names)


    

    for button in read_more_driver:
        try:
            button.click()
            print("Pressed the read more button")
        except:
            print("failed to press read more button")
        sleep(2)

    about_driver = driver.find_elements(
        by=By.XPATH, value="//div[@class='mb-8 flex flex-col gap-6']")
    # about_driver = driver.find_elements(by = By.XPATH, value = "//div[@class='styles_component__481pO']")

    abouts = [current.get_attribute("innerHTML") for current in about_driver]

    sleep(2)
    focus_driver = driver.find_elements(
        by=By.XPATH, value="//dd[@class='flex flex-wrap gap-2']")
    # about_driver = driver.find_elements(by = By.XPATH, value = "//div[@class='styles_component__481pO']")

    focus_areas = [current.get_attribute(
        "innerHTML") for current in focus_driver]


#   //div[@class='mb-8 flex flex-col gap-6']/dl[2] for the focus area

    # for i in range(len(inside_company_websites)-1):
    #     try:

    #         current_url = inside_company_websites[i].split("#")[0]
    #         next_url = inside_company_websites[i+1].split("#")[0]

    #         if current_url == next_url:
    #             inside_company_websites.remove(current_url)
    #     except:
    #         pass

    # print(company_names)
    # print(company_websites)

    # print(company_names)
    # print(company_websites)

    # total_companies = len(company_names)
    # print("total Companies", total_companies)

    # ratings = []
    # # people_strength = []

    # all_social_links = []
    # founded_year = []
    # time_zones = []
    # services = []
    # focus_areas = []
    # abouts = []
    # company_websites = []

    if SAVE_TXTS:

        with open(f"{SAVING_PATH}/inside_urls_page_{CURRENT_PAGE}.txt", "w+") as f:
            for line in inside_company_websites:
                f.write(f"{line}\n")

        with open(f"{SAVING_PATH}/company_names_page_{CURRENT_PAGE}.txt", "w+") as f:
            for line in company_names:
                f.write(f"{line}\n")

        with open(f"{SAVING_PATH}/people_strength_page_{CURRENT_PAGE}.txt", "w+") as f:
            for line in people_strength:
                f.write(f"{line}\n")

        with open(f"{SAVING_PATH}/company_websites_page_{CURRENT_PAGE}.txt", "w+") as f:
            for line in company_websites:
                f.write(f"{line}\n")

        with open(f"{SAVING_PATH}/abouts_page_{CURRENT_PAGE}.txt", "w+") as f:
            for line in abouts:
                f.write(f"{line}\n")

        with open(f"{SAVING_PATH}/focus_areas_page_{CURRENT_PAGE}.txt", "w+") as f:
            for line in focus_areas:
                f.write(f"{line}\n")

    sleep(5)
    driver.close()
    sleep(5)

    

    continue

    # exit()
    inside_company_websites = ["https://wellfound.com/company/dataiku"]

    try:

        # COMPANIES_PER_PAGE = min(COMPANIES_PER_PAGE,total_companies)

        total_possible_social_media = 3

        i = 0

        for company_url in inside_company_websites:
            # for company_url in inside_company_websites[:COMPANIES_PER_PAGE]:

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
            sleep(5)

            # Getting Company Official Website

            try:
                website_driver = driver.find_element(
                    by=By.XPATH, value="//li[@class='styles_websiteLink___Rnfc']")
                company_websites.append(website_driver.get_attribute("href"))
            except:
                company_websites.append("Not Available")

            sleep(3)

            # Getting ratings
            # //ul[@class="styles_component__5DMnC !pl-1"]/li[@class='styles_component__ejzCg styles_orange__lheFk']

            # try:
            #     # rating_driver = driver.find_element(by = By.XPATH, value = "/html/body/main/div[2]/section[1]/section[2]/div[1]/dl/dd/div/span")
            #     rating_driver = driver.find_element(by = By.XPATH, value = "//span[@class='review-rating']")
            #     rating = float(rating_driver.text)
            # except:
            #     rating = "Not Available"

            # # ratings[i] = rating
            # ratings.append(rating)

            current_social_link = ""
            social_counter = 1
            social_links = []

            while 1:
                try:
                    # social_media_links_driver = driver.find_element(by = By.XPATH, value=f"//div[@class='profile-social profile-social__wrap ']/a[{index}]")

                    social_media_links_driver = driver.find_element(
                        by=By.XPATH, value=f"//div[@class='styles_component__g_WAp styles_links__VvYv7']/ul/li[2]/ul/li[{social_counter}]/a")

                    current_social_link = social_media_links_driver.get_attribute(
                        "href")
                    social_links.append(current_social_link)
                    sleep(1)
                except:
                    # current_social_link = "Not available"
                    break
                social_counter += 1

            if len(social_links) == 0:
                social_links = "Not Available"
            # all_social_links[i] = social_links
            # print(all_social_links[i])
            # all_social_links.append(social_links)

            # # Getting Focus content
            # temp_focus = []
            # focus_counter = 1
            # while 1:
            #     try:
            #         focus_driver = driver.find_element(by=By.XPATH, value=f"//div[@class='industry-focus-container']/div[1]/div[{focus_counter}]")
            #         focus_name = focus_driver.get_attribute("data-content").replace("\n"," ").replace("<i>","").replace("</i>", "")
            #         focus_per = focus_driver.text
            #         temp_focus.append(" ".join([focus_name, focus_per]))

            #     except:
            #         break
            #     focus_counter += 1
            # if len(temp_focus) == 0:
            #     temp_focus = "Not Available"
            # # focus_areas[i] = temp_focus
            # focus_areas.append(temp_focus)

            # # Getting About

            # # Clicking on the read more button to load all the about content
            # try:
            #     driver.implicitly_wait(5)
            #     # print("We need to click the Read more")
            #     driver.find_element(by=By.XPATH, value = "//button[@class='read-more-summary']").click()
            #     # print("Clicked on Read More")
            # except:
            #     pass

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

            sleep(3)
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
        # df["Strength"] = people_strength
        df["Social Links"] = all_social_links
        # df["Founded Year"] = founded_year
        # df["Services"] = services
        # df["Focus Areas"] = focus_areas
        # df["Name"] = company_names[:COMPANIES_PER_PAGE]
        df["Website"] = company_websites[:COMPANIES_PER_PAGE]
        # df["About"] = abouts

        # main_df.append(df)
        main_df = pd.concat([main_df, df], axis=0)

        main_df.to_excel(f"{EXCEL_SAVING_PATH}/main_wellfound_test.xlsx")
        df.to_excel(f"{EXCEL_SAVING_PATH}/Page_{page}.xlsx")

    if is_end_page:
        print("Reached End of the Pages")
        break


# display.stop()
