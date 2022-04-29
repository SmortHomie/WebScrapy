import scrapy
import csv
import pandas as pd

class CareerG_Spider(scrapy.Spider):
    '''
    Spider to scrape CareerGuide Data
    '''
    name='CareerGuide'
    start_urls=['https://www.careerguide.com/career-options']

    def parse(self,response):
        for jobs in response.css('div.row >  div.col-md-4'):
            title=jobs.css('h2 > a::text').get()
            for i in jobs.css('ul li a::text'):
                yield {
                    'Category':title,
                    'Subcategory':i.get()
                }

    ''' Output will get stored in CareerG.csv'''

class LinkedInJob_Spider(scrapy.Spider):
    '''
    Spider to scrape LinkedIn jobs info from CareerGuide Data
    '''
    name='LinkedInJob'
    
    #Importing Scraped Data from CareerGuide
    jobs = pd.read_csv('D:\WebScrapy\ATG_Scraping\CareerG.csv')

    #Here I only chose first 10 subcategories, because the size of this list is 6000
    #And passing all subcategories throws 409 Too many Requests Error
    # and It'll also take much time
    SubCat=list(jobs['Subcategory'])[0:10]

    #Shortlisted this 5 States to pass as Location Parameter
    States=['Maharashtra','Tamil Nadu','Kerala','Gujrat','Delhi']

    start_urls=[]

    #Creating all possible search queries with all Categories and State
    for S in States:
        for Sub in SubCat:
            start_urls.append('https://www.linkedin.com/jobs/search?keywords={}&location={},India&position=1&pageNum=1'.format(Sub,S))

    def parse(self,response):
        Comp=[]
        fieldname=['ComName','Link']
        for Jobs in response.css('ul.jobs-search__results-list li> div > div.base-search-card__info'):
            Post=Jobs.css('h3::text').get().strip()
            cName=Jobs.css('h4 a::text').get().strip()
            cLink=Jobs.css('h4 a').attrib['href']
            Loc=Jobs.css('span.job-search-card__location::text').get().strip()
            Comp.append({
                'ComName': cName,
                'Link' : cLink
            })
            yield {
                'Designation':Post,
                'Company':cName,
                'Location':Loc
            }
            ''' Output will get stored in LinkedInJob.csv'''

        with open('Comp.csv', 'a') as csvfile:
            #Saving Comapany Details such as Name and LinkedIn Company Profile Link to Scrape
            writer = csv.DictWriter(csvfile, fieldnames = fieldname)
            writer.writerows(Comp)

class LinkedIn_Comp_Spider(scrapy.Spider):

    '''
    Spider to scrape Comap
    '''
    name='LinkedInComp'
    start_urls=[]

    cName=pd.read_csv('D:\WebScrapy\ATG_Scraping\Comp.csv')
    start_urls=list(cName['Link'])

    user_agent= 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'

    def parse(self,response):
        pass
