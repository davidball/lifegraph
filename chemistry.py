import collections
import re
import math
from graphviz import Graph
from graphviz import Digraph
import os
#Note: Run in Python 3

#pip install graphviz

#basic program to implement organic chemistry
class Atom:
    
    atomic_numbers = {"H":1,"He":2,"Li":3,"Be":4,"B":5,"C":6,"N":7,"O":8,"F":9,"Ne":10}
    electro_negativities = {"H":2.20,"C":2.55,"O":3.44,"Cl":3.16}    
    def __init__(self,symbol):
        self.symbol=symbol
        self.bonds=[]
        self.atomic_number = Atom.atomic_numbers.get(symbol,0)
        self.init_lone_electrons_from_atomic_number()
        self.electronegativity = Atom.electro_negativities.get(symbol,0)
    
    def init_lone_electrons_from_atomic_number(self):
        if self.atomic_number>2:
            self.lone_electrons = self.atomic_number - 2
        else:
            self.lone_electrons = self.atomic_number

    @property
    def formal_charge(self):
        c = self.atomic_number - self.lone_electrons
        if self.atomic_number>2:
            c-=2
        
        for bond in self.bonds:
            c-= bond.number
        return c         

    def show(self,details=True):
        print(self.symbol + " with " + str(len(self.bonds)) + " bonds")
        output_string = ""
        for bond in self.bonds:

            output_string += "\t"
            if bond.atom1==self:
                output_string += bond.atom2.symbol
            else:
                output_string += bond.atom1.symbol
                

            output_string+= " (" + bond.strength_name + ")" 
            if bond.is_polar:
                output_string += " (polar bond) "
            output_string+="\n"
        
        if details:
            output_string+= "\n Formal Charge: " + str(self.formal_charge)
            
        print(output_string)

        
    @property
    def lone_electrons(self):
        return self._lone_electrons    
    
    @lone_electrons.setter
    def lone_electrons(self,value):
        if value>=0:
            self._lone_electrons = value
        else:
            print("Warning! attempt to over debit electrons")
            self._lone_electrons = 0

class Bond:
    
    strength_names = {
        1: "single",
        2: "double",
        3: "triple"
    }
    
    def __init__(self,atom1,atom2,number=1):
        self.atom1 = atom1
        self.atom2 = atom2
        self.number = number
        for atom in [atom1,atom2]:
            atom.bonds.append(self)
            atom.lone_electrons -= number
        
    @property
    def strength_name(self):
        return Bond.strength_names[self.number]
    
    @property
    def is_polar(self):
        return abs(self.atom1.electronegativity - self.atom2.electronegativity) > 0.5
 
class IntermolecularBond:
    
    bond_type = {
        1: "hydrogen",
        2: "covalent"
    }
    
    def __init__(self,molecule1,molecule2):
        self.molecule1 = molecule1
        self.molecule2 = molecule2
 
        for molecule in [molecule1,molecule2]:
            molecule.intermolecularbonds.append(self)
    
    def remove(self):
        for molecule in [self.molecule1,self.molecule2]:
            molecule.intermolecularbonds.remove(self)
                        
class Molecule:
    def __init__(self,name,display_name=""):
        self.atoms = []
        self.intermolecularbonds = []
        self.parts = []
        self._display_name = display_name or name
            
        self.name=name
        for symbol in name:
            a = Atom(symbol)
            self.atoms.append(a)
    
    def show(self):
        print("Name:" + self.find_name)
        print("Structure:")
        for atom in self.atoms:
            atom.show()
    
    def destroy_all_bonds(self):
        for bond in self.intermolecularbonds[:]:
            bond.molecule1.intermolecularbonds.remove(bond)
            bond.molecule2.intermolecularbonds.remove(bond)
            
    @property
    def find_name(self):
        elements = collections.OrderedDict()
        for atom in self.atoms:
            s = atom.symbol
            if s in elements:
                elements[s] += 1
            else:
                elements[s] = 1
        word = ""
        for k in elements:
            word += k
            
            n = elements[k]
            if n > 1:
                word += str(n)
        return word

    @property
    def display_name(self):
        return self._display_name

    @display_name.setter
    def display_name(self,value):
        self._display_name=value
    
    def to_dot(self):
        content = ""
        
        idx = 0 
        
        dot_names = {}
        for atom in self.atoms:
            idx+=1
            dot_name = atom.symbol + str(idx)
            label_name = dot_name if atom.symbol=="C" else atom.symbol
            content += dot_name + " [label=" + label_name + "];\n"
            dot_names[atom] = dot_name
        
        bonds = {}
        for atom in self.atoms:
            for bond in atom.bonds:
                if not bond in bonds:
                    content += dot_names[bond.atom1] + " -- " + dot_names[bond.atom2]
                    
                    if bond.number == 2:
                         content += "[color=\"black:white:black\"]"
                    elif bond.number == 3:
                         content += "[color=\"black:white:black:white:black\"]"
                    content += ";\n"
                    bonds[bond]=True

        return "graph G {\n" + content + "\n}"
            
class CarbonDioxide(Molecule):
    def __init__(self):
        super(CarbonDioxide, self).__init__("COO")
        Bond(self.atoms[0],self.atoms[1],2)
        Bond(self.atoms[0],self.atoms[2],2)
        
class Water(Molecule):
    def __init__(self):
        super(Water, self).__init__("HHO")
        Bond(self.atoms[0],self.atoms[2],1)
        Bond(self.atoms[1],self.atoms[2],1)
        
        
class Ethane(Molecule):
    def __init__(self):
        super(Ethane, self).__init__("CHHHCHHH")
        for carbon in [0,4]:
            for h in [carbon+1,carbon+2,carbon+3]:
                Bond(self.atoms[carbon],self.atoms[h],1)        
        Bond(self.atoms[0],self.atoms[4])
    
class Glucose(Molecule):
    def __init__(self):
        super(Glucose, self).__init__("CCCCCCHHHHHHHHHHHHOOOOOO")
        for carbon in range(0,5):
            Bond(self.atoms[carbon],self.atoms[carbon+1])
        

        carbons = self.atoms[0:6]
        oxygens = self.atoms[-6:]
        hydrogens = self.atoms[6:18]
        o_in_ring = oxygens.pop()
    
        Bond(carbons[0],o_in_ring)
        Bond(carbons[4],o_in_ring)
    
        for carbon in range(0,6):
            if carbon != 4:
                self.add_oh(carbons[carbon],oxygens.pop(),hydrogens.pop())
        
        #now add all the remaining hydrogens to their carbons
        cidx = 0
        for carbon in carbons:
            while len(carbon.bonds)<4:
                Bond(carbon,hydrogens.pop())
            cidx+=1
                
    def add_oh(self,carbon,oxygen,hydrogen):
        Bond(carbon,oxygen)
        Bond(oxygen,hydrogen)



class DNA(Molecule):
    baseValidator = re.compile(r"[^ATGC]")
    def __init__(self):
        super(DNA, self).__init__("")
        print("new DNA")

    @property
    def sequence(self):
        return self._sequence

    @sequence.setter                       
    def sequence(self,value):
        if DNA.baseValidator.search(value):
            print("Error DNA sequence contains invalid bases")
        else:
            self._sequence=value

    #return index of base if the provided strand is complementary to this strand. 
    def does_base_pair(self,other_DNA):
        print("I don't know")


    def create_complementary(self):
        print("beging create compl")
        pairing_rule = {"A":"T","T":"A","G":"C","C":"G"}
        
        oldSequenceThreePrimeToFive = list(self.sequence[::-1])
        print(oldSequenceThreePrimeToFive)
        for i,base in enumerate(oldSequenceThreePrimeToFive):
            oldSequenceThreePrimeToFive[i] = pairing_rule[base]
        print(oldSequenceThreePrimeToFive)                       
        newStrand = DNA()
        newStrand.sequence = "".join(oldSequenceThreePrimeToFive)
        return newStrand

    @property
    def display_name(self,max_sequence_length=12):
 
        if len(self.sequence)>max_sequence_length:
            fragment_length = math.floor((max_sequence_length-3)/2)
            return "DNA " + self.sequence[0:(fragment_length+1)] + "..." + self.sequence[-fragment_length:]
        else:
            return "DNA " + self.sequence

class DoubleStrandDNA(Molecule):
    def __init__(self,seq):
        super(DoubleStrandDNA, self).__init__("")
        self._sequence = seq
        s1 = DNA()
        s1.sequence = seq
        s2 = s1.create_complementary()
        self._strands = [s1,s2]
        self.parts.append(s1)
        self.parts.append(s2)        
        bond = IntermolecularBond(s1,s2)
        self.display_name = "Double Stranded DNA"


    @property
    def strands(self):
        return self._strands

class RNA(Molecule):
    baseValidator = re.compile(r"[^AUGC]")
    pairing_rule = {"A":"U","U":"A","G":"C","C":"G"}
    def __init__(self):
        super(RNA, self).__init__("")

    @property
    def sequence(self):
        return self._sequence

    @sequence.setter                       
    def sequence(self,value):
        if RNA.baseValidator.search(value):
            print("Error RNA sequence contains invalid bases")
        else:
            self._sequence=value

    #return index of base if the provided strand is complementary to this strand. 
    def does_base_pair(self,other_DNA):
        print("I don't know")

    def complementary_string(seq):
        output=""
        for base in seq:
            output+=RNA.pairing_rule[base]
        return output

    def create_complementary(self):
        print("beging create compl")
        
        
        oldSequenceThreePrimeToFive = list(self.sequence[::-1])
        print(oldSequenceThreePrimeToFive)
        for i,base in enumerate(oldSequenceThreePrimeToFive):
            oldSequenceThreePrimeToFive[i] = RNA.pairing_rule[base]
        print(oldSequenceThreePrimeToFive)                       
        newStrand = RNA()
        newStrand.sequence = "".join(oldSequenceThreePrimeToFive)
        return newStrand

    @property
    def display_name(self,max_sequence_length=12):
 
        if len(self.sequence)>max_sequence_length:
            fragment_length = math.floor((max_sequence_length-3)/2)
            return "RNA " + self.sequence[0:(fragment_length+1)] + "..." + self.sequence[-fragment_length:]
        else:
            return "RNA " + self.sequence
            
            
            
class Protein(Molecule):
    
    peptideValidator = re.compile(r"[^ACDEFGHIKLMNPQRSTVWY]") #amino acid codes
    def __init__(self,name):
        super(Protein, self).__init__("",name)
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self,value):
        self._name = value
    @property
    def sequence(self):
        return self._sequence

    @sequence.setter                       
    def sequence(self,value):
        if DNA.peptideValidator.search(value):
            print("Error DNA sequence contains invalid bases")
        else:
            self._sequence=value

    

    #return index of base if the provided strand is complementary to this strand. 
    def does_base_pair(self,other_DNA):
        print("I don't know")





c = CarbonDioxide()
c.show()


w = Water()
#w.show()


e = Ethane()
#e.show()

g = Glucose()
#g.show()

#print(g.to_dot())

def createDoubleStrandedDNA(sequence):
    d1 = DNA()
    d1.sequence = sequence

    d2 = d1.create_complementary()

    IntermolecularBond(d1,d2)

    return [d1,d2]
    
    

