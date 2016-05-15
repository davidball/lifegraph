from moleculemovies import * 


class ActinPositiveEnd(Molecule):
    def __init__(self):
        super(ActinPositiveEnd, self).__init__("Actin + End")

class ActinMinusEnd(Molecule):
    def __init__(self):
        super(ActinMinusEnd, self).__init__("Actin - End")

    
class Actin(Protein):
    def __init__(self):
        super(Actin, self).__init__("Actin")
#        self.parts.append(ActinPositiveEnd())
#        self.parts.append(ActinMinusEnd())


class ActinFilament(Molecule):
    def __init__(self):
        super(ActinFilament, self).__init__("Actin")


class Coflin(Protein):
    def __init__(self):
        super(Coflin, self).__init__("Coflin")

class Tropomysin(Protein):
    #in lecture notes topic 19, not in text
    def __init__(self):
        super(Tropomysin, self).__init__("Tropomysin")
            
def buildModelOfCytoskeleton():

    actin_count = 10
    
    actins=[]
    world = Environment()

    picPrefix ="cytoFrame"

    for i in range(0,actin_count):
        a = Actin()
        actins.append(a)
        world.molecules.append(a)
        world.to_dot2(imageName(picPrefix,i),sizeOverride="9,5!")

    imageIndex = actin_count
    
    for i in range(0,actin_count-1):
        bond = IntermolecularBond(actins[i],actins[i+1])
        world.to_dot2(imageName(picPrefix,imageIndex),sizeOverride="9,5!")
        imageIndex+=1


    t= Tropomysin()
    
    world.molecules.append(t)
    
    world.to_dot2(imageName(picPrefix,imageIndex),sizeOverride="9,5!")
    imageIndex+=1

    
    
    for i in range(2, 9):
        bond = IntermolecularBond(t,actins[i])
        world.to_dot2(imageName(picPrefix,imageIndex),sizeOverride="9,5!")
        imageIndex+=1

    for delay in range(1,5):
        world.to_dot2(imageName(picPrefix,imageIndex),sizeOverride="9,5!")
        imageIndex+=1
    
    t.destroy_all_bonds()
    world.molecules.remove(t)
    
    c = Coflin()
    world.molecules.append(c)
    
    world.to_dot2(imageName(picPrefix,imageIndex),sizeOverride="9,5!")
    imageIndex+=1
    
    for i in range(2, 9):
        bond = IntermolecularBond(c,actins[i])
        world.to_dot2(imageName(picPrefix,imageIndex),sizeOverride="9,5!")
        imageIndex+=1
        
    for delay in range(1,5):
        world.to_dot2(imageName(picPrefix,imageIndex),sizeOverride="9,5!")
        imageIndex+=1
                
    for i in range(2, 9):
        a=actins[i]
        a.destroy_all_bonds()
        world.to_dot2(imageName(picPrefix,imageIndex),sizeOverride="9,5!")
        imageIndex+=1
    
    world.to_dot2(imageName(picPrefix,imageIndex),sizeOverride="9,5!")
    imageIndex+=1
    
    
    createAudioFile("output/cytoskeleton","After initial nucleation, actin monomer subunits combine to create an Actin filament. Tropomysin can bind to up to 7 actin subunits stabilizes actin filments.  Coflin binds to filaments, destabilizing them and leading to depolymerazation. Coflin favors ADP bound actin subunits and therefore dismantles older filaments.")
    saveMovie(picPrefix,"cytoskeleton",frameRate=3,audioFile="output/cytoskeleton.aiff")


buildModelOfCytoskeleton()