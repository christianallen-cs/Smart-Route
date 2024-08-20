# SOURCE CITED: C950-Webinar-2 Getting Greedy, who moved my data
import datetime


class Package:
    def __init__(self, packageID, address, city, state, zipcode, deadline, weight, truck_number, status):
        self.packageID = packageID
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = deadline
        self.weight = weight
        self.status = status
        self.truck_number = truck_number
        self.delivery = None
        self.departure = None

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s lbs, %s" % (
            self.packageID, self.address, self.city, self.state,
            self.zipcode, self.deadline, self.weight, self.status)

    def status_updates(self, expected):
        if self.delivery is not None and self.delivery < expected:
            self.status = f"Delivered At {self.delivery} by Truck {self.truck_number}"
        elif self.departure is not None and self.departure > expected:
            self.status = f"En Route on Truck {self.truck_number}"
        else:
            self.status = f"At Hub loaded on Truck {self.truck_number}"

        if self.packageID == 9 and expected >= datetime.timedelta(hours=10, minutes=20):
            self.address = "410 S State St"
            self.city = "Salt Lake City"
            self.state = "UT"
            self.zipcode = "84111"
