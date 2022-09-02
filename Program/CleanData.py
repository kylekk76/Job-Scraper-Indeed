import pandas as pd

def cleanData():
    print("Cleaning the Data")
    df=pd.read_excel("RawData.xlsx")
    df=df.sort_values("Status").drop_duplicates("Link",keep="first")

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

    # ############################################################################

    # #Jpaymore stands for Jobs that pay more
    # Jpaymore=df.groupby("Title").max("Starter_Salary")
    # Jpaymore["Count"]=df.groupby("Title")["Title"].count()
    # Jpaymore.reset_index(inplace=True)
    # #creating a serie to extract the tittle to reduce the variance
    # payserie=Jpaymore["Title"].str.extract(r"(^[A-z][a-z]+\s[A-za-z\s&]+)|(.*)")
    # payserie[0].fillna(payserie[1],inplace=True)
    # Jpaymore["Title"]=payserie[0]
    # Jpaymore.sort_values(by="Starter_Salary",ascending=False,inplace=True)
    print("Data Cleaned")
    return dataCleandf