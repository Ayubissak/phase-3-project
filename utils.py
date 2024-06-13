# from tabulate import tabulate

# def display_table(data, headers):
#     print(tabulate(data, headers=headers, tablefmt='grid'))

def get_input(prompt, type_=str, validation=None):
    while True:
        try:
            value = type_(input(prompt))
            if validation and not validation(value):
                raise ValueError("Invalid value.")
            return value
        except ValueError as e:
            print(e)
