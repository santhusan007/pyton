def reverse( x: int) -> int:
    reverse_num=0
    y=abs(x)
    while (y>0):
        reminder=y%10
        reverse_num=reverse_num*10+reminder
        y=y//10
    if (reverse_num>(pow(2,31))):
        return 0
    elif(x < 0):
        return f"-{reverse_num}"
    return reverse_num
print(reverse(15556))
