from Blockporn.scripts import Scripted
#====================================================================

class Blocker:
    def __init__(self, addlink=None):
        self.cusom = addlink
        self.block = self.readblock()

#====================================================================

    def blocker(self, incoming):
        cleaned = self.cleanlink(incoming)
        for blockers in self.block:
            if cleaned.startswith(blockers):
                return True
        else:
            return False

#====================================================================
    
    async def blocked(self, incoming):
        cleaned = self.cleanlink(incoming)
        for blockers in self.block:
            if cleaned.startswith(blockers):
                return True
        else:
            return False

#====================================================================
    
    def readblock(self):
        with open('RECORDED/blocked.txt', 'r') as filed:
            listed = filed.read().splitlines()
            listed.extend(self.cusom) if self.cusom else listed
            return listed

#====================================================================
    
    def cleanlink(self, incoming):
        if incoming.startswith(Scripted.DATA01):
             finals = incoming.replace(Scripted.DATA01, "", 1)
             return finals
        elif incoming.startswith(Scripted.DATA02):
             finals = incoming.replace(Scripted.DATA02, "", 1)
             return finals
        else:
             return incoming
        
#====================================================================
