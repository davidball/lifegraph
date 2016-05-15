from chemistry import *
from os import system
class Environment:
    def __init__(self,name=""):
        self.molecules = []
        self.name=name

    
    def show(self):
        print("Name:" + self.name)
        print("Molecules in this Environment:")
        for atom in self.atoms:
            atom.show()

    
    def to_dot(self):
        content = ""
        
        idx = 0 
        
        dot_names = {}
        for molecule in self.molecules: 
            idx+=1

#            if length(molecule.parts)>0:
#                for part in molecule.parts:
                    
#            else:
        dot_name = molecule.display_name + str(idx)
        label_name = molecule.display_name
        content += "\"" + dot_name + "\" [label=\"" + label_name + "\"];\n"
        dot_names[molecule] = "\"" + dot_name + "\""
        
        bonds = {}
        for m in self.molecules:
            for bond in m.intermolecularbonds:
                if not bond in bonds:
                    content += dot_names[bond.molecule1] + " -- " + dot_names[bond.molecule2]                              
                    content += ";\n"
                    bonds[bond]=True

        return "graph G {\n" + content + "\n}"
    def to_dot2(self,filename="environment.gv",sizeOverride=None,engine="neato"):
        g = Graph(format="png",engine=engine)        
#                g = Graph(format="png",engine="fdp")        
        if sizeOverride!=None:
            g.graph_attr["size"]=sizeOverride
        g.graph_attr["ratio"]="0.75"
#        g.node_attr["group"]="group1"
        cluster_index = 0
        idx = 0 
        
        dot_names = {}
        for molecule in self.molecules:
            idx+=1

            dot_name = molecule.display_name + str(idx)
            label_name = molecule.display_name
            #content += "\"" + dot_name + "\" [label=\"" + label_name + "\"];\n"
#            g.node(dot_name, label_name)
            dot_names[molecule] = dot_name

                
            if len(molecule.parts)>0:
                idx2 = 0
                cluster_index+=1
                cluster_name ="cluster_" + str(cluster_index)
                sg = Graph(cluster_name)
                sg.body.append('label = "'+ molecule.display_name + '"')
                dot_names[molecule] = cluster_name
                for part in molecule.parts:
                    idx2 += 1
                    part_dot_name = part.display_name + str(idx)+"p"+str(idx2)
                    part_label_name = part.display_name
                    sg.node(part_dot_name, part_label_name)
                    dot_names[part] = part_dot_name
                #g.node("struct1","''<f0> left|<f1> mid&#92; dle|<f2> right''")
 #               g.node('struct1', '''<
#                    <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
#                    <TR><TD>whoelrow</TD></TR>
#                      <TR>
#                        <TD>left</TD>
#                        <TD PORT="f1">middle</TD>
#                        <TD PORT="f2">right</TD>
#                      </TR>
#                    </TABLE>>''') #,_attributes={'shape':'record'}
                g.subgraph(sg)
            else:
                dot_name = molecule.display_name + str(idx)
                label_name = molecule.display_name
                #content += "\"" + dot_name + "\" [label=\"" + label_name + "\"];\n"
                g.node(dot_name, label_name)
                dot_names[molecule] = dot_name
                
        bonds = {}
        for m in self.molecules:
            for bond in m.intermolecularbonds:
                if not bond in bonds:
                    #content += dot_names[bond.molecule1] + " -- " + dot_names[bond.molecule2]
                    
                    g.edge(dot_names[bond.molecule1],dot_names[bond.molecule2])
                    #content += ";\n"
                    bonds[bond]=True
            if len(m.parts)>0:
                print("")
                for part in m.parts:
                    for b in part.intermolecularbonds:
                        if not b in bonds:
                            g.edge(dot_names[b.molecule1],dot_names[b.molecule2])
                            #content += ";\n"
                            bonds[b]=True
                    
        #g.edge("struct1:f2","TF2H")
        #g.edge("struct1:f1","TF2H")
        if False:

            sg = Graph("cluster_1")
            sg.body.append('label = "process #2"')
            sg.node("other clus")
            sg.edge("my cluster","other clus")
            g.subgraph(sg)
            g.node("connectme")
            g.edge("connectme","other clus")
            g.edge("cluster_1","nonesene")

        g.render("output/" + filename,view=False)        

def imageName(prefix,index):
    strIndex=str(index)
    while len(strIndex)<3:
        strIndex="0" + strIndex
    return prefix+strIndex    

def createAudioFile(outputName,text):
    
    #Alex", Vicki, Victoria, Zarvox
    cmd="say -o " + outputName + ".aiff " + text
    os.system(cmd)
    
def saveMovie(inputPrefix,outputPrefix,frameRate = "1/3",audioFile=None):
    #todo strip unsafe chars out of input and output prefix
    cmd = "ffmpeg -framerate " + str(frameRate) + " -i output/" + inputPrefix + "%03d.png"
    
    if audioFile!=None:
        cmd+=" -i " + audioFile
    cmd += " -c:v mpeg4 -pix_fmt yuv420p output/"+outputPrefix + ".mp4"
    
    os.system(cmd)
