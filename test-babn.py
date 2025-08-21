from mesomath.babn import BabN
from math import sqrt

# Creating instances
a = BabN('1.12.23')
b = BabN(405)

print('\nSome basic tests of BabN class follow:')

print(f'\nA couple of BabN numbers: a: {a} and b: {b}')
print(f'    Are they regular? a: {a.isreg}, b: {b.isreg}')
print(f'    Factors a: {a.factors}, b: {b.factors}')
print('Otherwise:')
print('a.explain()')
a.explain()
print('b.explain()')
b.explain()
print('\nBasic operations with them:')
print('     a + b = ',a+b)
print('     a - b = ',a-b)
print('     a * b = ',a*b)
print('    a**2 = ',a**2)
print('    a**4 = ',a**4)

print('\nComparisons:')
print('     a > b = ',a>b)
print('     a <= b = ',a<=b)
print('     not a <= b = ',not a<=b)
print('    a == a = ',a==a)
print('    a != a - 1 = ',a!=a-1)

print(f'\nApproximate inverse of a is: {a.inv()}\n    Testing: a*a.inv() = {a*(a.inv())}')
print(f'    Now using a.inv(8) we have: {a.inv(8)}\n    Testing: a*a.inv(8) = {a*(a.inv(8))}')
print('    b/a = ',b/a)
print('    (b/a).len() = ', (b/a).len())

print('\nFor regular number b:',b)
print('    Reciprocal of b: ', b.rec())
print('    Inverse of b: ', b.inv())
print('    a//b = ', a//b)

BabN.sep = '.'
print('\nFrom now on,  BabN.sep is ".", as in MesoCalc \
(http://baptiste.meles.free.fr/site/mesocalc.html)')
print('    a//b = ', a//b)
print('\nOther operations:')
print('    BabN(3)*(a+b)**2 // b = ',BabN(3)*(a+b)**2 // b)
print("    but you can mix operations with int's")
print('    3*(a+b)**2 // b = ',3*(a+b)**2 // b)
print(f'    BabN(2).sqrt() = {BabN(2).sqrt()}, BabN(2).sqrt()**2 = {BabN(2).sqrt()**2}')
print(f'    (BabN(2).sqrt()).dec/60.**5 = {(BabN(2).sqrt()).dec/60.**5}')
print(f'             Compare to sqrt(2) = {sqrt(2)}')

BabN.rdigits = 4
print('\nFrom now on, BabN.rdigits is:', BabN.rdigits)
print('    (30*BabN(2).sqrt()).float() = ',(30*BabN(2).sqrt()).float(),
        '\n        Compare to YBC 7289 (https://en.wikipedia.org/wiki/YBC_7289)\n')
print(f'    BabN(2).cbrt() = {BabN(2).cbrt()}, BabN(2).cbrt()**3 = {BabN(2).cbrt()**3}')

print('\nDatabase search for close regulars:')
print("a.searchreg('01:10','01:20',5,1)")
z = a.searchreg('01:10','01:20',5,1)
if z is not None:
    print(f'    its reciprocal is: {z.rec()}, compare to a.inv(): {a.inv()}')
