import numpy as np

#first iteration using the technique of sorthing everything as close to the left as possible and as close to the right as possible
def get_probabilities_simple(board_size, hints):
    left_result=np.array([0]*board_size)
    right_result=np.array([0]*board_size)

    #create left stacked results
    left_ptr=0
    index=1
    for i in hints:
        left_result[left_ptr:left_ptr+i]=[index]*i
        left_ptr=left_ptr+i+1
        index=index+1

    #create right stacked results
    right_ptr=board_size
    index=len(hints)
    for i in np.flip(hints):
        right_result[right_ptr-i:right_ptr]=[index]*i
        right_ptr=right_ptr-(i+1)
        index=index-1

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

    #TODO: move everything below into the recursive function

    #edge case for when there's only one initial hint
    if (len(hints)==1):
        while(remaining_space>=0):
            results.append(current_row+[0]*remaining_space)
            current_row.insert(0,0)
            remaining_space=remaining_space-1
        return results

    #start the recursive calls
    while (remaining_space>required_remaining_space):
        gen = recursive_check(current_row, remaining_space, hints[1:], index)
        #print (sum(1 for _ in gen))
        for i in gen:
            results.append(i)
        first_block=first_block+1
        remaining_space=remaining_space-1
        current_row.insert(0,0)
    #TODO: move everything above into the recursive call

    #TODO: clean this up
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
print(get_probabilities_brute(5,np.array([1,2])))
#print(get_probabilities_brute(5,np.array([3])))
#print(get_probabilities_brute(10,np.array([4,4])))

# test cases for simple approach
#print(get_probabilities_simple(20, np.array([1,3,9])))
#print(get_probabilities_simple(10, np.array([4,4])))