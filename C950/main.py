# Christian Allen
# Student ID: 011234151

import csv
import datetime
import truck

from hashtable import HashTable
from package import Package

# SOURCE CITED: pythonprogramming.net/reading-csv-files-python-3/
# Reads and prints specified csv file
with open('WGUPSAddressFile.csv') as csvfile1:
    readCSV1 = csv.reader(csvfile1)
    readCSV1 = list(readCSV1)

# SOURCE CITED: pythonprogramming.net/reading-csv-files-python-3/
# Reads and prints specified csv file
with open('WGUPSPackageFile.csv') as csvfile2:
    readCSV2 = csv.reader(csvfile2)
    readCSV2 = list(readCSV2)

# SOURCE CITED: pythonprogramming.net/reading-csv-files-python-3/
# Reads and prints specified csv file
with open('WGUPSDistanceFile.csv') as csvfile3:
    readCSV3 = csv.reader(csvfile3)
    readCSV3 = list(readCSV3)


# SOURCE CITED: C950-Webinar-3 How to Dijkstra
def loadData(fileName, package_hash):
    with open(fileName) as package_details:
        package_data = csv.reader(package_details)
        for packages in package_data:
            pID = int(packages[0])
            pAddress = packages[1]
            pCity = packages[2]
            pState = packages[3]
            pZip = packages[4]
            pDeadline = packages[5]
            pWeight = packages[6]
            pTruckNum = packages[7]
            pStatus = "At The Hub"

            # Package object
            p = Package(pID, pAddress, pCity, pState, pZip, pDeadline, pWeight, pTruckNum, pStatus)

            # Inserts package object into hash table
            package_hash.insert(pID, p)


# Returns the float value distance between two addresses
def distanceBetween(plot1, plot2):
    distance = readCSV3[plot1][plot2]
    if distance == '':
        distance = readCSV3[plot2][plot1]
    return float(distance)


# Returns the address number
def addressGetter(address):
    for row in readCSV1:
        if address == row[2]:
            return int(row[0])


# Creating all three truck objects
truck1 = truck.Truck(16, 18, None, [1, 4, 40, 29, 7, 13, 39, 14, 15, 19, 16, 34, 20, 21], 0, "4001 South 700 East",
                     datetime.timedelta(hours=8, minutes=0))

truck2 = truck.Truck(16, 18, None, [3, 5, 37, 38, 6, 18, 23, 24, 25, 26, 28, 31, 32, 36], 0, "4001 South 700 East",
                     datetime.timedelta(hours=9, minutes=5))

truck3 = truck.Truck(16, 18, None, [2, 33, 8, 9, 30, 10, 11, 12, 17, 22, 27, 35], 0, "4001 South 700 East",
                     datetime.timedelta(hours=10, minutes=20))


# Initializing the hash table, and loading the packages from the CSV
hashTable = HashTable()
loadData("WGUPSPackageFile.csv", hashTable)


# SOURCE CITED: Instructions.docx sent from course instructor Robert Ferdinand
# Implementation of nearest neighbor algorithm
def algo(truck, truck_number):
    undelivered = []
    for packageID in truck.packages:
        package = hashTable.search(packageID)
        undelivered.append(package)
    truck.packages.clear()

    while len(undelivered) > 0:  # Iterates through all packages until none remain
        minDistance = float('inf')  # Miles
        closestPackage = None  # No package

        truck_address = addressGetter(truck.address)
        for package in undelivered:
            package_address = addressGetter(package.address)
            distance = distanceBetween(truck_address, package_address)
            if distance <= minDistance:
                minDistance = distance
                closestPackage = package

        if closestPackage:
            closestPackage.truck_number = truck_number  # Adds truck number to packages
            truck.packages.append(closestPackage.packageID)  # Adds closest package to trucks list
            undelivered.remove(closestPackage)  # Removes package from undelivered list
            truck.mileage += minDistance  # Tracks mileage
            truck.address = closestPackage.address  # Updates current truck address
            truck.currentTime += datetime.timedelta(hours=minDistance / truck.speed)  # Updates travel times
            closestPackage.delivery = truck.currentTime
            closestPackage.depart = truck.depart


# Loading the trucks
algo(truck1, 1)
algo(truck2, 2)

# Prevents truck 3 from shipping until either of the first 2 are done
truck3.depart = min(truck1.currentTime, truck2.currentTime)
algo(truck3, 3)


# User interface
class Main:
    totalMileage = truck1.mileage + truck2.mileage + truck3.mileage
    print(f"Total mileage: {totalMileage}")

    statusCheck = input("If you want to check the status of your package, type 'start'. - ")
    if statusCheck == 'start':
        time = input("Enter a time using Hour:Minute. - ")
        (H, M) = time.split(':')
        timeConv = datetime.timedelta(hours=int(H), minutes=int(M))
        obj = input("Specify weather you want to see a 'specific' package, or 'all' packages. - ")
        if obj == 'specific':
            while True:  # Allows user to re-enter ID instead of restarting entire program
                inputID = input("Enter package ID number. - ")
                packageLookup = hashTable.search(int(inputID))
                if packageLookup is not None:
                    packageLookup.status_updates(timeConv)  # Returns status based on time and package specifics
                    print(str(packageLookup))
                    break
                else:
                    print("Invalid ID number, please try again.")
        elif obj == 'all':
            for packageID in range(1, 41):  # Returns all packages since id's range from 0 to 40
                packageLookup = hashTable.search(packageID)
                packageLookup.status_updates(timeConv)  # Returns all packages statues
                print(str(packageLookup))  # Prints all package status
        else:
            print("Invalid answer, goodbye.")
            exit()
    else:
        print("Invalid response, please type 'start'.")
        exit()  # End of program
