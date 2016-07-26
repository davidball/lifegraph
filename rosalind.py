#this is a runner for Rosalind problem solutions. It expects as an argument the short problem id from rosalind (as in the one in the URLs of the Rosalind problems.)

#It looks for an implementation of that problem in a file rosalind/rosalind_{key} with a class nameed Rosalind{key} that subclasses rosalind.RosalindProblem
import rosalind
import imp
import sys

if len(sys.argv)==2:
    print("I will try to find a file rosalind/rosalind_" + sys.argv[1] + ".py")
    try:
        mod_name = 'rosalind_' + sys.argv[1]
        mod =imp.load_source(mod_name, 'rosalind/' + mod_name + '.py')
    except :
        print("Could not find an implemented solution to that problem. Or there was an error in its definition")
        sys.exit()
    
    try:
        problem_class = getattr(mod,"Rosalind" + sys.argv[1])
    except:
        print("Class not implemented with the expected name Rosalind" + sys.argv[1])
        sys.exit()
    
    problem= problem_class()
    problem.run()
    
else:
    print("Please provide one and only one argument to specify which Rosalind problem to run")

#x=inspect.getmembers(rosalind.rosalind_abc,inspect.isclass)