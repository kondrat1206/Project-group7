from prompt_toolkit import prompt
from assistant.classes import AddressBook, Record, Name, Phone, Birthday, MyCompleter
import functools
import pickle
import os
from assistant.sortfolder import check_args, list_files_recursive, sort, unpack_archives, normalize, remove_empty_directories, library
from assistant.project_notes import PersonalAssistant
import re

help = """
Available commands:
hello: print \"How can I help you?\"
add [name] [phone] [birthday]: Add a new record to address book or new phone to contact phone list
add birthday [name] [birthday]: Add a new/change Birthday to the contact of address book
add email [name] [email]: Add email to the contact of address book
add address [name] [email]: Add address to the contact of address book
remove [name]: Remove contact from address book
to birthday [name]: Show days to contact`s Birthday
change [name] [old_phone] [new_phone]: Change phone num for contact in address book
change email [name] [new email]: Change email for contact in address book
change address [name] [new address]: Change address for contact in address book
phone [name]: Show phone list of contact
show all: Show address book
pages [size]: Show address book in pages, size is number records per page
search [string]: Matching search for name or phone in address book
sort folder [path to folder]: Sort files depends extensions into the target folder
notes []: module for notes use
celebrators [days to celebrate]: Show users with birthday less then set days
good bye, close, exit: print \"Good bye!\" and exit
help: Show this help
"""

home_directory = os.path.expanduser("~")
data_file = os.path.join(home_directory, "address_book.bin")

def save_data():

    with open(data_file, "wb") as file:
        pickle.dump(address_book, file)


def load_data():
    with open(data_file, 'rb') as file:
        address_book = pickle.load(file)

    return address_book


if os.path.exists(data_file):
    address_book = load_data()
    print("Loaded address book from file")
else:
    address_book = AddressBook()
    print("Not found address book. Created new Instance")




def input_error(func):

    @functools.wraps(func)
    def inner(param_list):

        if func.__name__ == "phone" or func.__name__ == "remove_contact":
            if len(param_list) > 0:
                result = func(param_list)
            else:
                result = f"""Command \"{func.__name__.replace("_contact", "")}\" reqired 1 argument: name.\nFor example: {func.__name__.replace("_contact", "")} [name]\n\nTRY AGAIN!!!"""
        elif func.__name__ == "celebrators":
            if len(param_list) > 0:
                result = func(param_list)
            else:
                result = f"""Command \"{func.__name__}\" reqired 1 argument: days to birthday.\nFor example: {func.__name__} [days to birthday]\n\nTRY AGAIN!!!"""
        elif func.__name__ == "add":
            if len(param_list) > 0:
                result = func(param_list)
            else:
                result = f"""Command \"{func.__name__}\" reqired 1 or 2 arguments: name and phone.\nFor example: {func.__name__} [name] - To add a new contact without phones\nFor example: {func.__name__} [name] [phone] - To add a new contact with phones, or add new phone to contact\n\nTRY AGAIN!!!"""
        elif func.__name__ == "add_birthday":
            param_list.pop(0)
            if len(param_list) > 1:
                result = func(param_list)
            else:
                result = f"""Command \"{func.__name__.replace("_", " ")}\" reqired 2 arguments: name and birthday.\nFor example: {func.__name__.replace("_", " ")} [name] [birthday]\n\nTRY AGAIN!!!"""

        elif func.__name__ == "add_email" or func.__name__ == "change_email":
            param_list.pop(0)
            if len(param_list) > 1:
                result = func(param_list)
            else:
                result = f"""Command \"{func.__name__.replace("_", " ")}\" reqired 2 arguments: name and email.\nFor example: {func.__name__.replace("_", " ")} [name] [email]\n\nTRY AGAIN!!!"""

        elif func.__name__ == "add_address" or func.__name__ == "change_address":
            param_list.pop(0)
            if len(param_list) > 1:
                result = func(param_list)
            else:
                result = f"""Command \"{func.__name__.replace("_", " ")}\" reqired 2 arguments: name and address.\nFor example: {func.__name__.replace("_", " ")} [name] [address]\n\nTRY AGAIN!!!"""

        elif func.__name__ == "change":
            if len(param_list) > 2:
                result = func(param_list)
            else:
                result = f"""Command \"{func.__name__}\" reqired 3 arguments: name, phone and new_phone.\nFor example: {func.__name__} [name] [phone] [new_phone]\n\nTRY AGAIN!!!"""
        elif func.__name__ == "to_birthday":
            param_list.pop(0)
            if len(param_list) > 0:
                result = func(param_list)
            else:
                result = f"""Command \"{func.__name__.replace("_", " ")}\" reqired 1 argument: name.\nFor example: {func.__name__.replace("_", " ")} [name]\n\nTRY AGAIN!!!"""
        elif func.__name__ == "pages":
            if len(param_list) > 0 and int(param_list[0]) > 0:
                result = func(param_list)
            else:
                result = f"""Command \"{func.__name__}\" reqired 1 argument: size. Size int and must be > 0.\nFor example: {func.__name__} [size]\n\nTRY AGAIN!!!"""
        elif func.__name__ == "search":
            if len(param_list) > 0:
                result = func(param_list)
            else:
                result = f"""Command \"{func.__name__}\" reqired 1 argument: search string. \nFor example: {func.__name__} [string]\n\nTRY AGAIN!!!"""
        elif func.__name__ == "sort_folder":
            param_list.pop(0)
            if len(param_list) > 0:
                result = func(param_list)
            else:
                result = f"""Command \"{func.__name__}\" reqired 1 argument: path to target folder. \nFor example: {func.__name__} [path]\n\nTRY AGAIN!!!"""

        return result
    return inner


@input_error
def add(param_list):

    name = Name(None)
    phone = Phone(None)
    birthday = Birthday(None)

    if len(param_list) == 1:
        try:
            name.value = param_list[0]
        except ValueError as e:
            result = str(e)
            return result
    elif len(param_list) == 2:
        try:
            name.value = param_list[0]
        except ValueError as e:
            result = str(e)
            return result
        try:
            phone.value = param_list[1]
        except ValueError as e:
            result = str(e)
            return result
    elif len(param_list) > 2:
        try:
            name.value = param_list[0]
        except ValueError as e:
            result = str(e)
            return result
        try:
            phone.value = param_list[1]
        except ValueError as e:
            result = str(e)
            return result
        try:
            birthday.value = param_list[2]
        except ValueError as e:
            result = str(e)
            return result

    if phone.value != None:
        result = address_book.add_record(
            Record(name, phone=phone, birthday=birthday))
    else:
        result = address_book.add_record(Record(name, birthday=birthday))

    return result


@input_error
def add_birthday(param_list):

    name = Name(None)
    birthday = Birthday(None)
    record = Record(Name(param_list[0]))
    if address_book.is_contact_exist(record):
        try:
            name.value = param_list[0]
        except ValueError as e:
            result = str(e)
            return result
        try:
            birthday.value = param_list[1]
        except ValueError as e:
            result = str(e)
            return result

        result = address_book[param_list[0]].add_birthday(birthday)
    else:
        result = f"Contact \"{param_list[0]}\" does not exist in the address book\n"

    return result


@input_error
def change(param_list):

    record = Record(Name(param_list[0]))
    old_phone_obj = Phone(param_list[1])
    new_phone_obj = Phone(None)
    try:
        new_phone_obj.value = param_list[2]
    except ValueError as e:
        result = str(e)
        return result

    if address_book.is_contact_exist(record):
        result = address_book[param_list[0]].change_phone(
            old_phone_obj, new_phone_obj)
    else:
        result = f"Contact \"{param_list[0]}\" does not exist in the address book\n"

    return result


@input_error
def phone(param_list):

    name = param_list[0]
    record = Record(Name(param_list[0]), None)
    if address_book.is_contact_exist(record):
        phone_list = address_book[name].phones
        value_list = []
        for phone_obj in phone_list:
            value_list.append(phone_obj.value)
        result = f"Phone list of contact \"{name}\" is \"{value_list}\"\n"
    else:
        result = f"Contact \"{name}\" does not exist in the address book\n"

    return result


@input_error
def to_birthday(param_list):

    record = Record(Name(param_list[0]))
    if address_book.is_contact_exist(record):
        result = address_book[param_list[0]].days_to_birthday()
    else:
        result = f"Contact \"{param_list[0]}\" does not exist in the address book\n"

    return result


def hello(param_list):

    result = "How can I help you?\n"
    return result


def exit(param_list):

    result = "exit"
    return result


def show_all(param_list):

    result = "All contacts:\n"
    for name, record in address_book.data.items():
        phones = record.phones
        birthday = record.birthday.value
        phone_values = []
        email = record.email
        address = record.home_address
        for phone in phones:
            phone_values.append(phone.value)
        result += f"Name: \"{name}\", Phones: {phone_values}, Birthday: [{birthday}], Email: [{email}], , Home address: [{address}]\n"

    return result


@input_error
def pages(param_list):
    size = int(param_list[0])
    result = address_book.get_pages(page_size=size)

    return result


@input_error
def search(param_list):

    result = "Finded contacts:\n"
    search_string = param_list[0]
    for key, value in address_book.data.items():
        first_string = f"{key}"
        phones_string = ""
        phone_values = []
        for phone in value.phones:
            phones_string = phones_string + str(phone.value)
            phone_values.append(phone.value)
        full_string = first_string + phones_string
        if search_string in full_string:
            result += f"Name: \"{key}\", Phones: {phone_values}, Birthday: [{value.birthday.value}]\n"

    return result


def helper(param_list):

    return help


@input_error
def sort_folder(param_list):
    path = param_list[0]
    real_path = check_args(path)
    new_dir = real_path
    
    list_files = list_files_recursive(real_path)
    for file in list_files:
        filename = file.split("/")[-1]  # Получаем имя файла с расширением
        extension = file.split(".")[-1]  # Получаем расширение файла
        sort(library, extension, file, new_dir)
    print('Файлы отсортированы')

    archive_dir = f'{real_path}/archives'
    if os.path.exists(archive_dir):
        print('Обнаружены архивы, приступаем к распаковке')

        unpack_archives(library, archive_dir)
        print("Архивы распакованы, их содержимое отсортировано")
    else:
        print('Архивы не обнаружены')

    normalize(new_dir)
    print('Имена файлов, за исключением неизвестных типов и распакованных архивов - нормализованы. Завершение работы')

    remove_empty_directories(new_dir)
    print(f'Ваши файлы отсортированы в директории {new_dir}, пустые папки удалены')


def notes (param_list):
    
    assistant = PersonalAssistant()
    while True:
        print("Select an option:")
        print("1. Add note")
        print("2. List of notes")
        print("3. Find note")
        print("4. Edit note")
        print("5. Delete note")
        print("0. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == "1":
            text = input("Input text of note: ")
            tags = input("Input tags (use ','): ").split(",")
            assistant.add_note(text, [tag.strip() for tag in tags])
        elif choice == "2":
            assistant.list_notes()
        elif choice == "3":
            query = input("Enter a query to search for notes: ")
            assistant.search_notes(query)
        elif choice == "4":
            note_id = int(input("Enter the note number you want to edit: "))
            new_text = input("New note text: ")
            new_tags = input("New tags (separated by commas): ").split(",")
            assistant.edit_note(note_id, new_text, [tag.strip() for tag in new_tags])
        elif choice == "5":
            note_id = int(input("Enter the note number you want to delete: "))
            assistant.delete_note(note_id)
        elif choice == "0":
            assistant.save_to_json()
            break
        else:
            print("Incorrect choice. Please try again.")

    return "Exited from notes \n"


@input_error
def celebrators(param_list):

    result = "Finded celebrators:\n"
    for record in address_book.data.values():
        text = record.days_to_birthday()
        days_left = extract_info(text)
        if days_left[1] != None and  int(days_left[1]) <= int(param_list[0]):
            result += f"For contact: \"{days_left[0]}\", left {days_left[1]} days to celebrate. Birthday: [{record.birthday.value}]\n"
            #print(days_left[0], days_left[1], param_list[0])

    return result
        


def extract_info(text):

    match = re.search(r'contact "(.*?)"(?: untill "(.*?)")? days', text)
    if match:
        name = match.group(1)
        days = match.group(2)
        return (name, int(days) if days else None)
    else:
        match = re.search(r'contact "(.*?)"', text)
        if match:
            name = match.group(1)
            return (name, None)
    return None


@input_error
def remove_contact(param_list):

    if param_list[0] in address_book.data:
        address_book.remove_record(param_list[0])
        result = f"Contact \"{param_list[0]}\" removed from address book"
    else:
        result = f"Contact \"{param_list[0]}\" does not exist in address book"

    return result


@input_error
def add_email(param_list):

    if param_list[0] in address_book.data:
        result = address_book[param_list[0]].add_email(param_list[1])
    else:
        result = f"Contact \"{param_list[0]}\" does not exist in address book"

    return result


@input_error
def add_address(param_list):

    if param_list[0] in address_book.data:
        address_book[param_list[0]].add_home_address(' '.join(param_list[1:]))
        result = f"For contact \"{param_list[0]}\" added new address \"{' '.join(param_list[1:])}\""
    else:
        result = f"Contact \"{param_list[0]}\" does not exist in address book"

    return result


@input_error
def change_email(param_list):

    if param_list[0] in address_book.data:
        result = address_book[param_list[0]].change_email(param_list[1])
        
    else:
        result = f"Contact \"{param_list[0]}\" does not exist in address book"

    return result


@input_error
def change_address(param_list):

    if param_list[0] in address_book.data:
        address_book[param_list[0]].add_home_address(' '.join(param_list[1:]))
        result = f"For contact \"{param_list[0]}\" address changed to \"{' '.join(param_list[1:])}\""
    else:
        result = f"Contact \"{param_list[0]}\" does not exist in address book"

    return result

    


commands = {
    "good bye": exit,
    "close": exit,
    "exit": exit,
    "show all": show_all,
    "show_all": show_all,
    "hello": hello,
    "add birthday": add_birthday,
    "add_birthday": add_birthday,
    "add email": add_email,
    "add_email": add_email,
    "add address": add_address,
    "add_address": add_address,
    "change email": change_email,
    "change_email": change_email,
    "change address": change_address,
    "change_address": change_address,
    "add": add,
    "change": change,
    "phone": phone,
    "to birthday": to_birthday,
    "to_birthday": to_birthday,
    "help": helper,
    "helper": helper,
    "pages": pages,
    "search": search,
    "sort folder": sort_folder,
    "sort_folder": sort_folder,
    "notes": notes,
    "celebrators": celebrators,
    "remove": remove_contact,
    "remove_contact": remove_contact
}


def parser(string: str):

    lower_string = string.lower()
    for keyword, command in commands.items():
        if keyword in lower_string:
            param_list = string.split()
            for param in param_list:
                if param.lower() in keyword:
                    param_list.remove(param)
                    command = command.__name__
            return command, param_list

    return None, ""


def handler(command):

    return commands[command]


def main():

    while True:
        source_command = prompt("Enter command: ", completer=MyCompleter(address_book, commands))
        command, param_list = parser(source_command)
        if not command:
            print(f"YOU ENTERED A WRONG COMMAND!!!\n{help}\nTRY AGAIN!!!")
            continue
        result = handler(command)(param_list)
        if result == 'exit':
            print("Good bye!")
            break
        else:
            print(result)
            save_data()


if __name__ == "__main__":

    main()
