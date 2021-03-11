## Try/Except Block structure

#x = 'my message'

try:
    print(x)
except NameError:
    print('NameError exception')
except:
    print('Catch all exception')
else:
    print('You can use the else keyword to define a block of code to be executed if no errors were raised:')
finally:
    print('The finally block, if specified, will be executed regardless if the try block raises an error or not.')