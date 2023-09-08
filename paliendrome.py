def isPalindrome(x):
        x=str(x)
        return x==x[::-1]

h=isPalindrome(121)
print(h)