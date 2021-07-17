from requests import get
from bs4 import BeautifulSoup
import time




pagenumber = 1

for i in range(20):



    pagenumber_string = str(pagenumber)

# Read Web URL
    response = get('https://www.autoscout24.be/nl/lst/?sort=age&desc=1&ustate=N%2CU&size=20&page=' + pagenumber_string + '&cy=B&atype=C&')

#LOAD Page into URL
    html_soup = BeautifulSoup(response.text, 'html.parser')

# Get array of all cars listed on page
    cars = html_soup.find_all('div', class_="cldt-summary-full-item-main")



    CarID = 0

    for n in cars:

    

# Select Car
        first = cars[CarID]

# Get Car Name
        CarName_holder = first.find_all('h2', class_="cldt-summary-makemodel sc-font-bold sc-ellipsis")
        CarName = CarName_holder[0].get_text()

# Get Car Price
        CarPrice_holder = first.find_all( class_="cldt-price sc-font-xl sc-font-bold" )
        CarPrice = CarPrice_holder[0].get_text()
        startchar = CarPrice.find('€')
        stopchar = CarPrice.find(',')
        CarPrice = CarPrice[startchar+2:stopchar]
        seperator = CarPrice.find(".")
        CarPrice_hundreds = CarPrice[seperator+1:]
        CarPrice_thousands = CarPrice[:seperator]
        CarPrice = CarPrice_thousands + CarPrice_hundreds

# Get Unique ID
        CarUniqueID_holder = first.find_all( class_="cldt-summary-titles")
        CarUniqueID_string = str(CarUniqueID_holder)
        URLtoken_start = CarUniqueID_string.find("href")
        URLtoken_stop = CarUniqueID_string.find('<div class="cldt-summary-title"')
        UniqueURL = CarUniqueID_string[URLtoken_start+6:(URLtoken_stop-3)]
        
        


# Get Car Details
        CarDetails_holder = first.find_all(class_="cldt-summary-vehicle-data")
        CarDetails = CarDetails_holder[0].find_all("li")

# Car Mileage
        CarMileage = CarDetails[0].get_text()
        stopchar = CarMileage.find('km')
        CarMileage = CarMileage[0:stopchar]
        seperator = CarMileage.find('.')

        if seperator == (-1):
            CarMileage = CarMileage[1:-1]

        if seperator != (-1):
            CarMileage_hundreds = CarMileage[seperator+1:]
            CarMileage_thousands = CarMileage[1:seperator]
            CarMileage = CarMileage_thousands + CarMileage_hundreds



# Build Date
        BuildDate = CarDetails[1].get_text()
        BuildMonth = BuildDate[1:3]
        BuildYear = BuildDate[4:8]

#Power
        Power = CarDetails[2].get_text()
        kwchar = Power.find("kW")
        Power = Power[1:kwchar]

#Usage
        Usage = CarDetails[3].get_text()
        Usage = Usage[1:-1]

#Transmissin
        Transmission = CarDetails[5].get_text()
        Transmission = Transmission[1:-1]

#Fuel
        Fuel = CarDetails[6].get_text()
        Fuel = Fuel[1:-1]

        #print(CarUniqueID_holder)
        print(UniqueURL)
        print(pagenumber)
        print(CarID)
        print(CarName)
        print(CarPrice)
        print(CarMileage)
        print(BuildMonth)
        print(BuildYear)
        print(Power)
        print(Usage)
        print(Transmission)
        print(Fuel)

    # Write To File
        f = open("DATA.txt", "a")
        f.write(pagenumber_string + ", ")
        f.write( str(CarID) + ", ")
        f.write(UniqueURL + ", ")
        f.write(CarName + ", ")
        f.write(CarPrice + ", ")
        f.write(CarMileage + ", ")
        f.write(BuildMonth + ", ")
        f.write(BuildYear + ", ")
        f.write(Power + ", ")
        f.write(Usage + ", ")
        f.write(Transmission + ", ")
        f.write(Fuel + "\n")

        CarID = CarID +1

    pagenumber = pagenumber + 1
    time.sleep(0.2)





    





