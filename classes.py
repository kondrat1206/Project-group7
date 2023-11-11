from prompt_toolkit.completion import PathCompleter, Completer, Completion
from collections import UserDict
from datetime import datetime, date
import re
import os




class AddressBook(UserDict):

    def __init__(self):

        self.data = {}
        self.current_page = 0
        self.page_size = 0


    def set_page_size(self, page_size):

        self.page_size = page_size


    def __iter__(self):

        self.current_page = 0
        
        return self
    

    def __next__(self):
        
        start_idx = self.current_page * self.page_size
        end_idx = (self.current_page + 1) * self.page_size
        items = list(self.data.items())

        if start_idx >= len(items):
            raise StopIteration

        self.current_page += 1

        return items[start_idx:end_idx]
    

    def get_pages(self, page_size=100):

        self.page_size = page_size
        self.set_page_size(self.page_size)

        for page in self:
            phone_list = []
            print(f"---------------PAGE-{self.current_page}---------------------")
            for el in page:
                for i in el[1].phones:
                    phone_list.append(i.value)
                print(f"Name: {el[0]} Phones: {phone_list} Birthday: [{el[1].birthday.value}]")
            print(f"---------------END-PAGE-{self.current_page}-----------------")

        return "Completed"


    def is_contact_exist(self, record):

        keys = []
        for key in self.data.keys():
            keys.append(key)
        if record.name.value in keys:
            result = True
        else:
            result = False
            
        return result
    

    def is_phone_exist(self, record):

        num_values = []
        for  i in self.data[record.name.value].phones:
            num_values.append(i.value)
        if record.phones[0].value in num_values:
            result = True
        else:
            result = False

        return result


    def add_record(self, record):

        if len(record.phones) < 1:
            if self.is_contact_exist(record) == False:
                self.record = record
                self.data[self.record.name.value] = self.record
                result = f"Contact \"{record.name.value}\" added to address book without phone\n"
            else:
                result = f"Contact \"{record.name.value}\" already exists in address book\n"
        else:
            if self.is_contact_exist(record) == False:
                self.record = record
                self.data[self.record.name.value] = self.record
                result = f"Contact \"{record.name.value}\" added to address book with phone \"{record.phones[0].value}\"\n"
            else:
                if self.is_phone_exist(record):
                    result = f"Phone \"{record.phones[0].value}\" already exists into the contact \"{record.name.value}\"\n"
                else:
                    self.data[self.record.name.value].add_phone(record.phones[0])
                    result = f"Added new phone \"{record.phones[0].value}\" to contact \"{record.name.value}\"\n"

        return result


class Record:

    def __init__(self, name, phone=None, birthday=None): 

        self.name = name
        self.birthday = birthday
        self.phones = []
        if phone != None:
            self.phones.append(phone)

    
    def add_phone(self, phone):

        self.phones.append(phone)
        result = f'Number \"{phone.value}\" added to phone list of \"{self.name.value}\"\n'

        return result
    

    def add_birthday(self, birthday):

        self.birthday.value = birthday.value
        result = f'Value \"{self.birthday.value}\" added to birthday of \"{self.name.value}\"\n'

        return result


    def remove_phone(self, phone):
        
        phone_num = phone.value
        for id, obj in enumerate(self.phones):
            if obj == phone:
                self.phones.pop(id)
                result = f'Number {phone_num} remuved from phone list of {self.name.value}'
                break
                
        return result
    

    def change_phone(self, old_phone, new_phone):

        phone_values = []
        for number in self.phones:
            phone_values.append(number.value)
        if old_phone.value in phone_values:
            for index, obj in enumerate(self.phones):
                if obj.value == old_phone.value:
                    self.phones[index] = new_phone
                    break
            result = f"Number \"{old_phone.value}\" changed to \"{new_phone.value}\" in phone list of \"{self.name.value}\"\n"
        else:
            result = f"Phone \"{old_phone.value}\" does not exist in the phone list of contact \"{self.name.value}\"\n"
                   
        return result
    

    def days_to_birthday(self):

        if self.birthday.value == None:
            result = f"Birthday value not set of contact \"{self.name.value}\"\nYou can set the Birthday with command:\nadd birthday {self.name.value} DD.MM.YYYY\n"
        else:
            now = date.today()
            birthday = datetime.strptime(self.birthday.value, "%d.%m.%Y").date()
            if now.month > birthday.month or (now.month == birthday.month and now.day >= birthday.day):
                next_birthday = date(now.year + 1, birthday.month, birthday.day)
            else:
                next_birthday = date(now.year, birthday.month, birthday.day)

            days = (next_birthday - now).days
            result = f"To Birthday of contact \"{self.name.value}\" untill \"{days}\" days\n"

        return result


class Field:
    
    def __init__(self, value):

        self.__value = value

    @property
    def value(self):

        return self.__value

    
    @value.setter
    def value(self, value):
        check = self.check_value(value)
        if check == True:
            self.__value = value
        else:
            raise ValueError(check)
        
    
class Name(Field):

    def check_value(self, value):
       
        return True
    

class Phone(Field):

    def check_value(self, value):
        match = re.fullmatch(r'\+\d{12}', value)
        if match:
            result = True
        else:
            result =  f"""Entered value \"{value}\" is not correct.\nPhone must start with \"+\" and must have 12 digits.\nFor example: \"+380681235566\"\n\nTRY AGAIN!!!"""
       
        return result
    

class Birthday(Field):

    def check_value(self, value):

        match = re.fullmatch(r'\d{2}\.\d{2}\.\d{4}', value)
        if match:
            result = True
        else:
            result =  f"""Entered value \"{value}\" is not correct.\nBirthday must have a format: DD.MM.YYYY and contain only numbers\nFor example: \"12.06.1978\"\n\nTRY AGAIN!!!"""
        
        day, month, year = map(int, value.split('.'))
        try:
            datetime(year, month, day)
        except ValueError:
            result = f"""Entered value \"{value}\" is not correct.\nSetted date is not exist\n\nTRY AGAIN!!!"""

        current_date = datetime.now().date()
        if datetime(year, month, day).date() > current_date:
            result = f"""Entered value \"{value}\" is not correct.\nSetted date can not be at the future\n\nTRY AGAIN!!!"""
        
        return result
    

class MyCompleter(Completer):

    def __init__(self, address_book):
        self.address_book = address_book
        self.path_completer = PathCompleter()
        
    
    def get_completions(self, document, complete_event):

        commands_list = ['good bye', 'close', 'exit', 'show all', 'hello', 'add birthday', 'add', 'change', 'phone', 'to birthday', 'help', 'pages', 'search', 'sort folder', 'notes', 'celebrators']
        users = list(self.address_book.data.keys())
        text = document.text
        completions = []
        for command in commands_list:
            if text in command:  
                completions = [c for c in commands_list if text in c]
                
            elif text.startswith('add birthday'):
                completions = [text.rsplit(' ', 1)[0]+' '+u for u in users if text.split(' ', -1)[-1] in u]
                if text.count(' ') == 3:
                    completions = [text.rsplit(' ', 1)[0]+' '+'[dd.mm.yyyy]']
                
            elif text.startswith('add'):
                completions = [text.rsplit(' ', 1)[0]+' '+'[name]'+'[phone]'+'[birthday]']
                
            elif text.startswith('change'):
                completions = [text.rsplit(' ', 1)[0]+' '+u for u in users if text.split(' ', -1)[-1] in u]
                if text.count(' ') == 2:
                    phone_list = self.address_book[text.split()[1]].phones
                    value_list = []
                    for phone_obj in phone_list:
                        value_list.append(phone_obj.value)
                    completions = [text.rsplit(' ', 1)[0]+' '+v for v in value_list if text.split(' ', -1)[-1] in v]
                if text.count(' ') == 3:
                    completions = [text.rsplit(' ', 1)[0]+' '+'[new phone]']

            elif text.startswith('phone'):
                completions = [text.rsplit(' ', 1)[0]+' '+u for u in users if text.split(' ', -1)[-1] in u]
                if text.count(' ') == 2:
                    completions = []

            elif text.startswith('to birthday'):
                completions = [text.rsplit(' ', 1)[0]+' '+u for u in users if text.split(' ', -1)[-1] in u]
                if text.count(' ') == 3:
                    completions = []

            elif text.startswith('celebrators'):
                completions = [text.rsplit(' ', 1)[0]+' '+'[days to birthday]']
                if text.count(' ') == 2:
                    completions = []
                
            elif text.startswith('pages'):
                completions = [text.rsplit(' ', 1)[0]+' '+'[size]']

            elif text.startswith('search'):
                completions = [text.rsplit(' ', 1)[0]+' '+'[string]']

        if text.startswith('sort folder'):
            # Получить путь к папке из введенной строки
            folder_path = text[len('sort folder'):].strip()
            #print(f"PATH: '{folder_path}'")

            # Проверить, существует ли указанная папка
            if os.path.exists(folder_path) and os.path.isdir(folder_path):
                # Получить список файлов и папок в указанной директории
                path_completions = os.listdir(folder_path)
                #completions.extend(path_completions)
                completions = [text.rsplit(' ', 1)[0]+' '+text.split(' ', -1)[-1]+p for p in path_completions]
                

                
        for completion in completions:
            yield Completion(completion, start_position=-len(text))