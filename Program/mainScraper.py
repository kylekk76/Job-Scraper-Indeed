#import requests
import cloudscraper
from bs4 import BeautifulSoup
import pandas as pd

from CleanData import cleanData

#### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### ####
dataCleandf=pd.DataFrame()
print("The visualization is not implemented yet, for now we just )got the basics")
joblist=[]
job=input("Introduce job Tittle: ")
if len(job) >= 1: job = "%20".join(job.split())
place=input("Input City: ").capitalize()
radius=input("input Radius, 5, 10, 15, 20, 50 miles: ")
print("Do you want to search by industry?")
industryQ=input("Introduce Y or N: ").capitalize()

print("""
1 Retail & Wholesale                            8  Management & Consulting                          15 Arts, Entertainment & Recreation 
2 Human Resourses & Staffing                    9  Information Technology                           16 Energy, Mining, Utilities
3 Restaurant & Food Service                     10 Non-profit & NGO                                 17 Pharmaceutical & Biotechnology
4 Construction, Repair & Maintenance Services   11 Government & Public Administration               18 Education
5 Healthcare                                    12 Manufacturing                                    29 Media & Communication
6 Finance                                       13 Telecommunications
7 Hotel & Travel Accommodation                  14 Real Estate
              """)

dit={"1":"48BZP","2":"Q3FC3","3":"W2F4E","4": "NTW8X", "5":"22VKN","6":"MSQWR","7": "X42V4", "8":"92AZY","9":"NKR5F","10":"ZMM32","11":"B23RH","12":"CPGHF","13":"JGU5R","14":"S7KHR",
        "15":"N322U","16":"TAN6J","17":"5ZM33","18":"RFWNN", "19":"4DGEF"}
if industryQ == "Y": industry=dit[input("Input the number of the industry you wanna concentrate on: ")]




def extract_the(page=0):

    scraper = cloudscraper.create_scraper(delay=10, browser={'browser': 'firefox','platform': 'windows','mobile': False})

    if industryQ == "N": url=f'https://uk.indeed.com/jobs?q={job}&l={place}%2C%20{place}&radius={radius}&start={page}' # placeholder to go throw the information we need
    if industryQ == "Y": url=f'https://uk.indeed.com/jobs?q={job}&l={place}%2C%20{place}&sc=0kf%3Acmpsec({industry})%3B&radius={radius}&start={page}'
    
    r = scraper.get(url)
    soup= BeautifulSoup(r.text,"html.parser")
    return soup,r
    
print(extract_the()[1])

def transform(soup):

    jobs=soup.find_all("div",class_="job_seen_beacon") # the list that it gives us back is each of the jobs
    for job in jobs: # we go throw the list finding what we need and adding all of this to a dictionary
        djobs={
        "Title"      :job.find("a").text.strip(),
        "Company"    :job.find("span",class_="companyName").text.strip(),
        "Location"   :job.find("div",class_="companyLocation").text.strip(),
        "Link"       :"https://uk.indeed.com/viewjob?jk="+ job.find("a").attrs["data-jk"],
        "Status"     :job.find("span",class_="date").text.strip()
        }
        try: # some of them do not have salary so to try evade errors we do a try and except
            djobs["salary"]=job.find("div",class_="metadata salary-snippet-container").text.strip()
        except:
            djobs["salary"]="Not Declared"
        try: # this sometimes give error, i can not find the problem yet, so we leave here
            djobs["Description"]=job.find("li").text.strip()
        except:
            djobs["Description"]="Not Found"
            
        joblist.append(djobs)
    return 

def save_all_data(dfraw,dataCleandf):
    print("Saved in Excel RawData")
    dfraw.to_excel('RawData.xlsx')
    print("Saving Clean Data in Excel File")
    dataCleandf.to_excel("CleanData.xlsx")
    # Jpaymore.to_excel("GroupsData.xlsx")
    
    question=input("Do you want to add this search to the Database?: ").capitalize()
    if question == "Y":
        print("Procesing...")
        database=pd.read_excel("DataBase.xlsx")
        newdatabase=database.append(dataCleandf)
        newdatabase.drop_duplicates(["Link","Last_Active_or_Posted"],keep="first",inplace=True)
        newdatabase.sort_values("Last_Active_or_Posted",inplace=True)
        newdatabase.to_excel("Database.xlsx")
    elif question == "K":
        print("Procesing Data Analyst Jobs...")
        database=pd.read_excel("DataAnalystBase.xlsx")
        newdatabase=database.append(dataCleandf)
        newdatabase.drop_duplicates(["Link","Last_Active_or_Posted"],keep="first",inplace=True)
        newdatabase.sort_values("Last_Active_or_Posted",inplace=True)
        newdatabase.to_excel("DataAnalystBase.xlsx")

    else: print("You did not make changes in the Data Base")

    print("All the data is Saved")


def main():
    pages=list([0,10,20,30,40,50,60,70,80,90])
    print("Extracting info")

    for page in pages: # run throw the first 10 pages
        info=extract_the(page)[0]
        transform(info)
    print("Generating Data frame")
    dfraw=pd.DataFrame(joblist) #creating a dataframe
    dataCleandf=cleanData()
    save_all_data(dfraw,dataCleandf)
    

if __name__ == "__main__":
    main()