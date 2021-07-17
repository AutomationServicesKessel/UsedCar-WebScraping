from os import write
from requests import get
from bs4 import BeautifulSoup
import time, datetime
import csv

#Generate CSV heading
fieldnames=["Timestamp","Page Number", "CarID", "UniqueURL", "CarName", "CarPrice", "CarMileage", "BuildMonth", "BuildYear", "Power", "Usage", "Transmission", "Fuel"]
#Initiate array of UID
UID = []

#Prepare Output file
with open("CarData.csv", "r+", newline="") as csvoutput:
        read_prepare = csv.reader(csvoutput,delimiter=",")

        #Read contents into array
        rows = []
        for row in read_prepare:
                rows.append(row)

        #If the array is empty, the file has not been used before, write heading to file.                
        if not rows:
                write_prepare = csv.writer(csvoutput, delimiter=",")
                write_prepare.writerow(fieldnames)
        #If the file has been used before, get Unique ID (URL) of each entry to avoid double entries.
        else:
                for i in rows:
                        #print(i)
                        UID.append(i[3])
#print(UID)
        



#Start with page 1 and scroll through 20 pages.
pagenumber = 1                  
for i in range(20):             

# Convert page number to string, to build URL
    pagenumber_string = str(pagenumber)
# Read Web URL as starting point
    response = get('https://www.autoscout24.be/nl/lst/?sort=age&desc=1&ustate=N%2CU&size=20&page=' + pagenumber_string + '&cy=B&atype=C&')

#Parse page with BS
    html_soup = BeautifulSoup(response.text, 'html.parser')

# Get array of all cars listed on page, based on html class.
    cars = html_soup.find_all('div', class_="cldt-summary-full-item-main")



# Reset CARID to 0 for each new page
    CarID = 0
# Loop over all cars on the page
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



        #Write to CSV
        with open("CarData.csv", "a+",  newline="") as csvfile:
                
                writer = csv.DictWriter(csvfile,fieldnames=fieldnames)

                if UniqueURL not in UID:

                        #print(UniqueURL)
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

                        writer.writerow({
                        "Timestamp": datetime.datetime.now(),
                        "Page Number": pagenumber_string,
                        "CarID": str(CarID),
                        "UniqueURL": UniqueURL, 
                        "CarName": CarName,
                        "CarPrice":CarPrice,
                        "CarMileage": CarMileage,
                        "BuildMonth": BuildMonth,
                        "BuildYear": BuildYear,
                        "Power":Power,
                        "Usage":Usage,
                        "Transmission":Transmission,
                        "Fuel":Fuel
                        })


                CarID = CarID +1

    pagenumber = pagenumber + 1
    time.sleep(0.2)





    





