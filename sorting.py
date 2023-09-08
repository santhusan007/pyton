# num=[12,10,6,3,4,2,1]
# for i in range (len(num)):
#     for j in range(i+1):
#         if num[i]>num[j]:
#             num[i],num[j]=num[j],num[i]

# print(num)    
from functools import lru_cache
@lru_cache(maxsize=1000)
def fib(n):
    if(n <= 1):
        return n
    return (fib(n-1) + fib(n-2))
print(fib(100))
# if __name__=="__main__":
#     number= int(input("please enter1 the number:- "))

#     for i in range (number):
#         print (fib(i))
# def fact(n):
#     if n==0 or n==1:
#         return 1
#     return n*fact(n-1)
# print(fact(0))
# print(fact(1))
# print(fact(5))