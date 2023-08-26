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
import random

# This variable should be greater than the total companies present in a single page, e.g. if we know maximum that maximu could be present is 20 then this variable should be greater than 20
COMPANIES_PER_PAGE = 1000
# 
# Total pages to scrape
#Total Pages 9
TOTAL_PAGES = 1
CITY = "arizona"
EXCEL_SAVING_PATH = f"excel_shared_to_scrape/third/beststartup/{CITY}_excels"

print("Saving excel file to",EXCEL_SAVING_PATH)

#give the website name with ?page=<page_no>
main_link = "https://beststartup.us/71-best-arizona-artificial-intelligence-companies-and-startups/"

# Inorder to use the virtual display, the website pop will not open 
display = Display(visible=0, size=(800, 600))
display.start()


if not os.path.exists(EXCEL_SAVING_PATH):
    os.makedirs(EXCEL_SAVING_PATH)


# The data that is present in this website
columns = ["Name","Website","About","Social Links","Founded Year","Strength","Focus Areas"]
# The data frame in which we will merge all the scraped pages data
main_df = pd.DataFrame(columns=columns)


agents = ["Edwin Potter","Arianna Edwards","Adnan Howard","Alejandro Brooks","Betty Simpson","Jenson Thomson","Nate Bates","Mark Hewitt","Samuel Contreras","Andy Sparks","Shane Franco","Jerry Gallegos","Kyle Blevins","Garfield Curtis","Josef Bowen","Enzo Mooney","Beau Leonard","Faisal Hood","Carly Hardin","Mia Dale","Mildred Frye","Kathryn Graham","Bryony Lozano","Mohamad Knight","Leonard Craig","Izabella Kerr","Maggie Branch","Jasper Santos","Abdullah Welsh","Alasdair Johns","Marvin Mosley","Kaitlin Dejesus","Yusra Harrison","Emilie Finley","Mohammed Dixon","Abi Mcbride","Silas Sharp","Amin Blair","Ayrton Richmond","Fleur Mann","Sam Simmons","Angelo Mcclure","Virginia Hampton","Marcel May","Andrew Anthony","Kelsey Valencia","Carlos Orr","Alfred Acosta","Kyra Mack","Scarlett Decker","Wyatt Bernard","Everett Massey","Yunus Fletcher","Asad Callahan","Aamina George","Sian Perkins","Brianna Rivas","Jenna Carney","Laila Sampson","Elodie Mccullough","Ted Riddle","Cleo Peters","Rebekah Burgess","Jorge Dyer","Nabil Horton","Josie Young","Leo Vang","Ronnie Gill","Halle Conway","Jeremy Meadows","Dora Velasquez","Hugh Church","Chris Leach","Magnus Bowers","Finnley Haney","Marjorie Velazquez","Franciszek Yoder","Irene Cummings","Dawn Burch","Chester Abbott","Siena Stark","Faris Tran","Gabriela French","Crystal Reese","Maia Mcknight","Joseph Morrow","Ismail Copeland","Ethel Koch","Teresa Sutton","Zaynab Gates","Ayub Jordan","Tia Alexander","Gareth Hanna","Laiba Lamb","Ajay Smith","Aarav Berg","Sana Blake","Miya Steele","Mariah Adams","Ieuan Mclaughlin","Ebony Moyer","Dillan Terry","Ollie Young","Taha Morton","Freddie Welsh","Vivian Mayer","Aoife Jennings","Carter Marsh","Sion Chandler","Rebekah Morrison","Sami Pollard","Lennox Berg","Kelsey Harding","Jodie Rhodes","Drew Estes","Ray Banks","Stella Howell","Stevie Wise","Mason Chambers","Elena Atkins","Brooke Kidd","Angel O'Sullivan","Billy Howe","Nadia Flynn","Pearl Graves","Darcey Middleton","Cody Rollins","Regan Mckay","Cai Rojas","Sienna Joseph","Jan Hartley","Shannon Welch","Phoenix Winters","Asa Walters","Francis O'Neill","Lee Delgado","Luna Preston","Juliet Conley","Katerina Stevenson","Devon Cummings","Rory Woods","Alexis Finch","Beau Haynes","Nana Suarez","Kaya Vang","Aidan Dean","Jay Kirby","Gabriel Gibson","Leslie Padilla","Morgan Velasquez","Tanya Monroe","Oakley Mcintyre","Kian Bullock","Zane Tate","Dante Castro","Wade Diaz","Zain Davenport","Casey Shaw","Marion Buchanan","Liberty Montes","Max Hart","Robbie Rubio","Erin Shaffer","Milan Snyder","Ashleigh Ashley","Sidney Hawkins","Mae Burton","Sana Weaver","Rowan Holt","Jaya Cooper","Evangeline Rivera","Jorge Ball","Kacie Oliver","Amelie David","Polly Jennings","Alexis Nolan","Lennox Andrews","Orla Whitehead","Olivia Black","Cindy Rogers","Jannat Stanley","Lara Horton","Jenna Jacobson","Madiha Rivers","Lisa Hahn","Syeda Perez","Lilli Molina","Samia Bloggs","Summer Hamilton","Delilah Butler","Cassandra Parsons","Brooklyn Holland","Sydney Roman","Jazmin Glover","Claire Malone","Emma Walton","Joanne Singleton","Bella Ortega","Annalise Mitchell","Kristina Ballard","Neha Fleming","Tamsin Johns","Chaya Henderson","Rebekah Davenport","Ayla Hudson","Maisy Salas","Thalia Soto","Mina Barlow","Evangeline Sparks","Wendy Lindsay","Bryony Robinson","Wanda Oconnor","Hannah Carney","Flynn Bullock","Neo Slater","Bushra Espinoza","Benedict Hunter","Coral Atkinson","Gwen Clarke","Ethel Vang","Serena Dickson","Zoe Mathews","Eliza Cobb","Sallie Mills","Vivian Odom","Shreya Tucker","Rowan Yoder","Sumaiya Acevedo","Dale Davidson","Lorraine Gould","Malika Guerra","Maariyah Tanner","Rhianna Knight","Husna Blackburn","Valentina Drake","Leila Bradford","Florence Blanchard","Lachlan Bird","Amy Haines","Kathryn O'Reilly","Esha Jacobs","Carla Bush","Lilly Saunders","Macauley Coffey","Ameera Fox","Esther Collier","Daniella Yang","Rayhan Holt","Abbey Villarreal","Aleeza Rush","Nate Kirk","Lula Mcguire","Irene Clark","Jan Wise","Sabrina Blaese","Keeley Singh","Taylor Klein","Faiza Petersen","Daisie Walters","Celeste Proctor","Elodie Fry","Soraya Adkins","Emelia O'Ryan","Ayesha Hines","Darcie Marshall","Callie Dotson","Kylie Mcdowell","Kacie Gates","Susie Strong","Lyla Kelley","Henrietta Long","Maddison Mccall","Melisa Pham","Sumayyah Melendez","Rehan Pineda","Rafe Walton","Laurie Sparks","Amin Whitaker","Marshall Valdez","Cordelia Cohen","Jade Bailey","Mohammed Kelley","Wesley Glover","Zak Hendricks","Beau Boyer","Victor Mcgee","Lucas Powers","Maya Proctor","Tristan Beasley","Seth Cotton","Uzair Juarez","Zaki Odling","Tatiana Anderson","Courtney Rivas","Max Mccormick","Anton Walsh","Olly Barker","Kaylum Hammond","Arjun Tate","Nathan Dean","Mackenzie Archer","Marissa Hanna","Abdullah Cummings","Luna Arias","Jago Goodwin","Yunus Phelps","Rahim Henry","Esme Petty","Colin Dickerson","Julia Carson","Edwin Andrade","Bradley Hart","Ruben Vaughn","Aaron Burke","Vinny Preston","Dylan Obrien","Eugene Cherry","Stefan Macdonald","Lennox Martin","Tobias Yang","Cody Mendez","Leroy Todd","Imran Mercado","Markus Winters","Bertie Petersen","Joe Heath","Rufus Dennis","Hamzah Clayton","Francis Salinas","Kaden Bryan","Yash Frye","Zane Franklin","Meredith Jefferson","Mason Ho","Oliwier Dickson","Ollie Morris","Eoin Gill","Dawid Nunez","Lexi Velasquez","Marley Stein","Kamil Kaufman","William Hunter","Stella Morton","Aidan Snyder","Owen Mata","Yasir Coleman","Joel Rodgers","Nate Sanders","Damian Hall","Harmony Connor","Chester Rubio","Josef Navarro","Earl Gaines","Sidney Tapia","Ray Thomas","Jan Cordova","Mario Montoya","Nicholas Pearce","Zakariya Sears","Justin West","Evan Sheppard","Ali Fowler","Awais Gomez","Keelan Holloway","Ismail Shannon","Armaan Stone","Kain Luna","Sid Edwards","Rory Perry","Archie Harris","Alistair Davila","Sufyan Strickland","Keane Ponce","Carlos Rowland"]


# driver = webdriver.Chrome()
old_agents = []
for page in range(1,TOTAL_PAGES+1):


    driver = uc.Chrome()
    
    current_page = f"{main_link}?page={page}"
    print("The current page is", current_page)
    driver.get(current_page)
    sleep(17)

    try:
        driver.find_element(by = By.XPATH, value = "//img[@src='https://i0.wp.com/www.beststartup.us/wp-content/uploads/cp_modal/modal_get_interviewed_cp_id_44c6a/cross-1.png?fit=22%2C22&ssl=1']").click()
    except:
        print("No pop up")

    sleep(5)

    # company_names_driver = driver.find_elements(by = By.XPATH, value = "//h3[@class='has-huge-font-size wp-block-heading']/span/strong")
    inside_company_urls_driver = driver.find_elements(by = By.XPATH, value = "//div[@class='wp-block-cover__inner-container is-layout-flow wp-block-cover-is-layout-flow']/p[1]/a[1]")
    # inside_company_urls_driver = driver.find_elements(by = By.XPATH, value = "//div[@class='wp-block-cover__inner-container']/p[1]/a[1]")
  
    # company_names = [current.text for current in company_names_driver]
    # print(company_names)
    inside_company_urls = [current.get_attribute("href") for current in inside_company_urls_driver]


    print("Total companies in the current page is ", len(inside_company_urls))

    sleep(5)

    driver.close()
    sleep(10)

    company_names = []
    company_websites = []
    final_social_links = []
    final_strengths = []
    final_founded_years = []
    final_abouts = []
    final_focuses = []

    # print(len(agents))
    

    # print(inside_company_urls)

    # COMPANIES_PER_PAGE = min(COMPANIES_PER_PAGE,1)
    COMPANIES_PER_PAGE = min(COMPANIES_PER_PAGE,len(inside_company_urls))

    for i,company_url in tqdm(enumerate(inside_company_urls)):
    # for company_url in ["https://www.crunchbase.com/organization/gametech-market"]: 

        print("Website number",i+1)

        try:
            
            sleep(3)
            # driver = webdriver.Chrome()
            # driver = uc.Chrome()
            while 1:
                rand_no = random.randint(0,len(agents)-1)
                current_agent = agents[rand_no]
                if current_agent in old_agents:
                    pass
                else:
                    old_agents.append(current_agent)
                    break
            # print(current_agent)



            print("This is the current agent", current_agent)
            opts = Options()
            opts.add_argument(f"user-agent={current_agent}")

            # driver = webdriver.Chrome(chrome_options=opts)
            driver = uc.Chrome()
            sleep(5)

            # company_url = "https://www.google.com/"
            print("Company Url", company_url)
            driver.get(company_url)
            sleep(30)


            # Clicking on the read more button
            
            try:
                print("Trying to press the read more button")
                driver.find_element(by = By.XPATH , value = "//button[@class='mdc-button mat-mdc-button mat-accent mat-mdc-button-base ng-star-inserted']").click()
                print("Pressed the read more button")
                # driver.find_element(by = By.XPATH , value = "//span[@class='mat-mdc-button-touch-target']").click()

            except:
                print("Not able to click the read more button")


            sleep(5)


            # Getting company name

            try:
                name_driver = driver.find_element(by = By.XPATH, value = "//h1[@class='profile-name']")
                name = name_driver.text
            except:
                name = "Not Available"



            # Getting company url

            try:
                # company_url_driver = driver.find_elements(by = By.XPATH, value = "//div[@class='wp-block-cover__inner-container is-layout-flow wp-block-cover-is-layout-flow']/p[1]/a[2]")

                company_url_driver = driver.find_elements(by = By.XPATH, value = "//a[@class='component--field-formatter accent ng-star-inserted']")

                url = company_url_driver[0].get_attribute("href")
            except:
                url = "Not Available"

            print("Found company url")

            sleep(2)


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


            print("Found social link")
            sleep(2)

            
            # Getting Strength
            print("Finding Strength")

            try:
                print("Inside try")

                

                strength_driver = driver.find_elements(by = By.XPATH, value = "//a[@class='component--field-formatter field-type-enum accent highlight-color-contrast-light ng-star-inserted']")

                # strength_driver = driver.find_elements(by = By.XPATH, value = "//a[@class='component--field-formatter field-type-enum link-accent highlight-color-contrast-light ng-star-inserted']")


                print("Strength driver worked")

                if len(strength_driver)>1:
                    strength = strength_driver[0].text.replace("'","")
                else:
                    strength = strength_driver[-1].text.replace("'","")

            except:
                strength = "Not Available"
                



            print("Found strenght")

            sleep(2)


            # Getting Founded year

            try:
                founded_year_driver = driver.find_element(by = By.XPATH, value = "//span[@class='component--field-formatter field-type-date_precision ng-star-inserted']")
                
                year = founded_year_driver.text
            except:
                year = "Not Available"


            print("Founded years")
        
            sleep(2)

            

            # Getting the about data

            temp_about = ""
            try:
                about_driver = driver.find_elements(by = By.XPATH, value = "//description-card[@class='ng-star-inserted']/div/span/p")

                for i in range(len(about_driver)):
                    temp_about = ",".join([temp_about,about_driver[i].text])
                
            except:
                pass

            if temp_about == "":
                temp_about = "Not Available"
            else:
                if temp_about[0] == ",":
                    temp_about = temp_about[1:]

            print("Found about")

            sleep(2)

            # Getting focus

            focus = []
            try:
                focus_driver = driver.find_elements(by = By.XPATH, value = "//ul[@class='text_and_value']/li[1]/field-formatter/identifier-multi-formatter/span/chips-container/a/chip/div/div")

                focus = [current.text for current in focus_driver]
            except:
                pass


            if focus == []:
                focus = "Not Available"

            print("Found focus")


            print()
            driver.close()
            sleep(10)

            company_websites.append(url)

            if temp_social_links == []:
                final_social_links.append("Not Available")
            else:
                final_social_links.append(temp_social_links)

            
            final_strengths.append(strength)
            final_founded_years.append(year)
            final_abouts.append(temp_about)
            final_focuses.append(focus)
            company_names.append(name)



        except:
            company_websites.append("Page got blocked")
            final_social_links.append("Page got blocked")
            final_strengths.append("Page got blocked")
            final_founded_years.append("Page got blocked")
            final_abouts.append("Page got blocked")
            final_focuses.append("Page got blocked")
            company_names.append("Page got blocked")

            print("This url is not opening",company_url)

        finally:

            with open(os.path.join(EXCEL_SAVING_PATH,f"company_names_page_{page}.txt"),"w+") as f:
                for name in company_names:
                    f.write(name)
                    f.write("\n")
                    
                # f.writelines(company_names)

            with open(os.path.join(EXCEL_SAVING_PATH,f"company_websites_page_{page}.txt"),"w+") as f:
                for website in company_websites:
                    f.writelines(website)
                    f.write("\n")

                # f.writelines(company_websites)
            with open(os.path.join(EXCEL_SAVING_PATH,f"final_social_links_page_{page}.txt"),"w+") as f:
                for link in final_social_links:
                    # for l in link:
                    f.write(str(link))
                    f.write("\n")

            with open(os.path.join(EXCEL_SAVING_PATH,f"final_strengths_page_{page}.txt"),"w+") as f:
                for strength in final_strengths:
                    f.writelines(strength)
                    f.write("\n")

            with open(os.path.join(EXCEL_SAVING_PATH,f"final_founded_years_{page}.txt"),"w+") as f:
                for year in final_founded_years:
                    f.writelines(year)
                    f.write("\n")
                    
            with open(os.path.join(EXCEL_SAVING_PATH,f"final_abouts_{page}.txt"),"w+") as f:
                for about in final_abouts:
                    f.writelines(about)
                    f.write("\n")

            with open(os.path.join(EXCEL_SAVING_PATH,f"final_focuses_{page}.txt"),"w+") as f:
                for focus in final_focuses:
                    # for temp_focus in focus:
                    f.write(str(focus))
                    f.write("\n")

            # with open(EXCEL_SAVING_PATH+"company_websites.txt","w+") as f:
            #     f.write(company_websites)







    df = pd.DataFrame(columns=columns)
    # df["Rating"] = ratings
    df["Strength"] = final_strengths
    df["Social Links"] = final_social_links
    df["Founded Year"] = final_founded_years
    # df["Services"] = services
    df["Focus Areas"] = final_focuses
    df["Name"] = company_names[:COMPANIES_PER_PAGE]
    df["Website"] = company_websites[:COMPANIES_PER_PAGE]
    df["About"] = final_abouts

    # main_df.append(df)
    main_df = pd.concat([main_df, df], axis=0)

    main_df.to_excel(f"{EXCEL_SAVING_PATH}/main_beststartup_test.xlsx")
    df.to_excel(f"{EXCEL_SAVING_PATH}/Page_{page}.xlsx")
    


display.stop()
# 
