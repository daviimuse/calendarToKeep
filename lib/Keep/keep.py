import gkeepapi


def var_dump(obj):
    '''return a printable representation of an object for debugging'''
    newobj=obj
    if '__dict__' in dir(obj):
        newobj=obj.__dict__
    if ' object at ' in str(obj) and not newobj.has_key('__type__'):
        newobj['__type__']=str(obj)
    for attr in newobj:
        newobj[attr]=var_dump(newobj[attr])
    return newobj

class Keep():
    def __init__(self, email, password):
        self.keep = gkeepapi.Keep()
        self.success = self.keep.login(email,password)
    
    def getAllNotes(self):
        return self.keep.find(trashed=False, archived=False)
       
    def pushToKeep(self,data:dict):
        try:
            note = self.keep.createNote(data["Title"],data["Text"])
            note.pinned = True
            note.archived = False
            self.keep.sync()
            return True
        except :
            return False 
    
         
if __name__ == "__main__":         
    calendar = Keep('noreply.64189489@gmail.com','qkerthvmellvdlwm')
    notes = calendar.getAllNotes()
    
    # print(notes)

    for note in notes:
        print(note.text)
    # data = {
    #     "Title": "test",
    #     "Text": "test_text"
    # }
    # print(calendar.pushToKeep(data))



# Blue = 'BLUE'
# Blue

# Brown = 'BROWN'
# Brown

# DarkBlue = 'CERULEAN'
# Dark blue

# Gray = 'GRAY'
# Gray

# Green = 'GREEN'
# Green

# Orange = 'ORANGE'
# Orange

# Pink = 'PINK'
# Pink

# Purple = 'PURPLE'
# Purple

# Red = 'RED'
# Red

# Teal = 'TEAL'
# Teal

# White = 'DEFAULT'
# White

# Yellow = 'YELLOW'
# Yellow
