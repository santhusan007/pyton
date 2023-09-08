def myAtoi(s: str) -> int:
    mylist=s.strip().split()
    x=int(ord(mylist[0][1]))
    newlist=mylist[0].split(".")
    if not newlist[0][0]:
        return mylist[0]
    else:        
        if((58>x>47) and (abs(int(mylist[0])))< pow(2,31))  :
            return mylist[0]
        elif int((58>x>47) and (int(mylist[0]) > pow(2,31))):
            return pow(2,31)
        elif int((58>x>47) and (int(mylist[0]) < -pow(2,31))):
            return -pow(2,31)
        else:
            return 0
    
            
print(((" 2.233").split('.')))
print(int(myAtoi(" 2.233")))




#  class Solution:
#     def myAtoi(self, s: str) -> int:
#         mylist=s.strip().split()
#         mylist=mylist[0].split(".")
#         if (mylist[0][1]):
#             x=int(ord(mylist[0][1]))
#             if((58>x>47) and (abs(int(mylist[0])))< pow(2,31))  :
#                 return mylist[0]
#             elif int((58>x>47) and (int(mylist[0]) > pow(2,31))):
#                 return pow(2,31)
#             elif int((58>x>47) and (int(mylist[0]) < -pow(2,31))):
#                 return -pow(2,31)
#             else:
#                 return 0
#         else: 
#             return mylist[0]       

        

# print(myAtoi("91283472"))
