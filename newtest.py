# x=[61,60,59,58,57,53,52,51,50,47,46,45,44,43,40,39,38,37,36,33,32,31,30,29,26,25,24,23,22,19,18,17,16,15,12,11,10,9,8,5,4,3,2,1]
# print(x[:2])
# # for i in x:
# #     print(i)

# datelist = [6,5,4,3,2]

# y = [31,30,29,26,25,24,23,22,19,18,17,16,15,12,11,10,9,8,5,4,3,2,1]
# for i in y:
#     print(i)
from nsepy import get_rbi_ref_history
import  datetime as dt
rbi_ref = get_rbi_ref_history(dt.date(2015,1,1), dt.date(2015,1,10))
# print(dt.date(2015, 1,1)-dt.date(2015,1,10))