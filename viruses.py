from moleculemovies import * 


class Virus(Molecule):
    def __init__(self):
        super(Virus, self).__init__("Virus")



class Herpes(Virus):
    def __init__(self):
        super(Herpes, self).__init__("Herpes")


class Adenovirus(Virus):
    def __init__(self):
        super(Adenovirus, self).__init__("Adenovirus")
    
    def E1A(self):
        e1a = Molecule("E1A")
        p300 = Molecule("p300")
        pRB = Molecule("pRB")
        TBP = "TBP (Tata Binding Protein)"
        e2f=Molecule("E2F")
        for m in [p300,prb,TBP];
            IntermolecularBond(e1a,m)
        IntermolecularBond(pRB,e2f)
        #the early protein E1A interacts with histone deacytlase p300, cell cycel blocker pRB

    
def VirusMovie(Environment):
    def __init__(self):
        super(RnaLoopingMovie, self).__init__()
        self.frameFileName="looping"
        self.engine="neato"

    def doPolymovirus(self):
    
    
        v = Molecule("SV40")
    
        largeA = Molecule("Large T Antigen")
    
        v.parts.append(largeA)
    
        pa = Molecule("Polalpha")
        p300= Molecule("p300")
        Rb= Molecule("Rb")
        Topoisomerase1= Molecule("Topoisomerase 1")
        mTBP = Molecule("TBP")
        p53= Molecule("p53")
    
        IntermolecularBond(largeA,pa)
        IntermolecularBond(largeA,p300)
        IntermolecularBond(largeA,Rb)
        IntermolecularBond(largeA,Topoisomerase1)
        IntermolecularBond(largeA,mTBP)                
        IntermolecularBond(largeA,p53)    
    
        #parts phosphorylated regions, NLS, Zinc Binding Site

        world = Environment()
        world.molecules = world.molecules + [v,pa,p300,Rb,Topoisomerase1,mTBP,p53]
        imageIndex=0
        world.to_dot2(imageName("sv40",imageIndex),sizeOverride="9,5!",engine="fdp")
    

    def dovirus(self):
        world = Environment()
        imageIndex=0
        picPrefix = "virus"
        m = Molecule("fake")
        p1 = Molecule("FakePart")
        p2 = Molecule("FakePart2")    
        m.parts.append(p1)
        m.parts.append(p2)
    
        l = Molecule("littlepart")
        p1.parts.append(l)
        m2 = Molecule("fakefriend")
    
        world.molecules.append(m)
        world.molecules.append(m2)
    
        bond = IntermolecularBond(l,m2)
    
        for i in range(0,10):
            m=Molecule("nothing")
            world.molecules.append(m)
            bond = IntermolecularBond(m,m2)
    
        world.to_dot2(imageName(picPrefix,imageIndex),sizeOverride="9,5!",engine="fdp")
    

v = VirusMovie()

v.doPolymovirus()    