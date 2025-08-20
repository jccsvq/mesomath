from mesomath.babn import BabN

# Creating instances
a = BabN('1.12.23')
b = BabN(405)

print('\nSome basic tests of `BabN` class follow:')

print(f'\nA couple of BabN numbers: a: {a} and b: {b}')
print(f'    Are they regular? a: {a.isreg}, b: {b.isreg}')
print(f'    Factors a: {a.factors}, b: {b.factors}')

print('\nBasic operations with them:')
print('    a+b: ',a+b)
print('    a-b: ',a-b)
print('    a*b: ',a*b)
print('    a**2: ',a**2)
print('    a**4: ',a**4)

print(f'\nApproximate inverse of a is: {a.inv()}\n    Testing: a*a.inv() = {a*(a.inv())}')
print(f'    Now using a.inv(8) we have: {a.inv(8)}\n    Testing: a*a.inv(8) = {a*(a.inv(8))}')
print('    b/a: ',b/a)
print('    (b/a).len() :', (b/a).len())

print('\nFor regular number b:',b)
print('    Reciprocal of b: ', b.rec())
print('    Inverse of b: ', b.inv())
print('    a//b: ', a//b)

BabN.sep = '.'
print('\nFrom now on,  BabN.sep is ".", as in MesoCalc')
print('    a//b: ', a//b)
print('\nOther operations:')
print('    BabN(3)*(a+b)**2 // b: ',BabN(3)*(a+b)**2 // b)
print(f'    BabN(2).sqrt(): {BabN(2).sqrt()}, BabN(2).sqrt()**2: {BabN(2).sqrt()**2}')

BabN.rdigits = 4
print('\nFrom now on, BabN.rdigits is:', BabN.rdigits)
print('    (BabN(30)*BabN(2).sqrt()).float() = ',(BabN(30)*BabN(2).sqrt()).float(),
        '\n        Compare to YBC 7289 (https://en.wikipedia.org/wiki/YBC_7289)\n')
print(f'    BabN(2).cbrt(): {BabN(2).cbrt()}, BabN(2).cbrt()**3: {BabN(2).cbrt()**3}')

print('\nDatabase search for close regulars:')
print("a.searchreg('01:10','01:20',5,1)")
z = a.searchreg('01:10','01:20',5,1)
print(f'    its reciprocal: {z.rec()}, compare to a.inv(): {a.inv()}')
