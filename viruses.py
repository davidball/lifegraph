from moleculemovies import * 


def doPolymovirus():
    
    
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
    

def dovirus():
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
    
    
doPolymovirus()    