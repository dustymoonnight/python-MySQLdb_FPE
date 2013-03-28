'''
Created on 2012-3-17

@author: wanqxu
'''

from Crypto.Cipher import AES
from math import ceil,log
import os
import struct

def split_bin(value,width):
    '''
    Split the "value" to two parts, left and right. "width" is left part'size.
    '''
    B = 1<<width
    l = value/B
    r = value%B
    return (l,r)


class TableItem:
    '''
    An encrypt item for constructing AES table
    '''
    def __init__(self,plaintext,ciphertext):
        '''
        Simply store the plaintext and ciphertext.
        '''
        self.plaintext = plaintext
        self.ciphertext = ciphertext

class AESTable:
    '''
    A permutation table which stores a permutation over the full plaintext set using AES to encrypt.
    '''
    def __init__(self,size,key):
        '''
        Set size for AES table. Set Key for AES cipher. Initialize AES cipher
        '''
        self.size = size
        self.key = key
        self.mode = AES.MODE_CFB
        self.table = []
        self._aes = AES.new(self.key, self.mode)
        self._permutation_table = []
    
    def get_size(self):
        '''
        Get size for AES table.
        '''
        return self.size
    
    def get_key(self):
        '''
        Get key for AES cipher.
        '''
        return self.key
    
    def _aes_encrypt(self,plaintext):
        '''
        Encrypt plaintext use aes chiper.
        '''
        plaintext = str(plaintext)
        ciphertext = self._aes.encrypt(plaintext)
        return TableItem(plaintext,ciphertext)
    
    def _construct_permutation_table(self):
        '''
        Construct permutation table using AES cipher.
        '''
        for i in range(0,self.size):
            self._permutation_table.append(self._aes_encrypt(i))
        self._permutation_table.sort(lambda x,y: cmp(x.ciphertext, y.ciphertext))
    
    def construct_table(self):
        '''
        Construct encrypted array. Index is the plaintext, and the value is ciphertext.
        '''
        self._construct_permutation_table()
        for item in self._permutation_table:
            self.table.append(item.plaintext)
        
    def _get_file_name(self):
        '''
        Get the file's name which store the encrypted array.
        '''
        return str(self.size)+'n'+struct.pack('16s',self.key).encode('hex')
    
    def store_table(self):
        '''
        Store encrypted array to an file.
        '''
        new_file_name = self._get_file_name()
        file = open(new_file_name,'w')
        content=','.join(self.table)
        file.write(content)
        file.close()
    
    def _has_table_in_file(self):
        '''
        Judge whether there is a file which stores the encrypted array.
        '''
        return os.path.isfile(self._get_file_name())
    
    def has_table(self):
        '''
        Judge whether encrypted array has been constructed or not..
        '''
        return len(self.table)>0 or self._has_table_in_file()
    
    def get_table(self):
        '''
        Get encrypted array. Index is the plaintext, and the value is ciphertext.
        '''
        if len(self.table)>0:
            return self.table
        elif self._has_table_in_file():
            file = open(self._get_file_name(),'r')
            content = file.read()
            self.table = content.split(',')
            return self.table
        else:
            self.construct_table()
            return self.table
    
    def tweak(self,t):
        '''
        Give a tweak to an existed table, and return encrypted array.
        '''
        self.get_table()
        new_table = []
        for i in range(0,self.size):
            new_table.append(self.table[(int(self.table[i])+t)%self.size])
        return new_table
    

class BalanceFeistelNet:
    '''
    A Balance Feistel Net
    '''
    def __init__(self,size,key,rounds):
        '''
        Set size for BalanceFeistelNet. 
        Set Key for AES cipher.
        Set rounds for BalanceFeistelNet. 
        '''
        self.size = size
        self.rounds = rounds
        self.key = key
        self.width = int(ceil(log(self.size,2)/2))
        
    def _encode_long(self,value):
        '''
        Encode long int value to binary.
        '''
        l,r = split_bin(value,64)
        encode_plaintext = struct.pack('Q'*2,r,l)[::-1]
        return encode_plaintext
    
    def psuedo_random_func(self,plaintext):
        '''
        This is a psuedo random function by truncated AES.
        '''
        aes =  AES.new(self.key,AES.MODE_CFB)
        ciphertext = aes.encrypt(self._encode_long(plaintext))
        ciphertext2 = bin(int(ciphertext.encode('hex'),16))
        ciphertext10 = int(ciphertext2[-self.width:],2)
        return ciphertext10
    
    def round(self,left,right):
        '''
        A round for BalanceFeistelNet.
        '''
        return left ^ self.psuedo_random_func(right)
    
    def feistel(self,plaintext):
        '''
        Use BalanceFeistelNet to encrypt a plaintext with n rounds.
        '''
        left,right = split_bin(plaintext,self.width)
        for i in range(0,self.rounds):
            tmp = self.round(left, right)
            left = right
            right = tmp
        return left*(1<<self.width)+right
    
    def re_feistel(self,ciphertext):
        '''
        Use BalanceFeistelNet to decrypt a ciphertext with n rounds.
        '''
        left,right = split_bin(ciphertext,self.width)
        for i in range(0,self.rounds):
            tmp = self.round(right, left)
            right = left
            left = tmp
        return left*(1<<self.width)+right


class ImbalanceFeistelNet:
    '''
    A imbalance Feistel Net.
    Use character wise addition.
    '''
    def __init__(self,chars,key,rounds):
        '''
        Set chars for ImbalanceFeistelNet. 
        Set radix for ImbalanceFeistelNet. 
        Set Key for AES cipher.
        Set rounds for ImbalanceFeistelNet. 
        '''
        self.chars = chars
        self.radix = len(chars)
        self.rounds = rounds
        self.key = key
        self._digit_len = self._get_digit_len()
        self._bin_len = int(ceil(log(self.radix,2)))
    
    def _get_digit_len(self):
        '''
        When one char in chars changes to a digit, we must first know the digit length it will be.
        '''
        return len(str(len(self.chars)-1))
    
    def _char_to_digit(self,char):
        '''
        Change a char in chars to digit.
        '''
        try:
            digit = str(self.chars.index(char))
        except:
            raise Exception("Input error, the plaintext has some chars not in FFX configuration.")
        while len(digit) < self._digit_len:
            digit = '0'+digit
        return digit
    
    def str_to_digit(self,str_value):
        '''
        Change a string to digit
        '''
        digit = ''
        for i in range(0,len(str_value)):
            digit = digit+self._char_to_digit(str_value[i])
        return digit
    
    def _digit_to_char(self,digit):
        '''
        Change a digit to char use chars.
        '''
        return self.chars[int(digit)]
        
    def digit_to_str(self,digit):
        '''
        Change a digit to sting.
        '''
        str_value = ''
        i = 0
        while i < len(digit):
            str_value = str_value+self._digit_to_char(digit[i:i+self._digit_len])
            i = i+self._digit_len
        return str_value
    
    def _fill_zero(self,value):
        '''
        Fill zero for the value to fit the length of _digit_len
        '''
        return '0'*(self._digit_len-len(value))+value
    
    def _getwidth(self,str_value):
        '''
        Get the l=split(n) from the string.
        '''
        return len(str_value)/2
    
    def _addition_single_char(self,a,b):
        '''
        Do operation: c = (a + b) mod radix
        '''
        tmp_addition = str((int(a)+int(b))%self.radix)
        return self._fill_zero(tmp_addition)

    def _addition(self,left,right):
        '''
        Do addition for every single char
        '''
        ret = ''
        i = 0
        while i < len(left):
            str_value = self._addition_single_char(left[i:i+self._digit_len], right[i:i+self._digit_len])
            ret = ret+str_value
            i = i+self._digit_len
        return ret
    
    def _subduction(self,minuend,subtrahend):
        '''
        For every single char in minuend and subtrahend find b that make below operation established: 
        c = (a + b) mod radix
        '''
        ret = ''
        i = 0
        while i < len(minuend):
            for j in range(0,self.radix):
                if (self._addition_single_char(j, subtrahend[i:i+self._digit_len]) == minuend[i:i+self._digit_len]):
                    str_value = self._fill_zero(str(j))
                    ret = ret+str_value
                    break
            i = i+self._digit_len
        return ret
    
    def _bin_to_digit(self,binary,width):
        '''
        Change binary to digit with the _bin_len which get from radix
        '''
        ret = ''
        need_bin_len = self._bin_len*width
        binary_len = len(binary)
        tmp_binary = binary[-(need_bin_len%binary_len):]+binary*(need_bin_len/binary_len)
        for i in range(0,width):
            mode_value=str(int(tmp_binary[i*self._bin_len:(i+1)*self._bin_len],2)%self.radix)
            ret = ret+self._fill_zero(mode_value)
        return ret
            
    def psuedo_random_func(self,plaintext,width):
        '''
        This is a psuedo random function by truncated AES.
        '''
        aes =  AES.new(self.key,AES.MODE_CFB)
        ciphertext = aes.encrypt(plaintext)
        ciphertext2 = bin(int(ciphertext.encode('hex'),16))
        return self._bin_to_digit(ciphertext2,width)
        
    def feistel(self,plaintext):
        '''
        Use ImbalanceFeistelNet to encrypt a plaintext with n rounds.
        '''
        width = self._getwidth(plaintext)
        digit_plaintext = self.str_to_digit(plaintext)
        for i in range(0,self.rounds):
            left = digit_plaintext[:width*self._digit_len]
            right = digit_plaintext[width*self._digit_len:]
            tmp = self._addition(left, self.psuedo_random_func(right,width))
            digit_plaintext = right + tmp
        return self.digit_to_str(digit_plaintext)
        
    def re_feistel(self,ciphertext):
        '''
        Use ImbalanceFeistelNet to decrypt a ciphertext with n rounds.
        '''
        cp_len = len(ciphertext)
        width = self._getwidth(ciphertext)
        digit_ciphertext = self.str_to_digit(ciphertext)
        for i in range(0,self.rounds):
            right = digit_ciphertext[:(cp_len-width)*self._digit_len]
            sum = digit_ciphertext[(cp_len-width)*self._digit_len:]
            tmp = self._subduction(sum, self.psuedo_random_func(right,width))
            digit_ciphertext = tmp + right
        return self.digit_to_str(digit_ciphertext)
    
    
class BPS_BC:
    '''
    The BPS_BC is the internal cipher of BPS.
    '''
    def __init__(self,s,key,rounds,tweak):
        '''
        Set radix for BPS_BC. 
        Set Key for AES cipher.
        Set rounds for BPS_BC. 
        Set tweak for BPS_BC.
        '''
        self.s = s
        self.rounds = rounds
        self.key = key
        self.tweak = tweak
    
    def _encode_long(self,value):
        '''
        Encode long int value to binary.
        '''
        l,r = split_bin(value,64)
        encode_plaintext = struct.pack('Q'*2,r,l)[::-1]
        return encode_plaintext
    
    def _addition(self,a,b,n):
        '''
        Do operation of (a+b)%n
        '''
        return (a+b)%n
    
    def _subduction(self,c,a,n):
        '''
        For an operation of c=(a+b)%n, we now know c, a and n, get b
        '''
        if c>=a:
            return c-a
        else:
            return c+n-a
        
    
    def psuedo_random_func(self,plaintext):
        '''
        This is a psuedo random function by truncated AES.
        '''
        aes =  AES.new(self.key,AES.MODE_CFB)
        ciphertext = aes.encrypt(self._encode_long(plaintext))
        ciphertext2 = bin(int(ciphertext.encode('hex'),16))
        ciphertext10 = int(ciphertext2[-96:],2)
        return ciphertext10
    
    def encryption(self,X):
        '''
        Use BPS_BC to encrypt a ciphertext with n rounds.
        '''
        TR = self.tweak%(1<<32)
        TL = (self.tweak-TR)/(1<<32)
        b = len(X)
        Y = [0]*b
        r = b/2
        l = b-r
        L = 0
        R = 0
        for i in range(0,l):
            L = L + X[i]*(self.s**i)
        for i in range(0,r):
            R = R + X[l+i]*(self.s**i)
        for i in range(0,self.rounds):
            if i%2 == 0:
                plaintext = (TR^i)*(1<<96)+R
                random = self.psuedo_random_func(plaintext)%(self.s**l)
                L = self._addition(L, random, self.s**l)
            else:
                plaintext = (TL^i)*(1<<96)+L
                random = self.psuedo_random_func(plaintext)%(self.s**r)
                R = self._addition(R, random, self.s**r)
        for i in range(0,l):
            Y[i] = L % self.s
            L = (L-Y[i])/self.s
        for i in range(0,r):
            Y[i+l] = R % self.s
            R = (R-Y[i+l])/self.s
        return Y
    
    def decryption(self,Y):
        '''
        Use BPS_BC to decrypt a ciphertext with n rounds.
        '''
        TR = self.tweak%(1<<32)
        TL = (self.tweak-TR)/(1<<32)
        b = len(Y)
        X = [0]*b
        r = b/2
        l = b-r
        L = 0
        R = 0
        for i in range(0,l):
            L = L + Y[i]*(self.s**i)
        for i in range(0,r):
            R = R + Y[l+i]*(self.s**i)
        for i in range(0,self.rounds):
            j = self.rounds-i-1
            if j%2 == 0:
                plaintext = (TR^j)*(1<<96)+R
                random = self.psuedo_random_func(plaintext)%(self.s**l)
                L = self._subduction(L, random, self.s**l)
            else:
                plaintext = (TL^j)*(1<<96)+L
                random = self.psuedo_random_func(plaintext)%(self.s**r)
                R = self._subduction(R, random, self.s**r)
        for i in range(0,l):
            X[i] = L % self.s
            L = (L-X[i])/self.s
        for i in range(0,r):
            X[i+l] = R % self.s
            R = (R-X[i+l])/self.s
        return X

class ASCII_Feistel:
    '''
    A Balance Feistel Net just encode ASCII.
    '''
    def __init__(self,cft,original,rounds):
        '''
        Set coefficient for psuedo random function.
        Set original for psuedo random function.
        Set rounds for BalanceFeistelNet. 
        '''
        self.cft = cft
        self.rounds = rounds
        self.original = original
    
    def chaos(self):
        '''
        Chaos is a function to get psuedo random value with expression: xn+1 = a*xn*(1-xn).
        '''
        rd_f = []
        rd = []
        x = self.original
        rd_f.append(x)
        for i in range(1,self.rounds):
            y = self.cft*rd_f[i-1]*(1-rd_f[i-1])
            rd_f.append(y)
        for i in range(0,self.rounds):
            bin_s = ''
            tmp_f = rd_f[i]
            for j in range(0,4):
                tmp_i = int(tmp_f*10)
                if tmp_i >= 5:
                    bin_s = bin_s+'1'
                else:
                    bin_s = bin_s+'0'
                tmp_f = tmp_f*10-tmp_i
            rd.append(int(bin_s,2))
        return rd
            
    def split_ascii(self,char):
        '''
        Split a char to two integer with equal binary size.
        '''
        value = ord(char)
        left = value/16
        right = value%16
        return left,right
    
    def combine_ascii(self,left,right):
        '''
        Combine two integer to a char with ascii.
        '''
        value = left*16+right
        return chr(value)
    
    def encode_one_char(self,char,key):
        '''
        Encode one char use chaos.
        '''
        left,right = self.split_ascii(char)
        tmp = left
        left = right
        right = tmp^key
        return self.combine_ascii(left, right)
    
    def decode_one_char(self,char,key):
        '''
        Decode one char use chaos.
        '''
        left,right = self.split_ascii(char)
        tmp = right
        right = left
        left = tmp^key
        return self.combine_ascii(left, right)
    
    def feistel(self,plaintext):
        '''
        Use BalanceFeistelNet to encrypt a plaintext with n rounds.
        '''
        rd = self.chaos()
        tmp_plaintext = plaintext
        for i in range(0,self.rounds):
            key = rd[i]
            encode_plaintext = ''
            for j in range(0,len(tmp_plaintext)):
                if j == 0:
                    tmp_char = tmp_plaintext[j]
                else:
                    tmp_char = chr(ord(tmp_plaintext[j])^ord(tmp_plaintext[j-1]))
                encode_plaintext = encode_plaintext+self.encode_one_char(tmp_char, key)
            tmp_plaintext = encode_plaintext
            encode_plaintext = ''
        return tmp_plaintext
            
