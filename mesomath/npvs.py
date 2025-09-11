'''This module implements classes for Non-Place-Value numeration system and 
related arithmetic. Intended for Mesopotamian metrological systems, 
but class Npvs is of general use.

    |  class  Npvs: Generic class inspired in Imperial Units System lengths
    |  class MesoM: Specializes the Npvs class to handle Mesopotamian measurements. 
    |  class  Blen: Babylonian length system
    |  class  Bsur: Babylonian surface system
    |  class  Bvol: Babylonian volume system
    |  class  Bcap: Babylonian capacity system
    |  class  Bwei: Babylonian weight system
    |  class  BsyG: Babylonian System G
    |  class  BsyS: Babylonian System S
    '''

def cmul(x):
    '''Utility function. Returns list of cumulative products of the factor list x
    
    Example: cmul([4,3,3,22,10,8,3]) returns:
         [1, 4, 12, 36, 792, 7920, 63360, 190080]'''
    if type(x) == list :
        prod = 1
        prodl =[1]
        for i in x :
            prod *= i
            prodl.append(prod)
        return prodl


class Npvs :
    '''This class implement Non-Place-Value System arithmetic
       Example is taken from Imperial length units.
       
    Class Atributes:
        |  title: Definition of the object
        |  uname: Unit names
        |  ufact: Factor between units
        |  cfact: Factor with the smallest unit
        |    siv: S.I. value of the smallest unit
        |    siu: S.I. unit name
        | prtsex: Printing meassurements in sexagesimal (default: False)
       
       
       Instance Attributes
        |    dec: Decimal value of meassurement in terms of the smallest unit
        |   list: List of values per unit

       jccsvq fecit, 2005. Public domain.'''

    title = 'Imperial length meassurement'
    uname = 'in hh ft yd ch fur mi lea'.split()      # Unit names
    ufact = [4,3,3,22,10,8,3]                        # Factor between units
    cfact = [1, 4, 12, 36, 792, 7920, 63360, 190080] # Factor with the smallest unit
    siv = 0.0254  # meters per inch
    siu = 'meters'  # S.I. unit name
    
    def scheme(self):
        '''Returns list with the unit names separated by the corresponding factors
        |  met: meassurement system class'''
        ll=[]
        for i in range(len(self.ufact)):
            ll.append(self.uname[i])
            ll.append('<-' + str(self.ufact[i])+ '-')
        ll.append(self.uname[-1])
        ll.reverse()
        return ll


    def dec2un(self, x) :
        '''Convert decimal integer n to list of int's'''
        result = []
        for i in self.ufact :
            result.append(x % i)
            x //= i
        result.append(x)
        return result

    def __init__(self,x):
        '''Class constructor
            | n: The parameter n can be an integer (sign is ignored) or a properly 
                 formatted string representing the value'''
        if type(x) == int:
            x = abs(x)
            self.dec = x
            self.list = self.dec2un(x)
        elif type(x) == str:
            if x.find('(') >= 0:
                xx = x.split('(')[1:]
                xnew = ''
                for i in xx:
                    xy = i.split(')')
                    if xy[-1].find(self.uname[-1]) >= 0 :
                        coef = self.sexsys(xy[0])
                    else:
                        coef = BsyS(xy[0])
                    xnew += str(coef.dec)+' '
                    xnew += xy[1]+' '
#                print(xnew)
                x = xnew
            ll = x.split()
            l1 = ll[::2]
            l2 = ll[1::2]
            t = 0
            for i in range(len(l2)):
                j = self.uname.index(l2[i])
                t += int(l1[i]) * self.cfact[j]
            self.dec = t
            self.list = self.dec2un(t)
            
    def __add__(self, other):
        '''Overloads `+` operator: returns object with the sum of operands'''
        if type(other) == type(self) :
            return self.__class__(self.dec + other.dec)

    def __sub__(self, other):
        '''Overloads `+` operator: returns object with the absolute difference 
        of operands'''
        if type(other) == type(self) :
            return self.__class__(abs(self.dec - other.dec))

    def __mul__(self, other):
        '''Overloads `-` operator: returns object with the operands product '''
        t = self.dec * other
        return self.__class__(int(round(t,0)))

    def __rmul__(self, other):
        '''Overloads `-` operator: returns object with the operands product '''
        return self.__mul__(other)

    def __truediv__(self, other):
        '''Overloads `/` operator: returns object with the operands product '''
        return self.__class__(int(round(self.dec / other,0)))

    def si(self):
        '''Returns the equivalent in SI units'''
        return self.dec * self.siv

    def SI(self):
        '''Returns string with the equivalent in SI units'''
        return f'{self.dec * self.siv} {self.siu}'

    def __lt__(self, other):
        '''Overloads < operator'''
        return self.dec < other.dec

    def __le__(self, other):
        '''Overloads <= operator'''
        return self.dec <= other.dec

    def __eq__(self, other):
        '''Overloads == operator'''
        return self.dec == other.dec

    def __ne__(self, other):
        '''Overloads != operator'''
        return self.dec != other.dec

    def __gt__(self, other):
        '''Overloads > operator'''
        return self.dec > other.dec

    def __ge__(self, other):
        '''Overloads >= operator'''
        return self.dec >= other.dec

    def __repr__(self):
        ss = []
        for i in reversed(range(len(self.uname))):
            if self.list[i] != 0:
                ss.append(str(self.list[i]))
                ss.append(self.uname[i])
        return ' '.join(ss)

class _MesoM(Npvs):
    '''Specializes the Npvs class to handle Mesopotamian measurements. 
    Introduces the .sex() and .explain() methods and the .prtsex attribute.
    Modifies __repr__()'''
    
    title = 'Sexagesimal sistem'
    uname = 's1 s2 s3 s4'.split()      # Unit names
    ufact = [60,60,60]                        # Factor between units
    cfact = [1, 60, 3600, 216000] # Factor with the smallest unit
    siv = 1  # 
    siu = 'counts'  # S.I. unit name
    prtsex = False  # Printing meassurements in sexagesimal
    ubase = 0   # Base unit for metrological tables

    def sex(self, r=0):
        '''Return sexagesimal floating value of object
        |  r: index of reference unit in uname'''
        from .babn import BabN
        
        return BabN(self.dec)//self.cfact[r]

    def explain(self):
        '''Print some information about the object'''
        print(f"This is a {self.title}: {self}")
        print("    Metrology: ", *self.scheme())
#        print(f"    Factor between units: {self.ufact}")
        print(f"    Factor with unit '{self.uname[0]}': ",*self.cfact)
        print(f"Meassurement in terms of the smallest unit: {self.dec} ({self.uname[0]})")
        print(f"Sexagesimal floating value of the above: {self.sex(False)}")
        print(f"Approximate SI value: {self.SI()}")


    def __repr__(self):
        '''Returns string representation of object.'''
        ss = []
        for i in reversed(range(len(self.uname))):
            if self.list[i] != 0:
                if not self.prtsex:
                    ss.append(str(self.list[i]))
                    ss.append(self.uname[i])
                else:
                    if self.list[i] >= 60:
                        ss.append(str(self.list[i]//60) + ':'
                         + str(self.list[i]%60))
                    else:
                        ss.append(str(self.list[i]))
                    ss.append(self.uname[i])
        return ' '.join(ss)


class BsyG(_MesoM):  # Babylonian System G numeration
    '''This class implement Non-Place-Value System arithmetic
        for Babylonian System-G numeration'''
    title = 'Babylonian System G to count objects'
    uname = 'iku ese bur buru sar saru sargal'.split()
    ufact = [6, 3, 10, 6, 10, 6]
    cfact = [1, 6, 18, 180, 1080, 10800, 64800]
    siv = 1
    siu = '#'
    ubase = 0 # iku

class BsyS(_MesoM):  # Babylonian System S numeration
    '''This class implement Non-Place-Value System arithmetic
        for Babylonian System-S numeration'''
    title = 'Babylonian System S to count objects'
    uname = 'dis u ges gesu sar saru sargal'.split()
    ufact = [10, 6, 10, 6, 10, 6]
    cfact = [1, 10, 60, 600, 3600, 36000, 216000]
    siv = 1
    siu = '#'
    ubase = 0 # dis

class MesoM(_MesoM):
    '''This class complements the _MesoN class by allowing you to express unit 
    coefficients in measurements using the S and G systems as appropriate. It 
    introduces the sexsys attribute and enhances the __repr__ method.'''
    
    sexsys = BsyS
    
    def __repr__(self):
        '''Returns string representation of object.'''
        ss = []
        for i in reversed(range(len(self.uname))):
            if self.list[i] != 0:
                if not self.prtsex:
                    ss.append(str(self.list[i]))
                else:
                    if i == len(self.uname) - 1:
                        ss.append('('+str(self.sexsys(self.list[i]))+')')
                    else:
                        ss.append('('+str(BsyS(self.list[i]))+')')
                ss.append(self.uname[i])
        return ' '.join(ss)


class Blen(MesoM):  # Length
    '''This class implement Non-Place-Value System arithmetic
        for Old Babylonian Period length units'''
    title = 'Babylonian length meassurement'
    uname = 'susi kus ninda us danna'.split()
    ufact = [30,12,60,30]
    cfact = [1, 30, 360, 21600, 648000]
    siv = 0.5/30
    siu = 'meters'
    ubase = 2 # ninda

    def __mul__(self, other):
        '''Overloads `-` operator: returns object with the operands product '''
        if type(other) == Blen :
            t = int(round((self.dec * other.dec)/12. ,0))
            return Bsur(t)
        elif type(other) == Bsur :
            t = int(round((self.dec * other.dec)/30. ,0))
            return Bvol(t)
        else:
            t = self.dec * other
            return self.__class__(int(round(t,0)))

class Bsur(MesoM):  # Surface
    '''This class implement Non-Place-Value System arithmetic
        for Old Babylonian Period surface units'''
    title = 'Babylonian surface meassurement'
    uname = 'se gin sar gan'.split()
    ufact = [180,60,100]
    cfact = [1, 180, 10800, 1080000]
    siv = 36./60/180
    siu = 'square meters'
    ubase = 1 # gin
    sexsys = BsyG

    def __mul__(self, other):
        '''Overloads `-` operator: returns object with the operands product '''
        if type(other) == Blen :
            t = int(round((self.dec * other.dec)/30. ,0))
            return Bvol(t)
        else:
            t = self.dec * other
            return self.__class__(int(round(t,0)))

class Bvol(MesoM):  # Volume
    '''This class implement Non-Place-Value System arithmetic
        for Old Babylonian Period volume units'''
    title = 'Babylonian volume meassurement'
    uname = 'se gin sar gan'.split()
    ufact = [180,60,100]
    cfact = [1, 180, 10800, 1080000]
    siv = 18./60/180
    siu = 'cube meters'
    ubase = 1 # gin
    sexsys = BsyG
    
    def cap(self):
        '''Convert volume to capacity meassurement'''
        return Bcap(18000*self.dec)

    def bricks(self, nalb = 1.0):
        '''Returns the volume in number of bricks equivalent based on their 
        "Nalbanum." 720 for 1 sar volume if nalb is 1. Output is a Bbri object.
          | nalb: nalbanum in decimal e.g. 7.20 for type 2 bricks (defaul: 1.0)'''
        tt = int(nalb * self.dec)
        return Bbri(tt)

class Bcap(MesoM):  #Capacity
    '''This class implement Non-Place-Value System arithmetic
        for Old Babylonian Period capacity units'''
    title = 'Babylonian capacity meassurement'
    uname = 'se gin sila ban bariga gur'.split()
    ufact = [180,60,10,6,5]
    cfact = [1, 180, 10800, 108000, 648000, 3240000]
    siv = 1./60/180
    siu = 'litres'
    ubase = 1 # gin

    def vol(self):
        '''Convert capacity to volume meassurement'''
        if self.dec >= 18000:
            return Bvol(self.dec//18000)
        else:
            print('Volume too small!')
            return None

class Bwei(MesoM):  # Weight
    '''This class implement Non-Place-Value System arithmetic
        for Old Babylonian Period weight units'''
    title = 'Babylonian weight meassurement'
    uname = 'se gin mana gu'.split()
    ufact = [180,60,60]
    cfact = [1, 180, 10800, 648000]
    siv = .5/60/180
    siu = 'kilograms'
    ubase = 1 # gin

class Bbri(MesoM):  # Counting bricks 
    '''This class implement Non-Place-Value System arithmetic
        for Old Babylonian Period counting bricks in sar-b's'''
    title = 'Babylonian brick count'
    uname = 'se gin sar gan'.split()
    ufact = [180,60,100]
    cfact = [1, 180, 10800, 1080000]
    siv = 720/10800
    siu = 'bricks'
    ubase = 1 # gin
    sexsys = BsyG

    def vol(self, nalb = 1.0):
        '''Returns the volume corresponding to a number of bricks  based on their 
        "Nalbanum."  1 sar volume for 720 bricks if nalb is 1. 
        Output is a Bvol object.
          | nalb: nalbanum in decimal e.g. 7.20 for type 2 bricks (defaul: 1.0)'''
        tt = int(self.dec/nalb)
        return Bvol(tt)

