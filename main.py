import numpy as np

#first iteration using the technique of sorthing everything as close to the left as possible and as close to the right as possible
def get_probabilities_simple(board_size, hints, board=None):
    left_result=np.array([0]*board_size)
    right_result=np.array([0]*board_size)

    #board would be given as a list of 0s, 1s and 2s
    #0 means the cell is empty
    #1 means the cell is already filled
    #2 means the cell is crossed out
    #assume for now that there's always a way to set all hints

    #TODO: get stacked results based on already filled squares
    # eg. board=[0,1,0,0,0],hints=[3] -> left_result=[1,1,1,0,0],right_result=[0,1,1,1,0]


    # if no board is provided, assume its entirely empty
    if board is None:
        board=np.array([0]*board_size)

    #create left stacked results
    left_ptr=0
    index=1
    for i in hints:
        #make sure the section we're working with is empty
        while not (np.all(board[left_ptr:left_ptr+i]==0)):
            left_ptr+=1
        left_result[left_ptr:left_ptr+i]=[index]*i
        left_ptr=left_ptr+i+1
        while (left_ptr<len(board) and board[left_ptr]==2):
            left_ptr+=1
        index=index+1
    print(left_result)

    #create right stacked results
    right_ptr=board_size
    index=len(hints)
    for i in np.flip(hints):
        while not (np.all(board[right_ptr-i:right_ptr]==0)):
            right_ptr-=1
        right_result[right_ptr-i:right_ptr]=[index]*i
        right_ptr-=i+1
        while (right_ptr<len(board) and board[right_ptr]==2):
            right_ptr-=1
        index=index-1
    print(right_result)

    #compare for final results
    result=np.array([0]*board_size)
    for i in range(board_size):
        if (left_result[i] != 0 and left_result[i]==right_result[i]):
            result[i]=1
    return result

# second iteration to brute force all possible combinations (probably recursively)
def get_probabilities_brute(board_size, hints):
    results=[]
    index=1
    first_block = hints[0]
    current_row=[index]*(first_block)
    remaining_space = board_size-first_block
    required_remaining_space = sum(hints[1:])+len(hints[1:])-1 

    #edge case for when there's only one initial hint
    if (len(hints)==1):
        while(remaining_space>=0):
            results.append(current_row+[0]*remaining_space)
            current_row.insert(0,0)
            remaining_space=remaining_space-1
    else:
        #start the recursive calls
        while (remaining_space>required_remaining_space):
            gen = recursive_check(current_row, remaining_space, hints[1:], index)
            for i in gen:
                results.append(i)
            first_block=first_block+1
            remaining_space=remaining_space-1
            current_row.insert(0,0)

    print (results)
    probs=[[0]*board_size for i in range(len(hints))]
    for r in results:
        for j in range(len(hints)):
            for innerIndex,k in enumerate(r):
                if (k==j+1):
                    probs[j][innerIndex]=probs[j][innerIndex]+1
                    
    print(probs)

    finalProbs=[{} for i in range(board_size)]
    for i in range(len(hints)):
        for j in range(board_size):
            finalProbs[j][i+1]=probs[i][j]/len(results)
    return finalProbs


def recursive_check(current_row, remaining_space, hints, index):
    required_remaining_space=sum(hints[1:])+len(hints[1:])-1
    index=index+1
    # special case when there's only one hint left
    if (len(hints)==1):
        counter=0
        current_row=current_row+[0]
        remaining_space=remaining_space-1
        while (counter+hints[0]<=remaining_space):
            yield current_row+[0]*counter+[index]*hints[0]+[0]*(remaining_space-(counter+hints[0]))
            counter=counter+1
    else:
        while(remaining_space>required_remaining_space):
            remaining_space=remaining_space-(hints[0]+1)
            current_row=current_row+[0]+[index]*hints[0]
            yield from recursive_check(current_row,remaining_space,hints[1:], index)
            remaining_space=remaining_space-1
            current_row.insert(0,0)
    


# test cases for brute force approach
#print(get_probabilities_brute(5,np.array([2,1])))
#print(get_probabilities_brute(5,np.array([1,1,1])))
#print(get_probabilities_brute(5,np.array([1,2])))
#print(get_probabilities_brute(5,np.array([3])))
#print(get_probabilities_brute(10,np.array([4,4])))

# test cases for simple approach
#print(get_probabilities_simple(20, np.array([1,3,9])))
print(get_probabilities_simple(10, np.array([4,4])))
print ("with board")
print(get_probabilities_simple(10, np.array([4,4]),np.array([0,0,0,0,2,0,0,0,0,0])))
#print(get_probabilities_simple(5, np.array([2]),np.array([0,0,0,2,0])))
#print(get_probabilities_simple(5, np.array([2])))