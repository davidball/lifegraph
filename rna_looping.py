from moleculemovies import * 


def build_sequence():
    
    world = Environment()

    picPrefix ="looping"
    
    imageIndex=0
    imageSize = "7.5,10.5!"
    seq = []
    
    rna= RNA()
    
#    sequence="GGCACAAUUGCAGUCUAAUUUGCAAUAGCUCUAUCUGU"
 
    sequence="GGCUAAAAAGCGCAUUUU"
    sequence = "GGAAAAAGGGGUUUUUGGGCUUCCGGGAAGGUUGGGAAAGGGUUU"
    reverse=sequence[::-1]

    #todo what is the minimum size of a loop needed for where it can loop around to itself 
    rna.sequence = sequence
    complementaryRna = rna.create_complementary()
    
    
    complementary_seq = complementaryRna.sequence
        
        

    #pattern_to_match=
    for base in sequence:
        n = Molecule(base)
        world.molecules.append(n)
        seq.append(n)
    
    for i in range(0,len(seq)-1):
        IntermolecularBond(seq[i],seq[i+1])

    world.to_dot2(imageName(picPrefix,imageIndex),sizeOverride=imageSize)
    imageIndex+=1
    
    #IntermolecularBond(seq[0],seq[10])
    #world.to_dot2(imageName(picPrefix,imageIndex),sizeOverride=imageSize)
    #imageIndex+=1
    
 #   IntermolecularBond(seq[1],seq[9])
    
  #  world.to_dot2(imageName(picPrefix,imageIndex),sizeOverride=imageSize)
   # imageIndex+=1
    
#    IntermolecularBond(seq[2],seq[8])
    
    
    
    foundMatch = False
    
    
    earliest_possible_start_index = 0 
    for size_of_block in range(5,2,-1):
        #if foundMatch:
        #    break
        start_index = earliest_possible_start_index
        while start_index < (len(sequence)- size_of_block):
            searchSequence = sequence[start_index:(start_index+size_of_block)]
            complementOfSearchSequence = RNA.complementary_string(searchSequence)
            reverseComplement = complementOfSearchSequence[::-1]
            
            spacer = 4 #todo how big should this be, biologically?  need room for a hairpin
            
            
            found = sequence.find(reverseComplement, start_index+size_of_block+spacer)
            
#                found = reverse.find(complementOfSearchSequence)
            if found>-1:
                print("found match " + searchSequence + " with startindex " + str(start_index) + " and size " + str(size_of_block) + " matches at " + str(found))
                
                print("reverse seq is " + reverse)
                print("prove it, is  " + searchSequence + " complementary to " + sequence[found:(found+size_of_block)])
                
                earliest_possible_start_index = found + size_of_block
                
                foundMatch = True
                for i in range(start_index,(start_index + size_of_block)):
                    second_index = found + (i-start_index)
                    print(seq[i].name)
                    print(seq[second_index].name)
                    print("The two indices being joined are " + str(i) + " and " + str(second_index))
                    IntermolecularBond(seq[i],seq[second_index])
                    world.to_dot2(imageName(picPrefix,imageIndex),sizeOverride=imageSize)
                    imageIndex+=1
                start_index = earliest_possible_start_index #todo does this work to skip ahead in the python loop?    
                #break
            else:
#                print("found no match")
                start_index += 1
                
        
#    size_of_block =5
 #   start_index = 0
   
    #todo find out does it have to be backwards for RNA loops? probably not, why would it, if such twisting is possible. maybe its highly unfavorable though. 
    
    
    
   # print("looking for where " + searchSequence + " can bind to " + complementOfSearchSequence)
    
    
    
    
    createAudioFile("output/looping","RNA Looping example")
    saveMovie(picPrefix,"looping",audioFile="output/looping.aiff",frameRate="1")


build_sequence()