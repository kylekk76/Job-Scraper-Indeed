# Job-Scraper - Started - 9/08/2022
### What this proyect is about:

I would like to have a program that i can run every 2 days or so, filter for me all the jobs and clean the information so everything is in the right format.
My idea is to have all the data as tidy up as posible to have a better idea of the market at the moment, also i would like to see how the job market is evolving throw the next 6 months or so.... so i can have some information of the diferent areas of the city jobwise to conect it with my next proyect about housing market... as i want to buy a house next year.


### Way to use:(This scraper is based in UK so would you will need to do some changes for your contry)

- In the jupyter notebook you have how this program works in a early version, any questions just ask.
#Updated# (02/09/2022)
Open the folder "program" and run the mainScraper.py you should have installed the librarys and the pack to read xlsx as this are the files that you gonna use to run the program, you need then to imput diferent things for the search and the rest is automatic.

You will have 4 files created, raw data(this is the data as come from the scraping), clean data (this is the data processed), data base (this is where all the search gonna be stored), data analyst base (this is a file just to storage that job)


### Possibles bugs:
- Could be happend as before that indeed or other page upgrade their security and this program not longer work giving you an 403 error, in that case i would look arround how to go arround.
- Depends of your Country is posible that their webpage is port in a diferent way and some of the code need be adapted for the       display that you have
- If you use a lot this program would give an error, but after 12h you can use it as normal.

The rest of the Code should work fine, if something its not working in your computer report to me, but is posible you have some missing packet or libraries.

### To Implement:
- [x] Loop to go throw all the pages avaliable (05/09/2022)
- [x] Clean the data for pos-procesing. (02/09/2022) 
- [x] Search for diferent jobs. (01/09/2022) 
- [x] Save to an excel file (22/08/2022)
- [x] Search for diferent locations (in UK 29/08/2022)
- [ ] Scrape more information about the jobs
- [ ] Add diferent pages as a linked id to the scraping to not use just indeed.
- [ ] Data plots.
- [x] Search for diferent industrys (02/09/2022) fixed(05/09/2022)
- [x] Data Base to store all the jobs since you start to use the program.(02/09/2022)

### Log:
- Fixed the dataframe to get the payrate separate in 2 columns and in the right type. (25/08/2022)
- Fixed the Localization Column to now be separate in City and Area. (25/08/2022)
- Create a visualization by job title, salary and jobs quantities posted for that group.(26/08/2022)
- Set up all the columns in the right format and eliminated the repited jobs(29/08/2022)
- Set up the basic program to run in python and create all the right files to use later (29/08/2022)
- Fixed a problem with the replicate jobs in the clean data and the database (02/09/2022)
- Remodelate a bit the program to make it more readable and organized. (02/09/2022)
- Added dinamic industry choise (05/09/2022)
- Group all in one file (05/09/2022)
- Diferent Choises to do a personalize search (05/09/2022)

