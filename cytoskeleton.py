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
        
class CytoskeletonMovie(Environment):
    def __init__(self):
        super(CytoskeletonMovie, self).__init__()
        self.frameFileName="cytoFrame"
        self.engine="fdp"
                
    def saveFrame(self):        
        self.to_dot2(self.nextImageName(),sizeOverride="9,5!",engine=self.engine)

    def generateActins(self,n,style="invisible"):
        self.actin_count=n
        actins=[]
        for i in range(0,n):
            a = Actin()
            actins.append(a)
            a.style=style
            self.molecules.append(a)
        self.actins=actins
        
    def buildSimpleModel(self):
        self.engine="neato"
        actin_count = 10
        
        self.generateActins(actin_count,"filled")    

        self.saveFrame()

        t= Tropomysin()
    
        self.molecules.append(t)
    
        self.saveFrame()
        
        for i in range(0,actin_count-1):
            bond = IntermolecularBond(self.actins[i],self.actins[i+1])
            self.saveFrame()
            
        for i in range(2, 9):
            bond = IntermolecularBond(t,self.actins[i])
            self.saveFrame()
    
#        self.delay(5)

        t.destroy_all_bonds()
    
        self.molecules.remove(t)

        c = Coflin()
        self.molecules.append(c)

        self.saveFrame()

        for i in range(2, 9):
            bond = IntermolecularBond(c,self.actins[i])
            self.saveFrame()
    
            
        for i in range(2, actin_count):
            a=self.actins[i]
            a.destroy_all_bonds()
            self.saveFrame()

        self.saveFrame()
    
        self.createAudio()
                
    def buildModelOfCytoskeleton(self):
        self.engine="fdp"
        actin_count = 16
        
        self.generateActins(actin_count)    

        thymosins = []
        thymosin_count = 1
    
        for i in range(0,thymosin_count):        
            thymosin = Molecule("Thymosin")
            thymosins.append(thymosin)
            self.actins[i].style="filled"
    #        self.molecules.append(self.actins[i])
            self.molecules.append(thymosin)
            bond = IntermolecularBond(self.actins[i],thymosin)
            if i % 2 ==1:  #just make a slide of every other one
                self.saveFrame()
    
        profilins = []
        profilin_count = 5
    
        profilin_bonds = []
        for i in range(0,profilin_count):        
            profilin = Molecule("Profilin")
            profilins.append(profilin)
            self.molecules.append(profilin)
            self.actins[i].style="filled"
    #        self.molecules.append(self.actins[i+thymosin_count])
            bond = IntermolecularBond(self.actins[i+thymosin_count],profilin)
            profilin_bonds.append(bond)
            if i % 2 ==1:  #just make a slide of every other one
                self.saveFrame()
    
        first_profilin_bound_actin_index = thymosin_count
    
        arp = Molecule("ARP 2 3 complex")
    
        arp2 = Molecule("Arp2")
        arp3 = Molecule("Arp3")
        arp.parts.append(arp2)
        arp.parts.append(arp3)
        IntermolecularBond(arp2,arp3)
        self.molecules.append(arp)
    
    
        self.saveFrame()

        bond = IntermolecularBond(arp2,self.actins[first_profilin_bound_actin_index])
        self.saveFrame()    

        bond = IntermolecularBond(arp3,self.actins[first_profilin_bound_actin_index+1])
        self.saveFrame()        
        
        self.actins[first_profilin_bound_actin_index].style="filled"

        for i in range(first_profilin_bound_actin_index,first_profilin_bound_actin_index + profilin_count):
            bond = IntermolecularBond(self.actins[i],self.actins[i+1])
            self.saveFrame()
            profilin_bonds[i-first_profilin_bound_actin_index].remove()
            self.saveFrame()

        t= Tropomysin()
    
        self.molecules.append(t)
    
        self.saveFrame()
    
        for i in range(2, 9):
            bond = IntermolecularBond(t,self.actins[i])
            self.saveFrame()
        
        self.delay(5)
    
        t.destroy_all_bonds()
        
        self.molecules.remove(t)
    
        c = Coflin()
        self.molecules.append(c)
    
        self.saveFrame()
    
        for i in range(2, 9):
            bond = IntermolecularBond(c,self.actins[i])
            self.saveFrame()
        
        self.delay(5)
                
        for i in range(2, 9):
            a=self.actins[i]
            a.destroy_all_bonds()
            self.saveFrame()

        self.saveFrame()
    
        self.createAudio()

    def createAudio(self):
        super(CytoskeletonMovie,self).createAudioFile("output/cytoskeleton","After initial nucleation, actin monomer subunits combine to create an Actin filament. Tropomysin can bind to up to 7 actin subunits stabilizes actin filments.  Coflin binds to filaments, destabilizing them and leading to depolymerazation. Coflin favors ADP bound actin subunits and therefore dismantles older filaments.  Actin nucleation is usually started by one of two proteins: the Arp 2 3 complex, or formins.")
        
    def saveMovie(self):
        super(CytoskeletonMovie,self).saveMovie("cytoFrame","cytoskeleton",frameRate="1.8",audioFile="output/cytoskeleton.aiff")

    def generate(self):
        self.buildSimpleModel()
        #clear it out and start again
        self.molecules=[]
        self.buildModelOfCytoskeleton()
        
        self.saveMovie()

movie = CytoskeletonMovie()

#movie.generate()
movie.saveMovie()
#movie.buildModelOfCytoskeleton()

#movie.saveMovie()
#movie.saveMovie("cytoFrame","cytoskeleton",frameRate="1/3",audioFile="output/cytoskeleton.aiff")
#saveMovie("cytoFrame","cytoskeleton",frameRate="1/3",audioFile="output/cytoskeleton.aiff")
#buildModelOfCytoskeleton()