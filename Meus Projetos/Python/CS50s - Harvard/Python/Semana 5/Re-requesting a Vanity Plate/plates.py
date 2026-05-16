def main():
    plate = input("Plate: ")
    if is_valid(plate):
        print("Valid")
    else:
        print("Invalid")

def is_valid(s):
    if not (2 <= len(s) <= 6):
        return False
    if not s[0:2].isalpha():
        return False
    found_digit = False
    for char in s:
        if char.isdigit():
            if not found_digit and char == '0':
                return False
            found_digit = True
        elif char.isalpha():
            if found_digit:
                return False
    if not s.isalnum():
        return False
    return True

if __name__ == "__main__":
    main()