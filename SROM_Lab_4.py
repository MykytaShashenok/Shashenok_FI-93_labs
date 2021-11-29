
field_element_1_in_str = str(input())
field_element_2_in_str = str(input())
power_number_in_str = str(input())

DEG_GEN = 491
P = 2*DEG_GEN + 1

normal_basis_neutral_element_multiplication = [1]*DEG_GEN
normal_basis_neutral_element_addition = [0]*DEG_GEN

array = [1]*DEG_GEN
array[0] = 0
power_for_inverse = array

pows_of_two_mod = [0]*DEG_GEN
for i in range(DEG_GEN):
    pows_of_two_mod[i] = (2**i) % P
    
lambda_matrix = [[0]*DEG_GEN for i in range(DEG_GEN)]
for i in range(DEG_GEN):
    for j in range(DEG_GEN):
        if ((pows_of_two_mod[i] + pows_of_two_mod[j]) % P == 1 or
            (-pows_of_two_mod[i] + pows_of_two_mod[j]) % P == 1 or
            (pows_of_two_mod[i] - pows_of_two_mod[j]) % P == 1 or
            (-pows_of_two_mod[i] - pows_of_two_mod[j]) % P == 1):
            lambda_matrix[i][j] = 1

vector = [0]*DEG_GEN           

for i in range(DEG_GEN):
    vector[i] = []
    for j in range(DEG_GEN):
        if lambda_matrix[i][j] == 1:
            vector[i].append(j)

def field_elements_to_list(element_in_str):
    element_in_list = [0]*DEG_GEN
    if (len(element_in_str) > DEG_GEN):
        return 0
    else:
        for i in range(len(element_in_str)):
            element_in_list[i] = int(element_in_str[i], 2)
        return element_in_list

def power_number_to_list(element_in_str):
    element_in_list = [0]*DEG_GEN
    if (len(element_in_str) > DEG_GEN):
        return 0
    else:
        for i in range(len(element_in_str)):
            element_in_list[i] = int(element_in_str[len(element_in_str)-i-1], 2)
        return element_in_list

x1 = field_elements_to_list(field_element_1_in_str)
x2 = field_elements_to_list(field_element_2_in_str)
x3 = power_number_to_list(power_number_in_str)

def reverse_convert_hex_to_string(element_in_list):
    string = "".join(map(str,element_in_list))
    return string

def cyclic_bits_to_high(element, k):
    cyclic_element = [0]*DEG_GEN
    for i in range(DEG_GEN):
        cyclic_element[i] = element[i - k]  
    return cyclic_element

def cyclic_bits_to_low(element, k):
    element_copy = element.copy()
    for i in range(k):
        element_copy.append(element_copy.pop(0))
    return element_copy

def high_bit_number_integer(integer):
    integer_1 = integer[::-1]
    for i in integer_1:
         if i != 0:
            return DEG_GEN - integer_1.index(i) - 1

def normal_basis_addition(element_1, element_2):
    element_3 = [0]*DEG_GEN
    for i in range(DEG_GEN):
        element_3[i] =  (element_1[i] ^ element_2[i])
    return element_3

def normal_basis_square(element):
    return cyclic_bits_to_high(element, 1)

def normal_basis_multiplication(element_1, element_2):
    mult_result = [0]*DEG_GEN
    for i in range(DEG_GEN):
        new_element = [0]*DEG_GEN
        shifted_element_1 = cyclic_bits_to_low(element_1, i)
        shifted_element_2 = cyclic_bits_to_low(element_2, i)
        new_element[0] = shifted_element_2[vector[0][0]]
        for j in range(1, DEG_GEN):
            new_element[j] = shifted_element_2[vector[j][0]] ^ shifted_element_2[vector[j][1]]
        dot_product = 0
        for k in range(DEG_GEN):
            dot_product ^= shifted_element_1[k] & new_element[k]
        mult_result[i] = dot_product
    return mult_result

def normal_basis_power(element, power_num):
    C = normal_basis_neutral_element_multiplication
    for i in range(high_bit_number_integer(power_num) + 1):
        if power_num[i] == 1:
            C = normal_basis_multiplication(C, element)
        element = normal_basis_square(element)
    return C

def inverse_field_element(element):
    inverse_element = normal_basis_power(element, power_for_inverse)
    return inverse_element
    
def normal_basis_trace(element):
    trace = 0
    for i in range(DEG_GEN):
        trace ^= element[i]
    return trace
               
print('This is addtiotn', reverse_convert_hex_to_string(normal_basis_addition(x1, x2)))
print('This is multiplication', reverse_convert_hex_to_string(normal_basis_multiplication(x1, x2)))
print('This is square', reverse_convert_hex_to_string(normal_basis_square(x1)))
print('This is power', reverse_convert_hex_to_string(normal_basis_power(x1, x3)))
print('This is inverse', reverse_convert_hex_to_string(inverse_field_element(x1)))
print('This is trace, 'normal_basis_trace(x1))
