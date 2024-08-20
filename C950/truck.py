# SOURCE CITED: C950-Webinar-2 Getting Greedy, who moved my data

class Truck:
    def __init__(self, capacity, speed, load, packages, mileage, address, depart):
        self.capacity = capacity
        self.speed = speed
        self.load = load
        self.packages = packages
        self.mileage = mileage
        self.address = address
        self.depart = depart
        self.currentTime = depart

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s" % (self.capacity, self.speed, self.load, self.packages,
                                               self.mileage, self.address, self.depart)
