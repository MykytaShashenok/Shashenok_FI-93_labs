field_element_1_in_str = str(input())
field_element_2_in_str = str(input())
power_number_in_str = str(input())

DEG_GEN = 491
DOUBLE_DEG = 2*DEG_GEN

zero = [0]*DOUBLE_DEG
zero[DOUBLE_DEG - 492] = 1
zero[DOUBLE_DEG - 18] = 1
zero[DOUBLE_DEG- 7] = 1
zero[DOUBLE_DEG - 3] = 1
zero[DOUBLE_DEG - 1] = 1
polynomial_generator = zero

def field_elements_to_list(element_in_str):
    element_in_list = [0]*DEG_GEN
    if (len(element_in_str) > DEG_GEN):
        return 0
    else:
        for i in range(len(element_in_str)):
            element_in_list[i] = int(element_in_str[len(element_in_str)-i-1], 2)
        element_in_list.reverse()
        return element_in_list
    
def reverse_convert_hex_to_string(element_in_list):
    string = "".join(map(str,element_in_list))
    return string

def power_number_to_list(element_in_str):
    element_in_list = [0]*DEG_GEN
    if (len(element_in_str) > DEG_GEN):
        return 0
    else:
        for i in range(len(element_in_str)):
            element_in_list[i] = int(element_in_str[len(element_in_str)-i-1], 2)
        return element_in_list
    
field_element_1 = field_elements_to_list(field_element_1_in_str)
field_element_2 = field_elements_to_list(field_element_2_in_str)
power_number_in_list = power_number_to_list(power_number_in_str)

def field_addition(element_1, element_2):
    element_3 = [0]*DEG_GEN
    for i in range(DEG_GEN):
        element_3[i] =  (element_1[i] ^ element_2[i])
    return element_3

def bits_to_high(element, k):
    new_element = [0]*DEG_GEN
    for i in range(DEG_GEN - k):
        new_element[i] = element[i+k]
    return new_element

def double_bits_to_high(element,k):
    new_element = [0]*DOUBLE_DEG
    for i in range(DOUBLE_DEG - k):
        new_element[i] = element[i + k]
    return new_element

def bits_to_low(res_1, m):
    res_2 = [0]*DEG_GEN
    for i in range(DEG_GEN - m):
        res_2[i+m] = res_1[i]
    return res_2

def high_bit_number(element):
    for i in element:
         if i != 0:
            return DEG_GEN - element.index(i) - 1

def high_bit_number_integer(integer):
    integer_1 = integer[::-1]
    for i in integer_1:
         if i != 0:
            return DEG_GEN - integer_1.index(i) - 1
        
def double_high_bit_number(element):
    for i in element:
         if i != 0:
            return int(DOUBLE_DEG - element.index(i) - 1)
        
def element_to_double(element):
    double_element = [0]*DOUBLE_DEG
    for i in range(DEG_GEN):
        double_element[i + DEG_GEN] = element[i]
    return double_element
    
def double_addition(element_1, element_2):
    element_1_double = element_to_double(element_1)
    element_2_double = element_to_double(element_2)
    double_element = [0]*DOUBLE_DEG
    for i in range(DOUBLE_DEG):
        double_element[i] = element_1_double[i] ^ element_2_double[i]
    return double_element
        
def modulo_reduction(double_element):
    t = double_high_bit_number(double_element)
    #print(t)
    if (t < 491):
        element = [0]*DEG_GEN
        for i in range(DEG_GEN):
            element[i] = double_element[i + DEG_GEN]
        return element
    else:
        rest_element = double_element
        while (t >= 491):
            #print('r_e', rest_element)
            shifted_generator = double_bits_to_high(polynomial_generator, t - 491)
            #print('s_g', shifted_generator)
            for i in range(DOUBLE_DEG):
                rest_element[i] = (rest_element[i] ^ shifted_generator[i])
            t = double_high_bit_number(rest_element)
        new_rest_element = [0]*DEG_GEN
        for j in range(DEG_GEN):
            new_rest_element[j] = rest_element[j + DEG_GEN]
        return new_rest_element

#def modulo_reduction_new(element):
 #  t = double_high_bit_number(double_element)
  # while (t>= 491):
    #   shifted_generator = double_bits_to_high(polynomial_generator, t - 491)
    #   t_491 = 
         
def field_square(element_1):
     square_element = [0]*DOUBLE_DEG
     for i in range(DEG_GEN):
         square_element[-2*i + 1] = element_1[-i]
     #print(square_element)
     return modulo_reduction(square_element)

def field_multiplication(element_1, element_2):
    norm_element_1 = element_1[::-1]
    norm_element_2 = element_2[::-1]
    mult_result_1 = [0]*DOUBLE_DEG
    mult_result_2 = [0]*DOUBLE_DEG
    for i_1, j_1 in enumerate (norm_element_1):
        for i_2, j_2 in enumerate (norm_element_2):
            mult_result_1[i_1 + i_2] ^= j_1&j_2
    mult_result_2 = mult_result_1[::-1]
    return modulo_reduction(mult_result_2)

def field_power(element_1, power_number):
    C = [0]*DEG_GEN
    C[DEG_GEN - 1] = 1
    #print('This is bit length of number = ', high_bit_number_integer(power_number) + 1)
    for i in range(high_bit_number_integer(power_number) + 1):
        #print('This is i =', i)
        if power_number[i] == 1:
            C = field_multiplication(C, element_1)
            #print('This is C', C)
        element_1 = field_square(element_1)
        #print('This is element_1', element_1)
    return C

def inverse_field_element(element):
    array = [1]*DEG_GEN
    array[0] = 0
    power_for_inverse = array
    inverse_element = field_power(element, power_for_inverse)
    return inverse_element

def trace_of_field_element(element):
    trace = zero
    for i in range(DEG_GEN):
        element = field_square(element)
        trace = field_addition(trace, element)
    return trace
           
print('Result of mul =', reverse_convert_hex_to_string(field_multiplication(field_element_1, field_element_2)))
print('Result of addition =', reverse_convert_hex_to_string(field_addition(field_element_1, field_element_2)))
print('Result of square = ', reverse_convert_hex_to_string(field_square(field_element_1)))
print('Result of power =', reverse_convert_hex_to_string(field_power(field_element_1, power_number_in_list)))
print('Result of inverse =', reverse_convert_hex_to_string(inverse_field_element(field_element_1)))
print('Result of trace = ', reverse_convert_hex_to_string(trace_of_field_element(field_element_1)))