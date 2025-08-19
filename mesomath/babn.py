from math import log, sqrt


class BabN:
    '''This class implements a sexagesimal representation of the natural numbers and their basic arithmetic operations, especially in their "floating" version, as performed by Babylonian scribes. Hence the name.
    
    Class attributes:
        |     sep: separator for string representation (default: ":")
        |    fill: if True writes: "01.33.07" instead of "1.33.7" (default: False)
        | rdigits: approximate number of sexagesimal digits for some results (default: 6:
        |database: path to sqlite3 database of regular numbers providing:
        |    regular    TEXT, regular number e.g. 01:18:43:55:12
        |    len     INTEGER, its length e.g. 5 for 01:18:43:55:12
        |   see hamming.py for how to generate it

    Instance attributes:
        |     dec: decimal versión of number (ex: 405 for sexagesimal "6:45")
        |    list: list of sexagesimal digits of number (ex: [6, 45] for 405 or "6:45")
        |   isreg: True if number is regular (only contains 2, 3, 5 as divisors)
        | factors: tuple with the powers of 2, 3, 5 and the remainder
        
    jccsvq fecit, 2005. Public domain.'''

    sep = ":"
    fill = False
    rdigits = 6
    database = 'regular.db3'
    
    def dec2list(n):
        '''Convert integer decimal n to list of int's (sexagesimal digits)'''
        if n < 60:
            return [n]
        else:
            rlist=[]
            while n >= 60:
                rlist.append(n % 60)
                n = n // 60
            if n > 0:
                rlist.append(n)
            rlist.reverse()
        return rlist

    def parse(n):
        '''Writes instance dec and list.
        | n: may be an integer (sign is ignored), a correctly formated string (e.g., 405, "02:45" or "2.45") or a list (e.g., [1, 12, 23])'''
        if type(n) == list :
            lt = n
            rs = 0
            for i in lt:
                rs = rs*60 +i
            return (rs, lt)
        if type(n) == int :
            return (abs(n), BabN.dec2list(abs(n)))
        if type(n) == str :
            if n.find(':') > 0 :
                lt = [int(j) for j in n.split(':')]
            elif n.find('.') > 0 :
                lt = [int(j) for j in n.split('.')]
            else:
                lt = [int(n)]
            rs = 0
            for i in lt:
                rs = rs*60 +i
            return (rs, lt)

    def __init__(self, n):
        '''Class constructor
        | n: The number n can be an integer (sign is ignored) or a properly formatted string representing a sexagesimal number, accepting the separators ":" or "." (e.g., 405, "02:45" or "2.45") or a list (e.g., [1, 12, 23]).
        '''
        (self.dec, self.list) = BabN.parse(n)
        if self.dec == 1:
            self.isreg = True
        else:
            x = self.dec
            i = j = k = 0
            while x % 2 == 0:
                i += 1
                x //= 2
            while x % 3 == 0:
                j += 1
                x //= 3
            while x % 5 == 0:
                k += 1
                x //= 5
            if x > 1:
                self.isreg = False
            else:
                self.isreg = True
            self.factors = (i, j, k, x)
                
    def inv(self, digits = 4):
        '''Returns an approximate inverse of the number'''
        x = self.dec
        nsd = int(log(x)/log(60))
        inv = (pow(60, nsd+digits))/x
        inv = int(round(inv,0))
        while inv % 60 == 0 :
            inv //= 60
        return BabN(inv)


    def float(self):
        '''Returns the floating part of the number (mantissa)'''
        x = self.dec
        while x % 60 == 0 :
            x //= 60
        return BabN(x)

    def len(self):
        '''Returns the number of sexagesimal digits of the number'''
        return len(self.list)

    def __add__(self, other):
        '''Overloads `+` operator'''
        return BabN(self.dec + other.dec)

    def __sub__(self, other):
        '''Overloads `-` operator'''
        return BabN(abs(self.dec - other.dec))

    def __mul__(self, other):
        '''Overloads `*` operator'''
        return BabN(self.dec * other.dec)

    def __truediv__(self, other):
        '''Overloads `/` operator'''
        a = self.dec
        b = other.dec
        q = a / b
        nsd = int(log(q)/log(60))
        inv = pow(60, BabN.rdigits - nsd) * q
        inv = int(round(inv,0))
        while inv % 60 == 0 :
            inv //= 60
        return BabN(inv)

    def __floordiv__(self, other):
        '''Overloads `//` operator'''
        if other.isreg :
            inv = other.rec().dec
            q = self.dec * inv
            while q % 60 ==0 :
                q //= 60
            return BabN(q)
        else:
            print('Divisor is nor a regular number!')

    def __pow__(self, x):
        '''Overloads `**` operator'''
        try:
            return BabN(self.dec ** x)
        except:
            print('x must be a positive integer')

    def rec(self):
        '''Returns the reciprocal of a regular number, None for a non-regular'''
        if self.isreg:
            x = self.dec
            while x % 60 == 0:
                x //= 60
            if x == 1:
                return BabN(1)
            i = j = k = 0
            while x % 2 == 0:
                i += 1
                x //= 2
            while x % 3 == 0:
                j += 1
                x //= 3
            while x % 5 == 0:
                k += 1
                x //= 5

            i0 = j0 = k0 = 0
            if i % 2 == 1:
                i0 += 1
                i += 1
            if j > k:
                k0 += j - k
                k += j - k
            if k > j:
                j0 += k - j
                j += k-j
            if i < 2 * j:
                i0 += 2 * j -i
                i += 2 * j -i
            if i > 2 * j:
                t = (i-2*j)//2
                j += t
                k += t
                j0 += t
                k0 += t
            return BabN(pow(2,i0)*pow(3,j0)*pow(5,k0))
        else:
            print('Not regular!')
            return None

    def sqrt(self):
        '''Returns approximate floating square root'''
        digits = BabN.rdigits - 1
        x0 = x = self.dec
        sqr = (pow(60, digits))*sqrt(x)
        sqr = int(round(sqr,0))
        while sqr % 60 == 0 :
            sqr //= 60
        return BabN(sqr)

    def cbrt(self):
        '''Returns approximate floating cube root'''
        digits = BabN.rdigits - 1
        x0 = x = self.dec
        cbr = (pow(60, digits))*x**(1./3)
        cbr = int(round(cbr,0))
        while cbr % 60 == 0 :
            cbr //= 60
        return BabN(cbr)

    def dist(self,n):
        '''Estimates a certain "distance" between two sexagesimal numbers. The objective is, given a non-regular number, to select the regular number that is closest to it from a list.
    | n: may be an integer, formated string (ex: "1:2:3"), a list (ex., [1, 12, 23]) or another BabN object'''
        list1 =[] + self.list
        len1 = self.len()
        if type(n) == BabN :
            list2 = [] + n.list
            len2 = n.len()
            print(self.dec, n.dec)
        else:
            (ndec, list2) = BabN.parse(n)
            len2 = len(list2)
        if len1 > len2 :
            list2 += [0 for i in range(len1-len2)]
        elif len2 > len1 :
            nextd = list2[len1]
            list2 = list2[:len1]
            if nextd > 30 :
                list2[-1] += 1
        return (BabN(list1)-BabN(list2)).dec

    def searchreg(self, minn, maxn, limdigits=6, prt=False) :
        '''Search database for regulars between sexagesimals minn y maxn
    
        | minn and maxn: must be sexagesimal strings using ":" separator
        |     limdigits: max regular digits number (default: 6)
        |           prt: print list of regulars found (default: False)
        
        Returns the closest regular as a BabN object'''
        from sqlite3 import connect
        conn = connect(BabN.database)
        cursor = conn.cursor()
        sql_line = """
    SELECT regular
      FROM regulars
     WHERE len <= ? AND 
           regular BETWEEN ? AND ?
     ORDER BY regular
    ;
    """
        cursor.execute(sql_line,(limdigits,minn,maxn))
        rl = cursor.fetchall()
        conn.commit()
        conn.close()

        tmplist = [] + self.list
        if len(tmplist) < limdigits :
            tmplist = tmplist + [0 for i in range(limdigits-len(tmplist))]

        a = BabN(tmplist)
        mind = a.dist(rl[0][0])
        minr = rl[0][0]
        for i in rl :
            i0 = i[0]
            if prt :
                print(f' {a.dist(i[0]):12d} {i[0]}')
            ndis = a.dist(i[0])
            if ndis < mind :
                mind = ndis
                minr = i[0]
        if prt :
            print(f'min d: {mind}, closest regular: {minr}')
        return BabN(minr)

    def __repr__(self):
        rlist = self.list
        if self.fill:
            tt = list(map(str, rlist))
            for i in range(len(tt)):
                if len(tt[i]) == 1:
                    tt[i] = "0"+tt[i]
            return BabN.sep.join(tt)
        else:
            return BabN.sep.join(map(str, rlist))


