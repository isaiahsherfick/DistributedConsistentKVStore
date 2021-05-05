class message():
    def __init__(self, cmd, payload, sender, receiver, clock):
        self.cmd = cmd
        self.payload = payload
        self.sender_id = sender
        self.receiver_id = receiver
        self.clock = clock

    def getCmd(self):
        return self.cmd
    def getPayload(self):
        return self.payload

    def getSender(self):
        return self.sender_id

    def getReceiver(self):
        return self.receiver_id

    def getClock(self):
        return self.clock

    def getClockValue(self):
        return self.clock.getClockValue()

    def incrementClock(self):
        self.clock.incrementClock()

    def updateClockValue(self,newval):
        self.clock.updateClockValue(newval)

    def updateClockAt(self,id,newval):
        self.clock.updateClockValForID(id,newval)

    def adjustClocks(self,otherClock):
        self.clock.adjustClocks(otherClock)

    def __str__(self):
        r = 'MESSAGE:'
        r+=str(self.cmd)+":"
        r+=str(self.payload)+":"
        r+=str(self.sender_id)+":"
        r+=str(self.receiver_id)+":"
        r+=str(self.clock)
        return r

    def __lt__(self, other):
        return self.getClockValue() > other.getClockValue()

    def __gt__(self, other):
        return self.getClockValue() < other.getClockValue()
