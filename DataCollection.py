#----------------------------------------------------------#
# Author: Anurodh Mohapatra
# Date: 13 Jan 2021
#----------------------------------------------------------#

# Importing Modules
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

# Creating time string to give fie name
timestr = time.strftime("%Y%m%d-%H%M%S")

# Creating empty list
BHK = []
Area = []
Latitude = []
Longitude = []
Size = []
Deposit = []
Rent = []
Type = []
Age = []
For = []
Possesion = []
Link = []

# Function to scrape 
def scrape_NoBroker(n):

    print(f'Exporting {n} rows!!!')

    try:
        for page in range(int(n/10)):
            
            try:
                print(f'{(page+1)*10} rows added!!!')

                # Requesting URL
                url = requests.get('https://www.nobroker.in/property/rent/bangalore/Bangalore/?searchParam=W3sibGF0IjoxMi45NzE1OTg3LCJsb24iOjc3LjU5NDU2MjcsInBsYWNlSWQiOiJDaElKYlU2MHlYQVdyanNSNEU5LVVlakQzX2ciLCJwbGFjZU5hbWUiOiJCYW5nYWxvcmUifV0=&sharedAccomodation=0&orderBy=nbRank,desc&radius=2&traffic=true&travelTime=30&propertyType=rent&pageNo='+str(page)).text
                
                # Converting from HTML tag to BeautifulSoup object
                soup = BeautifulSoup(url,'lxml')

                # Finding all the div tag wich contains all the info
                houses = soup.find_all('div',class_='card')
            
                # Looping through each div tag to get individual content
                for house in houses:
                    BHK.append(house.find('a',class_='card-link-detail')['title'][:1])
                    Area_raw= house.find('a',class_='card-link-detail')['title']
                    if ',' in Area_raw:
                        Area.append(Area_raw.split(',')[-1])
                    else:
                        Area.append(Area_raw.split('in',1)[-1])    
                    Latitude.append(house.find('meta',itemprop='latitude')['content'])
                    Longitude.append(house.find('meta',itemprop='longitude')['content'])
                    Size.append(house.find_all('meta',itemprop='value')[0]['content'])
                    Deposit.append(house.find_all('meta',itemprop='value')[1]['content'])
                    Rent.append(house.find_all('meta',itemprop='value')[2]['content'])
                    Type.append(house.find_all('h5',class_="semi-bold")[0].text)
                    Age.append(house.find_all('h5',class_="semi-bold")[1].text)
                    For.append(house.find_all('h5',class_="semi-bold")[2].text.replace('\n',''))
                    Possesion.append(house.find_all('h5',class_="semi-bold")[3].text.replace('\n',''))
                    Link.append(house.find('a',class_='card-link-detail')['href'])
            except:
                print(f'Row number {(page+1)*10} failed. Trying next one!!!')        
    except:    
        pass

    # Creating DataFrame and storing data
    df = pd.DataFrame(list(zip(BHK,Area,Latitude,Longitude,Size,Deposit,Rent,Type,Age,For,Possesion,Link)),
                      columns=['BHK','Address','Latitude','Longitude','Size(Acres)','Deposit(Rs)','Rent(Rs)',
                               'Furnishing','Property Age','Available For',' Immediate Possesion','Link'])
        
    # Exporting DataFrame in form of CSV file
    File_name = "House_Data_"+timestr+".csv"
    df.to_csv(File_name,index=False)
    print("File Exported Sucessfully!!!!")      

scrape_NoBroker(10000)                  