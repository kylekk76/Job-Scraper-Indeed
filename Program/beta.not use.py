import cloudscraper
from bs4 import BeautifulSoup
import pandas as pd
import math
import re


joblist=list()
def input_data():
    print("The visualization is not implemented yet, for now we just got the basics")
    #input all the data
    job=input("Introduce job Tittle: ")
    if len(job) >= 1: job = "%20".join(job.split())
    place=input("Input City: ").capitalize()
    radius=input("input Radius, 5, 10, 15, 25, 50, 100 miles: ")
    url=url=f'https://uk.indeed.com/jobs?q={job}&l={place}%2C%20{place}&radius={radius}&start=0'
    return job, place, radius, url

def extract_the(page=0,url="",job="",place="",radius="",):

    scraper = cloudscraper.create_scraper(delay=10, browser={'browser': 'firefox','platform': 'windows','mobile': False})
   
    r = scraper.get(url)
    soup= BeautifulSoup(r.text,"html.parser")
    #print(r) #debug
    return soup,r

def select_industry(soup,job,place,radius):
    list_industry=[]
    question=input("Would you like to search in general or to pick an industry?, Y/N ").capitalize()
    if question=="Y":
        number=soup.find_all("div",class_="yosegi-FilterPill-dropdownPillContainer")
        list_industry_s=number[7].find_all("a",class_="yosegi-FilterPill-dropdownListItemLink")
        for n in list_industry_s:
            list_industry.append((n.text,re.findall(r"\(([A-Z0-9]*)\)",n['href'])[0]))
        for job in list_industry:
            print(job[0])
        try: 
            industry_question=int(input("The first industry is 0, the second 1, the third 3... introduce the number: "))
            industry=list_industry[industry_question][1]
            url=f'https://uk.indeed.com/jobs?q={job}&l={place}%2C%20{place}&sc=0kf%3Acmpsec({industry})%3B&radius={radius}&start=0'
        except: 
            print("Sorry incorrect Data, try again later...")
            url=f'https://uk.indeed.com/jobs?q={job}&l={place}%2C%20{place}&radius={radius}&start=0'
    else: url=f'https://uk.indeed.com/jobs?q={job}&l={place}%2C%20{place}&radius={radius}&start=0'
    return url

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
        print(jobs) #rememebr take this out ########################
        joblist.append(djobs)    
        
        return 

def number_of_pages(soup):

    try:
        number=soup.find_all("div",id="searchCountPages")[0].text.split()[3]
    except: number=None
    if number == str(number): #this is to check we get something from the last part of code
        number = int(number)
        number_pages = math.ceil(number/15)
        print("Scraping the 10 or less pages ")
        

    else: 
        print("There are 15 jobs per page")
        number_pages = int(input("how many pages do you wanna scrape?: "))
        
    if number_pages >10: number_pages=10 # we maximun wanna do 10 pages because the rest of results are normally very far
    return number_pages

def cleanData(dfraw):

    print("Cleaning the Data")
    df=dfraw.sort_values("Status").drop_duplicates("Link",keep="first")

    #We extract each of the groups in in the status to later build a timer
    employer=df["Status"].str.extract("(Employer)(\d{1,2})")
    posted=df["Status"].str.extract(".(Posted)\s(\d{1,2})*")
    posted2=df["Status"].str.extract("(Posted)(\d{1,2})")
    active=df["Status"].str.extract(".(Active)\s(\d{1,2})")
    df["Status"]=df["Status"].str.replace("PostedJust posted","PostedToday")
    df["Status"]=df["Status"].str.replace("PostedToday","Posted Today")
    postedToday=df["Status"].str.extract("(Posted)\s(Today)")


    #Time to fill all the dataframe 
    posted=posted.fillna(active)
    posted=posted.fillna(employer)
    posted=posted.fillna(posted2)
    posted=posted.fillna(postedToday)
    posted=posted.fillna("0")
    #wecould do this replace in regex, but i though was going to be easy do it later on
    posted[1]=posted[1].replace("Today","0")
    
    #Now we change to int to can use the timedelta
    posted[1]=posted[1].astype(int)

    #And we apply a lambda to each number to transform it in a date
    posted[1]=posted[1].apply(lambda date: (pd.to_datetime("today")-pd.Timedelta(days=date)).strftime("%d/%m/%Y") )
    

    df[["Status","Last_Active_or_Posted"]]=posted

    #we divide the colum salary in 2
    df[["Starter_Salary","Top_Salary"]]=df["salary"].str.extract(r"£(\d{2},*\d*)?(?:.*)?£(\d*,*\d*)")
    df["Top_Salary"]=df["Top_Salary"].fillna(df["salary"].str.extract(r"£([0-9,]*)")[0])
                                    

    df.drop("salary",axis=1,inplace=True)
    df["Starter_Salary"].fillna(df["Top_Salary"],inplace=True) 

    #we use lambda to clean the "," from the numbers and convert the type to float so we can use it
    df[["Starter_Salary","Top_Salary"]]=df[["Starter_Salary","Top_Salary"]].apply(lambda x: x.str.replace(",","")).astype(float)

    # we clean the posible spaces from the database
    df["Location"]=df["Location"].str.strip()

    # And we extract the  city and the area from the location
    city=df["Location"].str.extract(r"^(?:Hybrid)[^A-Z]*([A-Z][a-z]*)|([A-Z][a-z]*)")
    city[0].fillna(city[1],inplace=True)
    df["City"]=city[0]

    df["Area"]=df["Location"].str.extract(r"([A-Z]\d{1,2})")
    df.drop("Location", axis=1, inplace=True)

    #Clean The title
    df["Title"]=df["Title"].str.split().apply(lambda title: [word.capitalize() for word in title]).str.join(" ")

    # We tidy up a bit the board
    df.sort_values("Starter_Salary",ascending=False,inplace=True)
    df.set_index(df.columns[0],inplace=True)
    df.index.name=""
    dataCleandf=df

    print("Data Cleaned")
    return dataCleandf

def save_all_data(dfraw,dataCleandf):
    print("Saved in Excel RawData")
    dfraw.to_excel('RawData.xlsx')
    print("Saving Clean Data in Excel File")
    dataCleandf.to_excel("CleanData.xlsx")

    print("this is the dataset shape",dataCleandf.shape)

    question=input("Do you want to add this search to the Database?: ").capitalize()
    if question == "Y":
        print("Procesing...")
        database=pd.read_excel("DataBase.xlsx")
        newdatabase=database.append(dataCleandf)
        newdatabase.drop_duplicates(["Link","Last_Active_or_Posted"],keep="first",inplace=True)
        #newdatabase.reset_index(drop=True,inplace=True)
        newdatabase.sort_values("Last_Active_or_Posted",inplace=True)
        newdatabase.to_excel("Database.xlsx")
    elif question == "K":
        print("Procesing Data Analyst Jobs...")
        database=pd.read_excel("DataAnalystBase.xlsx")
        newdatabase=database.append(dataCleandf)
        newdatabase.drop_duplicates(["Link","Last_Active_or_Posted"],keep="first",inplace=True)
        #newdatabase.reset_index(drop=True,inplace=True)
        newdatabase.sort_values("Last_Active_or_Posted",inplace=True)
        newdatabase.to_excel("DataAnalystBase.xlsx")

    else: print("You did not make changes in the Data Base")

    print("All the data is Saved")

def main():
    
    job, place, radius,url=input_data()
    pages=list([0,10,20,30,40,50,60,70,80,90])
    for_pages,conection=extract_the(0,url,job,place,radius)
    print(conection)
    url=select_industry(for_pages,job,place,radius)
    number=number_of_pages(for_pages)
    

    print("Extracting info")
    joblist=list()
    for page in pages[0:number]: # run throw the first 10 pages
        info=extract_the(page,url,job,place,radius)[0]
        transform(info)

    print("Generating Data frame")
    dfraw=pd.DataFrame(joblist) #creating a dataframe
    print(dfraw)
    print(joblist)
    dataCleandf=cleanData(dfraw)
    save_all_data(dfraw,dataCleandf)

if __name__ == "__main__":
    main()