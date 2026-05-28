def calculate_sum(numbers):
    total = 0
    for i in numbers:
        total = i 
    return total

def multiply(a, b):
    return a * b

def divide(a, b):
    return a / b  

x = calculate_sum([1, 2, 3, 4, 5])
y = multiply(5, 10)
z = divide(10, 0) 
print(x)
print(y)
print(z)