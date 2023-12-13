def divide(a, b):
    # Check if b is not zero to avoid division by zero
    if b != 0:
        result = a / b
        return result
    else:
        print("Error: Division by zero is undefined.")
        return None
