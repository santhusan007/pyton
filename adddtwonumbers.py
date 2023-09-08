# Input: l1 = [2,4,3], l2 = [5,6,4]
# Output: [7,0,8]
# Explanation: 342 + 465 = 807

def addNumber(list1,list2):
    list1=reversed (list1)
    list2=reversed(list2)
    list1=int(''.join(str(l) for l in list1))
    list2=int(''.join(str(l) for l in list2))
    list3=str(list1+list2)
    print(list3)
    list3=list3[::-1]
    print(list3)
    list3=list((list3))
    list3=[int(l) for l in list3]
    print(list3)
    return list3
    

addNumber([1,2,3],[4,5,3])