from moleculemovies import * 

class RnaLoopingMovie(Environment):
    def __init__(self):
        super(RnaLoopingMovie, self).__init__()
        self.frameFileName="looping"
        self.engine="neato"

    def saveFrame(self):        
        self.to_dot2(self.nextImageName(),sizeOverride="7.5,10.5!",engine=self.engine)
    

    def single_strand_rna_animation(self,sequence,repeatFinalFrameTimes=0,autoBasePair=True):
    
        seq = []
    
        rna= RNA()

        #todo what is the minimum size of a loop needed for where it can loop around to itself 
        rna.sequence = sequence

        #pattern_to_match=
        for base in sequence:
            n = Molecule(base)
            self.molecules.append(n)
            seq.append(n)
    
        for i in range(0,len(seq)-1):
            IntermolecularBond(seq[i],seq[i+1])

        self.saveFrame()
        

        foundMatch = False
    
        if not autoBasePair:
            return
            
        earliest_possible_start_index = 0 
        for size_of_block in range(12,2,-1):
            start_index = earliest_possible_start_index
            while start_index < (len(sequence)- size_of_block):
                searchSequence = sequence[start_index:(start_index+size_of_block)]
                complementOfSearchSequence = RNA.complementary_string(searchSequence)
                reverseComplement = complementOfSearchSequence[::-1]
                
                spacer = 4 #todo how big should this be, biologically?  need room for a hairpin
                        
                found = sequence.find(reverseComplement, start_index+size_of_block+spacer)
            
                if size_of_block==12:
                    print("it was 12")
                    print(searchSequence + " now looking for " + reverseComplement)
                    print(found)
    #                found = reverse.find(complementOfSearchSequence)
                if found>-1:
                    print("found match " + searchSequence + " with startindex " + str(start_index) + " and size " + str(size_of_block) + " matches at " + str(found))
                
                    print("prove it, is  " + searchSequence + " complementary to " + sequence[found:(found+size_of_block)])
                
                    earliest_possible_start_index = found + size_of_block
                
                    foundMatch = True
                    for i in range(start_index,(start_index + size_of_block)):
                        second_index = found + (i-start_index)
                        print(seq[i].name)
                        print(seq[second_index].name)
                        print("The two indices being joined are " + str(i) + " and " + str(second_index))
                        IntermolecularBond(seq[i],seq[second_index])
                        self.saveFrame()
                    start_index = earliest_possible_start_index #todo does this work to skip ahead in the python loop?    
                    #break
                else:
                    start_index += 1
                
        self.delay(repeatFinalFrameTimes)
                        
#    size_of_block =5
 #   start_index = 0
   
    #todo find out does it have to be backwards for RNA loops? probably not, why would it, if such twisting is possible. maybe its highly unfavorable though. 
    
    def forceBasePair(self,index1,index2,createFrame=True):
        IntermolecularBond(self.molecules[index1],self.molecules[index2])
        if createFrame:
            self.saveFrame()
        
    def generateFigure58Manual(self):
        figure5_8a="GGGUGGGACCCCUUUCGGGGUCCUGCUCAACUUCCUGUCGAGCUAAUGCCAUUUUUAAUGUCUUUAGCGAGACGCUACCAUGGCUAUCGCUGUAGGUAGCCGGAAUUCCAUUCCUAGGAGGUUUGACCUGUG"
        
#        figure5_8b="GGGUGGGACCCCUUUCGGGGUCCUGCUCAACUUCCUGUCGAGCUAAAAAAAAAAAAAAAAAAAAAGGAGGUUUGACCUGUG"
        
        
        self.single_strand_rna_animation(figure5_8a,repeatFinalFrameTimes=3,autoBasePair=False)
        
        
        self.forceBasePair(1,28)
        self.forceBasePair(3,26)
        self.forceBasePair(6,23)
        self.forceBasePair(7,22)
        self.forceBasePair(8,21)
        self.forceBasePair(9,20)
        self.forceBasePair(10,19)
        self.forceBasePair(11,18)
        self.forceBasePair(12,17) 
        for i in range(0,8):
            if i!=3:
                self.forceBasePair(29+i,123-i)                       
        for i in range(0,3):
                self.forceBasePair(37+i,72-i)                 
        for i in range(0,5):
                self.forceBasePair(42+i,68-i)                 
        for i in range(0,4):
                self.forceBasePair(50+i,60-i)                 
        for i in range(0,6):
                self.forceBasePair(74+i,100-i)
        for i in range(0,5):
            if i!=1 and i!=2:
                self.forceBasePair(80+i,93-i)                                                        
        for i in range(0,5):
            if i!=1 and i!=2:
                self.forceBasePair(102+i,114-i)                                        
                

#        self.forceBasePair(29,123)
##        self.forceBasePair(30,122)
  #      self.forceBasePair(30,122)         
        
        
        #hmmm a lot of G-U pseudo bonds in the figure, how should we handlee them? 
        #self.molecules = []
#        self.single_strand_rna_animation(figure5_8b,repeatFinalFrameTimes=3)
        createAudioFile("output/looping","These are RNA sequences from figure 5.8 in the textbook Fundamentals of Molecular Virology. Base Pairing is hard coded to match the figure.")
        saveMovie(self.frameFileName,"loopingFigure58manual",audioFile="output/looping.aiff",frameRate="3")
        
    def generateFigure58(self):
        figure5_8a="GGGUGGGACCCCUUUCGGGGUCCUGCUCAACUUCCUGUCGAGCUAAUGCCAUUUUUAAUGUCUUUAGCGAGACGCUACCAUGGCUAUCGCUGUAGGUAGCCGGAAUUCCAUUCCUAGGAGGUUUGACCUGUG"
        
        figure5_8b="GGGUGGGACCCCUUUCGGGGUCCUGCUCAACUUCCUGUCGAGCUAAAAAAAAAAAAAAAAAAAAAGGAGGUUUGACCUGUG"
        
        self.single_strand_rna_animation(figure5_8a,repeatFinalFrameTimes=3)
        #hmmm a lot of G-U pseudo bonds in the figure, how should we handlee them? 
        #self.molecules = []
        self.single_strand_rna_animation(figure5_8b,repeatFinalFrameTimes=3)
        createAudioFile("output/looping","These are RNA sequences from figure 5.8 in the textbook Fundamentals of Molecular Virology. Be aware that the base pairing shown here is by a simple algorithm, not by natural findings.")
        saveMovie(self.frameFileName,"loopingFigure58",audioFile="output/looping.aiff",frameRate="3")
        
    def generateMovieFromSequence(self,sequence,audioText,fileName):
        
        self.single_strand_rna_animation(sequence,repeatFinalFrameTimes=5)
        createAudioFile("output/looping",audioText)
        saveMovie(self.frameFileName,fileName,audioFile="output/looping.aiff",frameRate="3")
            
    def generate(self):   
        
        self.single_strand_rna_animation("GGCUAAAAAGCGCAUUUU",repeatFinalFrameTimes=5)
        
        self.single_strand_rna_animation("GGCACAAUUGCAGUCUAAUUUGCAAUAGCUCUAUCUGU",repeatFinalFrameTimes=5)
        
        self.single_strand_rna_animation("GGAAAAAGGGGUUUUUGGGCUUCCGGGAAGGUUGGGAAAGGGUUU",repeatFinalFrameTimes=5)
        
        createAudioFile("output/looping","In these RNA Looping examples, each single strand of RNA forms base pairs with itself.")
        saveMovie(self.frameFileName,"looping",audioFile="output/looping.aiff",frameRate="3")

movie = RnaLoopingMovie()
movie.generate()
#movie.generateFigure58()
#movie.generateFigure58Manual()
#movie.generateMovieFromSequence()

#mfold

#you can form U-G base pairs , n

#ncbi at nih nucleotides 

#cucumosiais virus.  

Documentar- Our Secret Universe The HIdden LIfe of the Cel....