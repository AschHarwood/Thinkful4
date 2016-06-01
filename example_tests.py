import unittest

class ExampleTests(unittest.TestCase):
	fizzbuzz_goodtest(f)

if _name_ == "_main_":
	unittest.main()

def fizzbuzz_goodtest(f):#defines function that takes another function
    output = [] #create a list
    for n in range(100): #creates a set of 0 - 99 to test with
        output.append(str(f(n) + '\n')) #runs n through fizzbuzz function
        
    expected = open('fizzbuzz-output.txt', 'r') #opens a file with expected behavior
    i = 0 
    for line in expected:#for loop checking each line in file
        if line == output[i]: checks the value against the expected out
            print('success!') 
            i += 1
        else:
            print('nope. try again.')