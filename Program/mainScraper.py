#import requests
import cloudscraper
from bs4 import BeautifulSoup
import pandas as pd

###
from CleanData import cleanData


print("The visualization is not implemented yet, for now we just got the basics")
joblist=[]
job=input("Introduce job Tittle: ")
place=input("Input City: ").capitalize()
radius=input("input Radius, 5, 10, 15, 20, 50: ")
if len(job) >= 1: job = "%20".join(job.split())


def extract_the(page=0):
    scraper = cloudscraper.create_scraper(delay=10, browser={'browser': 'firefox','platform': 'windows','mobile': False})
    url=f'https://uk.indeed.com/jobs?q={job}&l={place}%2C%20{place}&radius={radius}&start={page}' # placeholder to go throw the information we need
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



def main():
    pages=list([0,10,20,30,40,50,60,70,80,90])
    print("Extracting info")

    for page in pages: # run throw the first 10 pages
        info=extract_the(page)[0]
        transform(info)
    print("Generating Data frame")
    df=pd.DataFrame(joblist) #creating a dataframe
    df.to_excel(f'RawData.xlsx')
    print("Saved in Excel RawData")
    print("Cleaning the Data")
    cleanData()
    print("All Data Save")


if __name__ == "__main__":
    main()