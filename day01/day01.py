import re
import inflect

infile = "data/data.txt"

with open(infile) as f:
    indata = f.readlines()

indata = [i.strip() for i in indata]
indata = [i for i in indata if len(i) > 0]


digits = range(1, 10)

ie = inflect.engine()
digit_lookup = {}
for d in digits:
    digit_lookup[str(d)] = ie.number_to_words(d)


def replace_to_digits(my_str, my_dict):
    for key, value in my_dict.items():
        my_str = my_str.replace(value, key)

    return my_str


def extract_numbers(indata, withwords=False):
    numbers_out = []
    if withwords:
        digit_string = "one|two|three|four|five|six|seven|eight|nine"
        re_first_digit = r"^[^\d]*?(\d|" + digit_string + ")"
        # Reverse the numbers as words
        re_last_digit = r"^[^\d]*?(\d|" + digit_string[::-1] + ")"
    else:
        re_first_digit = r"^[^\d]*?(\d)"
        re_last_digit = re_first_digit 
        
    for i in indata:
        first = re.match(re_first_digit, i)[1]
        last = re.match(re_last_digit, i[::-1])[1][::-1]
        numbers_out.append(
            replace_to_digits(first, digit_lookup)
            + replace_to_digits(last, digit_lookup)
        )

    return numbers_out


print("part1")
print(sum([int(i) for i in extract_numbers(indata)]))

print("part2")
print(sum([int(i) for i in extract_numbers(indata, withwords=True)]))
