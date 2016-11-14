#python program  for insight data challenge
#November 13,2016
#Getasew Ashebir
import sys
import getopt
def init_setup(filename, datastruct):
    """This function loads the data structure with the data from the setup file
    (batch_payment.txt). It uses dictionary to represent the 
    undirectional graph with the id as key and list of (id,time,amount,message)
    tuples as values"""
    #open the file to read
    fo = open(filename, "r")
    lines = fo.readlines()
    for l in range(1, len(lines)):
        line = lines[l]
        line = lines[l].split(",")
        if len(line) == 5:
          time =line[0]
          id1 = line[1]
          id2 = line[2]
          amount = float(line[3])
          message = line[4]
          if id1 in datastruct:
            datastruct[id1].append((id2,time,amount,message))
          elif id2 in datastruct:
            datastruct[id2].append((id1,time,amount,message))
          else:
            datastruct[id1] = [(id2,time,amount,message)]
            datastruct[id2] = [(id1,time,amount,message)]

    return datastruct
#function that implements feature1
def check_friendship(datastruct, listpair):
    """checks if the requested users have the history of transaction if they have 
    it returns the message "trusted" if not it returns the message "unverified" """
    if listpair[0] in datastruct:
        if listpair[1] in [datastruct[listpair[0]][i][0]\
           for i in range(len(datastruct[listpair[0]]))]:
            return "trusted" 
        else :
            return "unverified"
    return "unverified"
#function that implements feature 2
def check_if_in_2nddegree_friendship(datastruct, listpair):
    """ Checks if the requested transaction  are with in the 2nd degree network(if they are
    friends of friends)"""
    #return check_if_in_4thdegree_network(datastruct,listpair,2)
    if check_friendship(datastruct,listpair) == "trusted":
      return "trusted"
    if listpair[0] in datastruct:
        for user in datastruct[listpair[0]]:
            for childuser in datastruct[user[0]]:
                if listpair[1] == childuser[0]:
                    return "trusted"
    return "unverified"
#function that implements feature 3
def check_if_in_4thdegree_network(datastruct, listpair,limit):
    """ This function checks if the two users are with 4th degree relation in
       the past transaction. it uses a recursive function recursively_check(...)
        to check until it gets the affirmation that the two users lies in the 
        fourth degree relation ship if not it returns "unverified" message"""
    return recursively_check(listpair[0],datastruct,listpair,limit)
def recursively_check(node,datastruct,listpair,limit):
    """recurses on each edge of the graph starting from the root node until
    the depth limit ends """
    # cutoff_occured is a flag that indicates there is a cut off edge  before
    # ending the recursion
    cutoff_occured = False 
   
    if listpair[1]== node:
        return "trusted"
    elif limit == 0:
        return "unverified"
    elif node not in datastruct:
        return "unverified"
    else:
        
        for user in datastruct[node]:
            result = recursively_check(user[0],datastruct,listpair,limit-1)
            if result == "unverified":
               cutoff_occured = True 
            else:
               return "trusted" 

    if cutoff_occured:
           return "unverified"

def main():
    """The main function used to call initial setup and other function calls """
    try:
        opts,args = getopt.getopt(sys.argv[1:],"h",["help"])
    except getopt.error as msg:
        print(msg)
        print("for help use --help")
        sys.ext(2)
    for o,a in opts:
        if o in ("-h", "--help"):
            print( __doc__)
            sys.exit(0)
    input1 = args[0]
    input2 = args[1]
    output1 = args[2]
    output2 = args[3]
    output3 = args[4]   
    #Declaring the data structure.
    datastruct= {}
    # setting up the initial structure
    init_setup(input1, datastruct)
    #processing input2(stream.txt)
    text_file = open(input2).readlines()  
    result1= open(output1,'w') 
    result2 = open(output2,'w') 
    result3 = open(output3,'w') 
    n = len(text_file)
    for l in range(1,n):
          line = text_file[l].strip()
          line = text_file[l].split(",")
          if len(line) == 5:
            time = line[0]
            id1 = line[1]
            id2 = line[2]
            amount = float(line[3])
            message = line[4]
            listpair = (id1,id2) # for this problem I use only the user ids to detect fraud.
            #testing feature 1
            solution1 = check_friendship(datastruct,listpair)
            if solution1:
              result1.write(solution1+'\n')
            #testing feature 2
            solution2 = check_if_in_2nddegree_friendship(datastruct,listpair)
            if solution2:
              result2.write(solution2+'\n')
            solution3 = check_if_in_4thdegree_network(datastruct,listpair,4)
            if solution3:
              result3.write(solution3+'\n')
    result1.close()
    result2.close()
    result3.close()
     
if __name__== "__main__":
    main()

