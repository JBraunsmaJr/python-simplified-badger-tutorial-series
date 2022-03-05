from collections.abc import Iterable


def is_valid_age(number: int) -> bool:
    return 0 < number <= 130


def get_user_input(message: str,
                   expect: type = str,
                   error_message: str = None,
                   predicate=None,
                   predicate_error_message: str = None):
    while True:
        user_input = input(message)
        try:
            user_input = expect(user_input)

            if predicate is not None:
                if not callable(predicate):
                    raise AssertionError("predicate must be callable")

                if predicate(user_input):
                    return user_input
                else:
                    if predicate_error_message is None:
                        print(f"Input does not meet criteria")
                    else:
                        print(predicate_error_message)
                    continue
            return user_input
        except ValueError:
            if error_message is None:
                print(f"Invalid data was given. Expected a {expect.__name__}")
            else:
                print(error_message)


def select_from_list(message: str, title: str, data: list, error_message: str = None, start_at_zero: bool = False):
    if not isinstance(data, Iterable):
        raise AssertionError("Must provide a valid collection")

    output: str = f"{title}\n"
    count = 0 if start_at_zero else 1

    for item in data:
        output += f"\t[{count}]\t{item}\n"
        count += 1

    output += "\n"
    output += message

    if start_at_zero:
        start = 0
        end = len(data) - 1
    else:
        start = 1
        end = len(data)

    selected = get_user_input(output, int,
                              predicate=lambda x: start <= x <= end,
                              error_message=error_message,
                              predicate_error_message=f"Please select a number between {start} - {end}")
    return data[selected if start_at_zero else selected - 1]


market = ["Sword", "Shield", "Bow", "Health Potion"]

username = get_user_input("Welcome traveler! What's your name? ")
age = get_user_input(f"Hello there, {username}! How old are you? ", int,
                     predicate=is_valid_age,
                     predicate_error_message="Please provide a number between 1 and 130!")

purchase_item = select_from_list("Welcome to my shop! What would you like to buy? ",
                                 data=market,
                                 title="Shop Goods")

print(f"You have acquired a {purchase_item}")