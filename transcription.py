from moleculemovies import * 

def buildModelOfTranscriptionInitiation():

    doubleStrand = DoubleStrandDNA("TATAGCGTAC")
    d1 = doubleStrand.strands[0]
    d2 = doubleStrand.strands[1]
    
    tfiid = Protein("TF2D")
    tfiib = Protein("TF2B")
    tfiih = Protein("TF2H")

    imagePrefix="Trans"
    transcriptionInitWorld = Environment()

    for m in [doubleStrand,tfiid,tfiib,tfiih]:
        transcriptionInitWorld.molecules.append(m)

    transcriptionInitWorld.to_dot2(imageName(imagePrefix,1),engine="fdp")
    
    bond = IntermolecularBond(d1,tfiid)
    transcriptionInitWorld.to_dot2(imageName(imagePrefix,2),engine="fdp")

    bond = IntermolecularBond(d1,tfiib)
    transcriptionInitWorld.to_dot2(imageName(imagePrefix,3),engine="fdp")

    bond = IntermolecularBond(d1,tfiih)
    transcriptionInitWorld.to_dot2(imageName(imagePrefix,4),engine="fdp")
    
    
    saveMovie(imagePrefix,"transcriptionInitiation")
    
    #os.system("ffmpeg -framerate 1/3 -i frame%03d.png -c:v mpeg4 -r 30 -pix_fmt yuv420p transcriptionInitiation.mp4")
    #os.system("ffmpeg -r 1 -i frame%03d.png -c:v mpeg4 -r 1 -pix_fmt yuv420p transcriptionInitiation.mp4")
    
    #-frame-rate 1/3 = means each image should be shown for 3 seconds
#    os.system("ffmpeg -framerate 1/3 -i frame%03d.png -c:v mpeg4 -pix_fmt yuv420p transcriptionInitiation.mp4")
    



buildModelOfTranscriptionInitiation()
