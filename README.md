# lifegraph

This is a little experiment in learning some basic molecular and cell biology by modeling it graphically. 

This project allows for modeling the structures of varios molecules and linking them together and portraying changing systems over time.

GraphViz is used for layouts of still images, then FFMpeg is used to compile the GraphViz output into a simple movie. 



GraphViz rendering offers a choice of layout engine. 
The fdp engine handles subgraphs better. 
The neato engine seems to generally give the better images though for most of these models if nesting (containment) is not an issue. 
