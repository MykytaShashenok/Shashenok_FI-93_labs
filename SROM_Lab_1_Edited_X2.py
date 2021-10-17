
my_num_1 = str(input())
my_num_2 = str(input())
NUM_LEN = 256

def convert_hex_to_list(number):
    num_in_list = [0]*NUM_LEN
    if (len(number) > NUM_LEN):
        return 0
    else:
        for i in range(len(number)):
            num_in_list[i] = int(number[len(number)-i-1], 16)
        return num_in_list
    
def reverse_convert_hex_to_string(number):
    string = map(hex,number)
    my_list_1 = list(string)
    for i in range(len(my_list_1)):
        my_list_1[i] = my_list_1[i].replace('0x','')
    str_1 = ''.join(my_list_1)
    str_2 = str_1[::-1]
   # while str_2[0] == '0':
      #  str_2[0] = str_2[0].replace('0','')
    return str_2
    
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

def GetBit(num_in_hex, n):
    x = n // 4
    i = n % 4
    t = num_in_hex[x]
    return (t >> i) & 1

def SetBit(number, n):
    x = n // 4
    y = n % 4
    t = number[x]
    w = t | (1 << y)
    number[x] = w
    return number

def BitLenght(number):
    k = last_non_zero_num(number)
    t = len(bin(number[k])) - 2
    lenght = 4*k + t
    return lenght

def BigPower(res_1,res_2):
    C = [0]*NUM_LEN
    C[0] = 1
    for i in range(BitLenght(res_2)):
        if GetBit(res_2, i) == 1:
            C = BigMul(C,res_1)
        res_1 = BigMul(res_1,res_1)  
    return C

def last_non_zero_num(number):
    new_number = number[::-1]
    for i in new_number:
        if i != 0:
            return NUM_LEN - new_number.index(i) - 1

#def BitLenght(number):
 #   k = last_non_zero_num(number)
  #  t = len(bin(number[k])) - 2
   # lenght = 4*k + t
    #return lenght

def BitsToHighUntil_3(number, k):
    new_number = [0]*NUM_LEN
    new_number[0] = (number[0] << k) & 0xF
    for i in range (1, NUM_LEN - 1):
        new_number[i] = ((number[i] << k) | (number[i-1] >> 4 - k)) & 0xF
    return new_number

def LongShiftBitsToHigh(number, n):
    x = n // 4
    y = n % 4
    new_number_1 = LongShiftDigitsToHigh(number, x)
    new_number_2 = BitsToHighUntil_3(new_number_1, y)
    return new_number_2 

def BigDivMod(res_1, res_2):
    R = res_1
    k = BitLenght(res_2)
    #print('k=',k)
    #print('res_2=',res_2)
    Q = [0]*NUM_LEN
    while (BigComp(R, res_2) == 1 or BigComp(R,res_2) == 0):
        t = BitLenght(R)
        #print('R=',R)
        #print('t=',t)
        C = LongShiftBitsToHigh (res_2, t-k)
        if (BigComp(R,C) == -1):
            t = t - 1
            C = LongShiftBitsToHigh (res_2, t-k)
        R,_ = BigSub(R,C)
        Q = SetBit(Q, t-k)
    return Q, R
        

X1,_ = BigAddition(t1,t2)
Y1 = reverse_convert_hex_to_string(X1)
X2,_ = BigSub(t1,t2)
Y2 = reverse_convert_hex_to_string(X2)
Y3 = X3_bool = BigComp(t1,t2)
X4 = BigMul(t1,t2)
Y4 = reverse_convert_hex_to_string(X4)
X5,X6 = BigDivMod(t1,t2)
Y5 = reverse_convert_hex_to_string(X5)
Y6 = reverse_convert_hex_to_string(X6)
X7 = BigPower(t1,t2)
Y7 = reverse_convert_hex_to_string(X7)

          
print("Result of addition is:")
print(Y1)
print("Result of subtraction is:")
print(Y2)
print("Result of comprassion is:")
print(Y3)
print("Result of multiplication is:")
print(Y4)
print("Result of divison is:")
print(Y5)
print(Y6)
print("Result of power is:")
print(Y7)
