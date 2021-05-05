import os
class logical_clock():
    def __init__(self,id,initial_val=0):
        self.id = id
        self.clockMap = {id:initial_val}

    def getId(self):
        return self.id

    def getClockValue(self):
        return self.clockMap.get(self.id)

    def incrementClock(self):
        self.clockMap.update({self.id:self.clockMap.get(self.id)+1})

    def setClockValue(self,newval):
        if(newval > self.clockMap.get(self.id)):
            self.clockMap.update({self.id:newval})

    def setClockValueForID(self,id,newval):
        if (self.clockMap.get(id) == None):
            self.clockMap.update({id:newval})
        elif(newval > self.clockMap.get(id)):
            self.clockMap.update({id:newval})

    def getClockValueAtID(self,id):
        otherClock = self.clockMap.get(id)
        if otherClock != None:
            return otherClock
        else:
            print("Error!")

    def adjustClocks(self,otherClock):
        self.setClockValueForID(otherClock.getId(),otherClock.getClockValue())
        otherClock.setClockValueForID(self.id,self.getClockValue())


        if (otherClock.getClockValue() > self.getClockValue()):
            self.setClockValue(otherClock.getClockValue())

        elif (self.getClockValue() > otherClock.getClockValue()):
            otherClock.setClockValue(self.getClockValue())
        return

    def __str__(self):
        return f"CLOCK:{self.id}:{self.getClockValue()}"

    def __lt__(self, other):
        return self.getClockValue() < other.getClockValue()

    def __gt__(self,other):
        return self.getClockValue() > other.getClockValue()

if __name__ == '__main__':
    lc1 = logical_clock(4000,1)
    print(lc1.getClockValue())
    lc1.incrementClock()
    print(lc1.getClockValue())
    lc2 = logical_clock(4343,3)
    print(lc2 > lc1)
    print(lc1 < lc2)
    print(lc2 < lc1)
    print(lc1 > lc2)
