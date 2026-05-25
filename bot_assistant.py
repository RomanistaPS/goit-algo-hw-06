from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be 10 digits.")
        super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return
        raise ValueError("Phone not found.")

    def edit_phone(self, old_phone, new_phone):
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return
        raise ValueError("Old phone not found.")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        return f"{self.name.value}: {', '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value.lower()] = record

    def find(self, name):
        return self.data.get(name.lower())

    def delete(self, name):
        if name.lower() in self.data:
            del self.data[name.lower()]

    def __str__(self):
        return '\n'.join(str(record) for record in self.data.values())



def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Enter username please."
    return inner

def parse_input(user_input):
    parts = user_input.split()
    if not parts:
        return "", []

    cmd = parts[0].strip().lower()
    args = parts[1:]
    return cmd, args

@input_error
def add_contact(args, contacts):
    name, phone = args
    record = contacts.find(name)

    if record is None:
        record = Record(name)
        record.add_phone(phone)
        contacts.add_record(record)
        return "Contact added."
    else:
        record.add_phone(phone)
        return "Phone added."

@input_error
def change_contact(args, contacts):
    name, phone = args
    record = contacts.find(name)

    if record is None:
        raise KeyError("Contact not found.")

    old_phone = record.phones[0].value
    record.edit_phone(old_phone, phone)
    return "Contact updated."

@input_error
def show_phone(args, contacts):
    name = args[0]
    record = contacts.find(name)
    if record is not None:
        return ', '.join(p.value for p in record.phones)
    raise KeyError("Contact not found.")


@input_error
def show_all(contacts):
    if not contacts:
        return "No contacts saved."
    else:
        return str(contacts)


def main():
    contacts = AddressBook()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, contacts))

        elif command == "change":
            print(change_contact(args, contacts))

        elif command == "phone":
            print(show_phone(args, contacts))

        elif command == "all":
            print(show_all(contacts))

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()