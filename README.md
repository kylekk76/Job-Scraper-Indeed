# Job-Scraper - Started - 9/08/2022
### What this proyect is about:

This is the first proyect that i try to deal with an issue and it's that i do not like much the way linked id present the jobs as
much as you got plenty of choises:

Is dificult to keep track of the diferent jobs.
Compare them
Look if you are a good fit for them, or they are for you.
if they are underpaying for the actual market of in another hand its a good pay for your work.

I would like to have the information scraped from diferent pages and create diferent metrics and have them plots on a geomap as:

- What jobs have a higher salary
- What kind of jobs are offer more often
- What kind of skills are more requiered
- what zones, area or places are offer the best jobs
- etc...

I know i can check probably all that stats from the webpages, but as i say is a lot of clicks and dificult to keep the track, would be wonderfull have all the information to just one click, so that is my plan with this wee proyect.

Anyway this gonna be especially usefull when it could store the information for a month or so and we could study what is the better option to afront the market.

### Way to use:
Until is a bit more developed, you would scrape the data with the job scraper and clean it with the cleaner file.

In a future would be all in a automatic program that just need to be run once, and will create all the plots and necesary files.


### Possibles bugs:
- Could be as happend before that indeed or other page upgrade their security and this program would not longer work giving you an   403 error, in that case i would look arround how to go arround.
- Depends of your Country is posible that their webpage is port in a diferent way and some of the code need be adapted for the       display that you have
- The link that i use to go throw the pages is thatone that you get for few seconds after click in a second page of a search, that   gives you a link to iterate for the pages, is posible that you gonna need for now to change that link to your own.

The rest of the Code should work fine, if something its not working in your computer report to me, but is posible you have some missing packet or module.

### To Implement:
- [x] Loop to go throw all the pages avaliable (i will not implement this as after a maximun of 10 pages the result is useles)
- [x] Clean the data for pos-procesing. (22/08/2022) **Not finished**
- [x] Searcher for diferent jobs. (21/08/2022) **Not finished**
- [x] Save to an excel file (22/08/2022)
- [ ] Searcher for diferent locations (right know when you pastle your link search in your last location).
- [ ] 2nd part that when you select a list of jobs, scrape more information about it
- [ ] Add diferent pages as a linked id to the scraping to not use just indeed.
- [ ] Plot the data in a interactive geomap.
- [ ] Analize the data and install some models of machine learning to select jobs and best areas.
- [ ] Store the data from diferent searches in the same place.

### Log:
- fixed the dataframe to get the payrate separate in 2 columns and in the right type. (25/08/2022)
- fixed the Localization Column to now be separate in City and Area. (25/08/2022)
- create a visualization by job title, salary and jobs quantities posted for that group.(26/08/2022)
