
class Graph {
    constructor() {
        this.nodes = new Map();
        this.edges = new Map();
    }
    addNode(key, label) {
        //if not label provided just use the key as the label
        this.nodes.set(key, label||key)
    }
    addNodes(list_of_key_label) {
        var self = this;
        for (var n of list_of_key_label) {
            self.addNode(n[0],n[1]);
        }
    }
    addLinkedNode(source_key, target_key, target_label) {
        //creates a target node that (may) not exist and links them.
        this.addNode(target_key, target_label);
        this.addEdge(source_key, target_key);
    }
    addLinkedNodes(l) {
        //exepcts list of [source_key, target_key, target_label]
        var self = this;
        for (var item of l) {
            self.addLinkedNode(item[0],item[1],item[2]);
        }
    }
    addEdge(from_key, to_key, directed = true) {
        var edgeKey = from_key + "-" + (directed ? ">" :"") + to_key;
        this.edges.set(edgeKey,"")
    }
    addEdges(list_of_dot_edges) {
        var self = this;
        for (var e of list_of_dot_edges) {
          var parts = e.split("->");
            var directed = true;
            if (parts.length<2) {
                parts = e.split("-");
                directed = false;
            }
            if (parts.length==2) {
                self.addEdge(parts[0],parts[1],directed)
            }
        }
  
    }
    removeNode(node_id) {
        this.nodes.delete(node_id);
        var that = this;
        for (var [key, value] of this.edges)  {
            if (key.includes(node_id)) {
                that.edges.delete(key);
            }            
        };
    }
    copy() {
        var c = new Graph()
        c.nodes = new Map(this.nodes);
        c.edges = new Map(this.edges);
        return c;
    }
    toDot() {
   /* expects g= {"nodes":{Map}{node_id: DotString for node with label and other properties, }
          ,edges: {Map} {"nodeid1->nodeid2":'dot string for any edge properties or blank ok too}}
  
          use a js Map because order might matter for the dot to d3 business
          */
          var lines = []
          for (var [key, value] of this.nodes)  {
  
              lines.push(`${key} [label="${value}"];`);
          };
  
          for (var [key, value] of this.edges)  {
              lines.push(key  + ";")
          };
          
          
          var dotstring = "digraph G {\n" + lines.join("\n") + "\n}";
  
          return dotstring;
    }
  }

var frameShiftDuration = 400;

function makeDotsFromSubGraphs(startGraph, operations) {
    var dots = [];
    dots.push(startGraph.toDot());

    currentGraph = startGraph.copy();
    for (var op of operations) {
        //tmp assume op is add. 
        var opname = op[0];
        if (opname=="addnode") {
            currentGraph.addNode(op[1],op[2]);
        } else if (opname == "addedge") {
            currentGraph.addEdge(op[1],op[2]);
        } else if (opname == "addlinkednode") {
            //expects [opname, sourcekey, targetkey, targetlabel]
            currentGraph.addLinkedNode(op[1],op[2],op[3]);
        } else if (opname=="addlinkednodes") {
            currentGraph.addLinkedNodes(op[1]);
        } else if (opname == "removenode") {
            currentGraph.removeNode(op[1]);
        }
        dots.push(currentGraph.toDot())
    }
    return dots;
}



  function renderArrayOfDots(dots) {

    var dotIndex = 0;
    var graphviz = d3.select("#graph").graphviz()
        .transition(function () {
            return d3.transition("main")
                .ease(d3.easeLinear)
                .delay(10)
                .duration(frameShiftDuration);
        })
        //.logEvents(true)
        //.on("initEnd", render);
    
    function render() {
        var dot = dots[dotIndex];
        
        graphviz
            .renderDot(dot)
            .on("end", function () {
                
                dotIndex = dotIndex + 1;
                if (dotIndex<dots.length){
                    render();
                }
                
            });
    }
    render();
    }
    