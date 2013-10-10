class Player(object):
    def __init__(self, id, isDead, lat, lng, userID, isWerewolf):
        self.id = id
        self.isDead = isDead
        self.lat = lat
        self.lng = lng
        self.userID = userID
        self.isWerewolf = isWerewolf
    
    def getID():
        return id
    
    def setID(id):
        self.id = id
    
    def isDead():
        return isDead
        
    def setDead(isDead):
        self.isDead = isDead
        
    def getLng():
        return lng
        
    def getLat():
        return lat
        
    def setLng(lng):
        self.lng = lng
        
    def setLat():
        self.lat = lat
        
    def getUserID():
        return userID
        
    def setUserID(userID):
        self.userID = userID
        
    def isWerewolf():
        return isWerewolf
        
    def setWerewolf(isWerewolf):
        self.isWerewolf = isWerewolf

class Game(object):
    def __init__(self, dayNight, dateCreated):
        self.dayNight = dayNight
        self.dateCreated = dateCreated
    
    def getDayNight():
        return dayNight
        
    def setDayNight(dayNight):
        self.dayNight = dayNight
        
    def getDateCreated():
        return dateCreated
        
    def setDateCreated(dateCreated):
        self.dateCreated = dateCreated
        
class User(object):
    def __init__(self, id, firstName, lastName, userName, hashedPassword):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.userName = userName
        self.hashedPassword = hashedPassword
        
    def getID():
        return id
        
    def setID(id):
        self.id = id
        
    def getFirstName():
        return firstName
        
    def getLastName():
        return lastName
        
    def setFirstName(firstName):
        self.firstName = firstName
        
    def setLastName(lastName):
        self.lastName = lastName
        
    def getUserName():
        return userName
        
    def setUserName(userName):
        self.userName = userName
        
    def getHashedPassword():
        return hashedPassword
        
    def setHashedPassword():
        self.hashedPassword = hashedPassword
        
class Kill (object):
    def __init__(self, killerID, victimID, timestamp, lat, lng):
        self.killerID = killerID
        self.victimID = victimID
        self.timestamp = timestamp
        self.lat = lat
        self.lng = lng
        
    def getKillerID():
        return killerID
        
    def setKillerID(killerID):
        self.killerID = killerID
        
    def getVictimID():
        return victimID
        
    def setVictimID(victimID):
        self.victimID = victimID
        
    def getTimestamp():
        return timestamp
        
    def setTimestamp(timestamp):
        self.timestamp = timestamp
        
    def getLat():
        return lat
        
    def getLng():
        return lng
        
    def setLat(lat):
        self.lat = lat
        
    def setLng(lng):
        self.lng = lng
    
    
    
    