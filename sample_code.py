def calculate_sum(numbers):
    total = 0
    for i in numbers:
        total = total + i
    return total

def multiply(a, b):
    result = a * b
    return result

x = calculate_sum([1, 2, 3, 4, 5])
y = multiply(5, 10)
print(x)
print(y)