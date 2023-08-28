# -*- coding: utf-8 -*-
"""
Created on Sat Aug 12 10:19:01 2023

@author: lucas
"""

class MetaNumber:
    
    def __init__(self,digits,base=None,sign=None,symbols=None):
        """
        Initializes a MetaNumber object. If only the digits parameter is specified
        the constructor assumes a base 10 representation. In this case, the 'digits'
        parameters can be a integer or string representing the decimal number.
        
        When both digits and base are defined, the digits will simply check if 
        the digits are consistent with the base (i.e., 0 <= digit < base).
    

        Parameters
        ----------
        digits : str, int or list
            List of digits (on little-endian formating) or string representation
            of the number (e.g., '-125', '826', '4AC3' - last one on hex base) or
            an integer. 
        base : int, optional
            Base (radix) of the number representation.
        sign : int, optional
            1 for positive, 0 for zero, -1 for negative.
        symbols : dict, optional
            Mapping between the digits and the number quantity that it represents and 
            vice-versa. For a hexadecimal base, for instance, the mapping is
            
            {'0':0, '1':1, ...,'9':9,'A':10,'B':11,...,'E':14,'F':15
             0:'0', 1:'1', ...,9:'9',10:'A',11:'B',...,14:'E',15:'F'}
            
            Note that the same dict maps the symbol to value ('A':11) and the
            value to symbol (11:'A') - not optimal, plus each class stores a version of this
            dict, but for our purposes, it works.
            
            The class provides a static method that generates a standard mapping 
            (check MetaNumber.standard_mapping())

        """
        self.symbols = MetaNumber.standard_mapping() if symbols is None else symbols
        self.digits = []
        self.base10 = None
        
        if digits is None:
            raise RuntimeError('The parameter ''digits'' is mandatory')

        if type(digits) is int:
            self.base10 = digits
            digits = str(digits)

        if type(digits) is str:
            self.base = 10 if base is None else base
        
            # Gets the sign of the number
            if digits == '0':
                self.sign = 0
            elif digits[0] in ['+','-']:
                self.sign = 1 if digits[0] == '+' else -1
                digits = digits[1:]
            else:
                self.sign = 1
            
            for c in digits[::-1]:
                value = self.symbols[c]
                assert 0 <= value < abs(self.base), "Digits must satisfy 0 <= digit < base"
                self.digits.append(value)
        else:
            assert abs(base) >= 2,  "Base cannot be -1, 0 or 1"
            self.base = base
            
            assert sign in (-1,0,1),  "Sign must be -1, 0 or 1"
            self.sign = sign 
            
            for d in digits:
                assert 0 <= d < abs(self.base), "Digits must satisfy 0 <= digit < base"
                self.digits.append(d)
        
        self.init = True
        
    def isInit(self):
        return self.init
    
    def get_sign(self):
        """
        Return the sign of the number.

        Returns
        -------
        int
            1 for positive, -1 for negative, 0 for zero

        """
        return self.sign
    
    def get_base(self):
        """
        Returns the base (radix) of the number representation.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        return self.base
    
    def get_digits(self):
        """
        Returns a shallow copy of the list of digits of the number.

        Raises
        ------
        RuntimeError
            If the current instance is not properly initialized

        Returns
        -------
        list
            List with digits

        """
        if not self.isInit():
            raise RuntimeError('MetaNumber not correctly initialized')
        return self.digits.copy()
    
    def to_base10(self):
        """
        Computes the decimal representation of the number.

        Returns
        -------
        int
            Number on base 10

        """
        if self.base10 is None:
            num = 0
            for i in range(len(self.digitos)):
                num += self.base**i * self.digitos[i]
            self.base10 = num*self.sign
        return self.base10

    def __str__(self):
        n = "".join([self.symbols[i] for i in reversed(self.digits)])
        if self.sign == -1:
            n = "-" + n
        n += '({})'.format(self.base)
        return n
    
    def __repr__(self):
        return self.__str__()
    
    @staticmethod
    def standard_mapping():
       """
       Standard mapping from symbols to digits. This mapping have 35 symbols, 
       with "digits" ranging from zero to 35.
   
       Returns
       -------
       d : dict
           Dictionary mapping symbols to digits
   
       """
       d = {}
       for i in range(10):
           d[str(i)] = i
           d[i] = str(i)
       
       for c in range(65,91):
           d[str(chr(c))] = c - 55 
           d[c - 55] = str(chr(c))
       return d


    def to_base(self, base=2, verbose=False):
        """
        Converts the number to a specified base. This function converts the 
        metanumber to a integer (on base 10) and works from there.

        Parameters
        ----------
        base : int, optional
            Target base for conversion. The default is 2.
        verbose : bool, optional
            Print the division steps on the conversion (probably incorrect for negative 
            bases). The default is False.

        Returns
        -------
        MetaNumber
            MetaNumber converted to the specified radix

        """
        n = self.to_base10() 

        if n == 0:
            return MetaNumber([0],base,0)
        
        if base == self.base:
            return self
        
        sign = 1 if n > 0 else -1
    
        digs = []
        q = n
        
        while (abs(q) > 0):
            q_old = q
            r = q % base
            q = q//base
            if verbose:
                print("{} = {} x {} + {}".format(q,q_old,base,r))
    
            if r < 0:
                q += 1
                r += abs(base)
            
            digs.append(abs(int(r)))
           
        return MetaNumber(digs,base,sign)
    
    
    def __eq__(self, o):
        if type(o) is not MetaNumber:
            return False
                 
        if o.get_base() != self.base:
            return False
        
        if o.get_sign() != self.sign:
            return False
        
        if len(o.digits) != len(self.digits):
            return False
        
        for i in range(len(self.digits)):
            if o.digits[i] != self.digits[i]:
                return False
        
        return True
    

        





