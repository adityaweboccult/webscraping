
import os
import numpy as np
import pandas as pd
from tqdm import tqdm


CITY = "texas"
EXCEL_SAVING_PATH = f"excel_shared_to_scrape/third/wellfound/{CITY}_excels"
SAVING_PATH = f"excel_shared_to_scrape/third/wellfound/{CITY}_txts"
TOTAL_PAGES = 3
MAIN_DF_PATH = f"{EXCEL_SAVING_PATH}/main_wellfound_till_page_{TOTAL_PAGES}_v1.xlsx"
SAVE = True

print("Saving the file to ",SAVING_PATH)

columns = ["Name","Website","Strength","About","Focus Areas"]

if not os.path.exists(MAIN_DF_PATH):
    main_df = pd.DataFrame(columns=columns)
else:
    main_df = pd.read_excel(MAIN_DF_PATH)


for CURRENT_PAGE in tqdm(range(3,TOTAL_PAGES+1)):
# CURRENT_PAGE = 1
# try:
    with open(f"{SAVING_PATH}/focus_areas_page_{CURRENT_PAGE}.txt", "r") as f:
        data = f.readlines()

    focus_areas = []

    for current_industry in data:
        splitted_data = [value[-100:] for value in current_industry.split("</a")]

        temp_focus = []


        for i,temp in enumerate(splitted_data[:-1]):
            try:
                temp_focus.append(temp.split('">')[-1])
            except:
                pass

        if len(temp_focus) == 0:
            temp_focus = "Not Available"
        else:
            focus_areas.append(temp_focus)

    with open(f"{SAVING_PATH}/company_names_page_{CURRENT_PAGE}.txt", "r") as f:
        company_names = [data.replace("\n","").strip() for data in f.readlines()]
    print("Total Compnies", len(company_names))

    with open(f"{SAVING_PATH}/people_strength_page_{CURRENT_PAGE}.txt", "r") as f:
        people_strength = [data.replace("\n","").replace("'","").strip() for data in f.readlines()]
    print("Total Company Strenghts Count" ,len(people_strength))


    with open(f"{SAVING_PATH}/company_websites_page_{CURRENT_PAGE}.txt", "r") as f:
        company_websites = [data.replace("\n","").strip() for data in f.readlines()]
    print("Total Websites",len(company_websites))



    # print(CURRENT_PAGE)
    # if os.path.exists(f"{SAVING_PATH}/abouts_page_{CURRENT_PAGE}.txt"):
    #     print("YEs")
    with open(f"{SAVING_PATH}/abouts_page_{CURRENT_PAGE}.txt", "r",encoding="utf8") as f:
        about_data = f.readlines()
    print("Total About", len(about_data))


    abouts = []
    for i,data in enumerate(about_data):

        profile_data = ""
        for char in data:
            if char == "<":
                # to_remove_text = "<"
                to_ignore = True
            elif char == ">":
                to_ignore = False 
            if not to_ignore:
                profile_data = "".join([profile_data,char])
                # to_remove_text =  "".join([to_remove_text,char])
                # to_ignore = False

            # if to_remove_text:

            # to_remove_text =  "".join([to_remove_text,char])
        about = profile_data.split(">>Industries")[0].split(">>>>")[-1].replace(">","")

        if about == "":
            about = "Not available"
        abouts.append(about)
        # print(i,profile_data.split(">>Industries")[0].split(">>>>")[-1].replace(">",""))
        # print()


    # with open(f"{SAVING_PATH}/abouts_page_{CURRENT_PAGE}.txt", "r") as f:
    #     about_data = f.readlines()

    # abouts = []

    # for i,data in enumerate(about_data):
    #     try:
                
    #         try: #when we press readmore
    #             temp_data = data.split('class="styles_component__481pO"><div>')[1]
    #         except:
    #             temp_data = data.split('class="styles_component__481pO">')[1]


    #         if temp_data[0] == "<":
    #             temp_data = temp_data.split(f"</{temp_data[1]}>")[1]

    #         split_by_dot = temp_data.split(".")[:-1]
    #         split_by_dot = ".".join(split_by_dot)
    #         split_by_dot = split_by_dot.replace("amp;","").replace("<!-- -->","").replace("<br>","\n")   

    #         #removing the remaining anchor tag
    #         try:
    #             split_by_a = split_by_dot.split("<a")[0]

    #             remaining_from_a = split_by_dot.split(">")[1]

    #             # print(split_by_a)
    #             # print()
    #             # print(remaining_from_a[1])
    #             about = " ".join([split_by_a,remaining_from_a])
    #         except:
    #             about = split_by_a
    #     except:
    #         about = "Not Available"

    #     # print(i,split_by_a)
        
    #     abouts.append(about.replace("</a",""))

    # for i,(a,f)in enumerate(zip(abouts,focus_areas)):
    #     print(i,a)
    #     print(f)
    #     print()


    # final_strenght = []
    # for s in people_strength:
    #     try:
    #         final_strenght.append(s.split("'")[1])
    #     except:
    #         final_strenght.append(s)

    if SAVE:
            

        df = pd.DataFrame(columns=columns)
        # df["Rating"] = ratings
        df["Strength"] = people_strength
        # df["Social Links"] = all_social_links
        # df["Founded Year"] = founded_year
        # df["Services"] = services
        df["Focus Areas"] = focus_areas
        df["Name"] = company_names
        df["Website"] = company_websites
        df["About"] = abouts

        # main_df.append(df)
        main_df = pd.concat([main_df, df], axis=0)

        main_df.to_excel(MAIN_DF_PATH)
        df.to_excel(f"{EXCEL_SAVING_PATH}/Page_{CURRENT_PAGE}_v1.xlsx")
# except:
#     pass