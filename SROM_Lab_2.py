
my_num_1 = str(input())
my_num_2 = str(input())
my_num_3 = str(input())
NUM_LEN = 256
DOUBLE_LEN = 2*NUM_LEN + 1

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
t3 = convert_hex_to_list(my_num_3)

def BigAddition(res_1 , res_2):
    carry = 0
    C = [0]*NUM_LEN
    for i in range(NUM_LEN):
        temp = res_1[i] + res_2[i] + carry
        C[i] = temp & (15)
        carry = temp >> 4
    return C, carry

def BigModuloAddition(num_1, num_2, num_3):
    X, bit_carry = BigAddition(num_1, num_2)
    Y = NumToDouble(X)
    num_4 = NumToDouble(num_3)
    Y[NUM_LEN] = bit_carry
    _, Z = DoubleBigDivMod(Y, num_4)
    return Z

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

def BigModuloSub(num_1, num_2, num_3):
    if (BigComp(num_1, num_2) >= 0):
        sub_1, _ = BigSub(num_1, num_2)
        _, mod_sub_1 = BigDivMod(sub_1, num_3)
        return mod_sub_1
    else:
        sub_2, _ = BigSub(num_2, num_1)
        _, mod_sub_2 = BigDivMod(sub_2, num_3)
        mod_sub_3, _ = BigSub(num_3, mod_sub_2)
        return mod_sub_3

def BigComp(res_1, res_2):
    i = len(res_1) - 1
    while (i >= 0) and (res_1[i] == res_2[i]):
        i = i - 1
        
    if i == -1 :
        return 0
    else:
        if res_1[i] < res_2[i]:
            return -1
        else:
            return 1

#bool = BigComp(t1,t2)
        
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

def LongShiftDigitsToLow(res_1, m):
    res_2 = [0]*NUM_LEN
    for i in range(NUM_LEN - m):
        res_2[i] = res_1[i+m]
    return res_2
    
def BigMul(res_1, res_2):
    C = [0]*NUM_LEN
    for i in range(NUM_LEN):
        temp = BigOneMulDigit(res_1, res_2[i])
        temp = LongShiftDigitsToHigh(temp, i)
        C,_ = BigAddition (C,temp)
    return C

def BigMulModulo(res_1, res_2, res_3):
    num_1 = BigMul(res_1, res_2)
    _, num_2 = BigDivMod(num_1, res_3)
    return num_2

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

#def last_non_zero_num(number):
#   new_number = number[::-1]
#    for i in new_number:
#        if i != 0:
#           return NUM_LEN - new_number.index(i) - 1
def last_non_zero_num(number):
   new_number = number[::-1]
   for i in new_number:
        if i != 0:
           return len(number) - new_number.index(i) - 1


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
    Q = [0]*NUM_LEN
    while (BigComp(R, res_2) == 1 or BigComp(R,res_2) == 0):
        t = BitLenght(R)
        C = LongShiftBitsToHigh (res_2, t-k)
        if (BigComp(R,C) == -1):
            t = t - 1
            C = LongShiftBitsToHigh (res_2, t-k)
        R,_ = BigSub(R,C)
        Q = SetBit(Q, t-k)
    return Q, R

def DivBy2(res):
    if (res[0] % 2 == 0):
        return 1
    else:
        return 0

def BigMin(res_1, res_2):
    if (BigComp(res_1, res_2) == 1 or BigComp(res_1,res_2) == 0):
        return res_2
    else:
        return res_1

def BigAbsSub(res_1, res_2):
    if (BigComp(res_1,res_2) == 1 or BigComp(res_1,res_2) == 0):
        return BigSub(res_1, res_2)[0]
    else:
        return BigSub(res_2, res_1)[0]

def LongShiftBitToLow(number):
    new_number = [0]*NUM_LEN
    new_number[NUM_LEN - 1] = (number[NUM_LEN - 1] >> 1) & 0xF
    for i in range (0, NUM_LEN - 2):
        new_number[i] = ((number[i] >> 1) | (number[i + 1] << 3)) & 0xF
    return new_number
        
def BinaryGCD(num_1, num_2):
    zero = [0]*NUM_LEN
    gcd = [0]*NUM_LEN
    gcd[0] = 1
    while (DivBy2(num_1) == 1 and DivBy2(num_2) == 1):
        num_1 = LongShiftBitToLow(num_1)
        num_2 = LongShiftBitToLow(num_2)
        gcd = BigOneMulDigit(gcd,2)
         
    while (DivBy2(num_1) == 1):
        num_1 = LongShiftBitToLow(num_1)
    
    while (num_2 != zero):
        while (DivBy2(num_2) == 1):
            num_2 = LongShiftBitToLow(num_2)

        num_1,num_2 = BigMin(num_1,num_2), BigAbsSub(num_1, num_2)
    gcd = BigMul(gcd, num_1)
    return gcd

def BinaryLCM(num_1, num_2):
    n = BinaryGCD(num_1, num_2)
    k = BigMul(num_1, num_2)
    x, _ = BigDivMod(k,n)
    return x

def NumToDouble(num_1):
    num_2 = [0]*DOUBLE_LEN
    for i in range(NUM_LEN):
        num_2[i] = num_1[i]
    return num_2

def DoubleLongShiftDigitsToLow(res_1, m):
    res_2 = [0]*DOUBLE_LEN
    for i in range(DOUBLE_LEN - m):
        res_2[i] = res_1[i+m]
    return res_2

def DoubleBigOneMulDigit(res_1, b):
    carry = 0
    A = [0]*DOUBLE_LEN
    for i in range (DOUBLE_LEN):
        temp = res_1[i]*b + carry
        A[i] = temp & (15)
        carry = temp >> 4
    return A
    

def DoubleBigMul(res_1, res_2):
    C = [0]*DOUBLE_LEN
    for i in range(DOUBLE_LEN):
        temp = DoubleBigOneMulDigit(res_1, res_2[i])
        temp = DoubleLongShiftDigitsToHigh(temp, i)
        C,_ = DoubleBigAddition (C,temp)
    return C
    

def DoubleBigSub(res_1, res_2):
    B = [0]*DOUBLE_LEN
    borrow = 0
    for i in range (DOUBLE_LEN):
        temp = res_1[i] - res_2[i] - borrow
        if (temp >= 0):
            B[i] = temp
            borrow = 0
        else:
            B[i] = 16 + temp
            borrow = 1
            
    return B, borrow

def DoubleLongShiftDigitsToHigh(res_1, m):
    res_2 = [0]*DOUBLE_LEN
    for i in range(DOUBLE_LEN - m):
        res_2[i+m] = res_1[i]
    return res_2

def DoubleBitsToHighUntil_3(number, k):
    new_number = [0]*DOUBLE_LEN
    new_number[0] = (number[0] << k) & 0xF
    for i in range (1, DOUBLE_LEN - 1):
        new_number[i] = ((number[i] << k) | (number[i-1] >> 4 - k)) & 0xF
    return new_number

def DoubleLongShiftBitsToHigh(number, n):
    x = n // 4
    y = n % 4
    new_number_1 = DoubleLongShiftDigitsToHigh(number, x)
    new_number_2 = DoubleBitsToHighUntil_3(new_number_1, y)
    return new_number_2

def DoubleBigDivMod(res_1, res_2):
    R = res_1
    k = BitLenght(res_2)
    #print('bit - l',k)
    Q = [0]*DOUBLE_LEN
    while (BigComp(R, res_2) == 1 or BigComp(R,res_2) == 0):
        t = BitLenght(R)
        C = DoubleLongShiftBitsToHigh (res_2, t-k)
        #print('shift',C)
        if (BigComp(R,C) == -1):
            t = t - 1
            #print('bit-l-1', t)
            C = DoubleLongShiftBitsToHigh (res_2, t-k)
            #print('shiftbit',C)
        R,_ = DoubleBigSub(R,C)
        #print('R',R)
        Q = SetBit(Q, t-k)
        #print('Q',Q)
    return Q, R

def BarettPrecomp(module_0):
    k = last_non_zero_num(module_0) + 1
    module = NumToDouble(module_0)
    new_number = [0]*DOUBLE_LEN
    new_number[2*k] = 1
    myu, _ = DoubleBigDivMod(new_number, module)
    return module, k, myu

def BarettReduction(number_1, BarettPc):
    q_0 = DoubleLongShiftDigitsToLow(number_1, BarettPc[1] - 1)
    q_0 = DoubleBigMul(q_0, BarettPc[2])
    q_0 = DoubleLongShiftDigitsToLow(q_0, BarettPc[1] + 1)
    q_module = DoubleBigMul(q_0, BarettPc[0])
    r = DoubleBigSub(number_1, q_module)
    while (BigComp(r, BarettPc[0]) >= 0):
        r = DoubleBigSub(r, BarettPc[0])
    return r

def BigModPowerBarett(num_1, num_2, num_3):
    num_4 = [0]*DOUBLE_LEN
    num_4[0] = 1
    BarettPc = BarettPrecomp(num_3)
    for i in range(BitLenght(num_2)):
        if (GetBit(num_2,i) == 1):
            num_4 = BarettReduction(DoubleBigMul(num_4, num_1), BarettPc)
        num_1 = BarettReduction(DoubleBigMul(num_1, num_1), BarettPc)
    return num_4

x1 = BigModuloAddition(t1, t2, t3)
x2 = BigModuloSub(t1, t2, t3)
x3 = BigMulModulo(t1, t2, t3)
x4 = BigModPowerBarett(t1, t2, t3)
y1 = reverse_convert_hex_to_string(x1)
y2 = reverse_convert_hex_to_string(x2)
y3 = reverse_convert_hex_to_string(x3)
y4 = reverse_convert_hex_to_string(x4)

print('This is modulo addition', y1)
print('This is modulo subtraction', y2)
print('This is modulo multiplication', y3)      
Z1 = BinaryGCD(t1,t2)
Z2 = BinaryLCM(t1,t2)
W1 = reverse_convert_hex_to_string(Z1)
W2 = reverse_convert_hex_to_string(Z2)
print('This is gcd', W1)
print('This is lcm',W2)
print('This is modulo power', y4)
        
        
    
    
        

#X1,_ = BigAddition(t1,t2)
#Y1 = reverse_convert_hex_to_string(X1)
#X2,_ = BigSub(t1,t2)
#Y3 = X3_bool = BigComp(t1,t2)
#X4 = BigMul(t1,t2)
#Y4 = reverse_convert_hex_to_string(X4)
#X5,X6 = BigDivMod(t1,t2)
#Y5 = reverse_convert_hex_to_string(X5)
#Y6 = reverse_convert_hex_to_string(X6)
# X7 = BigPower(t1,t2)
# Y7 = reverse_convert_hex_to_string(X7)

          
#print("Result of addition is:")
#print(Y1)
#print("Result of subtraction is:")
#print(Y2)
#print("Result of comprassion is:")
#print(Y3)
#print("Result of multiplication is:")
#print(Y4)
#print("Result of divison is:")
#print(Y5)
#print(Y6)
#print("Result of power is:")
#print(Y7)
