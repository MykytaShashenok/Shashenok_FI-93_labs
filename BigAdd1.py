from math import ceil

my_num_1 = str(input())
my_num_2 = str(input())
#k = int(input(), 16)
NUM_LEN = 128

def convert_hex_to_list(number):
    num_in_list = [0]*NUM_LEN
    if (len(number) > NUM_LEN):
        return 0
    else:
        for i in range(len(number)):
            num_in_list[i] = int(number[len(number)-i-1], 16)
        return num_in_list
    
t1 = convert_hex_to_list(my_num_1)
t2 = convert_hex_to_list(my_num_2)

def BigAddition(res_1 , res_2):
    carry = 0
    C = [0]*NUM_LEN
    for i in range(NUM_LEN):
        temp = res_1[i] + res_2[i] + carry
        C[i] = temp & (15)
        carry = temp >> 4
    return C, carry

def BigSub(res_1, res_2):
    B = [0]*NUM_LEN
    borrow = 0
    for i in range (NUM_LEN):
        temp = res_1[i] - res_2[i] - borrow
        if (temp >= 0):
            B[i] = temp
            borrow = 0
        else:
            B[i] = 16 + temp
            borrow = 1
            
    return B, borrow

def BigComp(res_1, res_2):
    i = len(res_1) - 1
    while (i >= 0) and (res_1[i] == res_2[i]):
        i = i - 1
        
    if i == -1 :
        return 0
    else:
        if res_1[i] > res_2[i]:
            return 1
        else:
            return -1

bool = BigComp(t1,t2)
        
def BigOneMulDigit (res_1,b): 
    carry = 0
    A = [0]*NUM_LEN
    for i in range (NUM_LEN):
        temp = res_1[i]*b + carry
        A[i] = temp & (15)
        carry = temp >> 4
    return A

def LongShiftDigitsToHigh(res_1, m):
    res_2 = [0]*NUM_LEN
    for i in range(NUM_LEN - m):
        res_2[i+m] = res_1[i]
    return res_2
    
def BigMul(res_1, res_2):
    C = [0]*NUM_LEN
    for i in range(NUM_LEN):
        temp = BigOneMulDigit(res_1, res_2[i])
        temp = LongShiftDigitsToHigh(temp, i)
        C,_ = BigAddition (C,temp)
    return C

def GetMeBitFromHex(num_in_hex, n):
    x = n / 4
    j = ceil(x) - 1
    i = n % 4
    t = num_in_hex[j]
    return (t >> i) & 1  

def BigPower(res_1,res_2): #дописать вытягивание и-ого бита из хекса 
    C = [0]*NUM_LEN
    C[0] = 1
    for i in range(NUM_LEN):
        if GetMeBitFromHex(res_2, i) == 1:
            C = BigMul(C,res_1)
        res_1 = BigMul(res_1,res_1)  
    return C

#def BigPowerWindow(res_1,res_2):
#     C = [0]*NUM_LEN
#     C[0] = 1
#     D = [0]*NUM_LEN
#     B = [0]*NUM_LEN
#     B[0] = 1
#     D[0] = B
#     D[1] = res_1
#     for i in range(15, 2):
#         D[i] = BigMul(D[i-1], res_1)
#     for i in range(NUM_LEN - 1, 0):
#         C = BigMul(C, D[res_2[i]])
#         if i!=0:
#                 C = BigMul(BigMul(BigMul((BigMul(C,C),C),C),C),C)
#   return C 
        
          
print(BigPower(t1, t2))
    
#t3, _ = BigAddition(t1,t2)
#print(t3)
#t4, _ = BigSub(t3,t2)
#print(t4)
