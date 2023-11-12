# Address Book CLI Application

This is a command-line interface (CLI) application for managing an address book. The application allows you to add, edit, and view contacts along with their phone numbers and birthdays.

## Available Commands:

- **hello**: Print "How can I help you?"

- **add [name] [phone] [birthday]**: Add a new record to the address book or a new phone to a contact's phone list. Provide the contact's name, phone number, and an optional birthday in the format 'YYYY-MM-DD'.

- **add birthday [name] [birthday]**: Add a new or change the birthday of a contact in the address book. Provide the contact's name and the birthday in the format 'YYYY-MM-DD'.

- **to birthday [name]**: Show the number of days until the contact's birthday.

- **change [name] [old_phone] [new_phone]**: Change the phone number for a contact in the address book. Provide the contact's name, the old phone number, and the new phone number.

- **add email [name] [email]**: Add email to the contact of address book

- **add address [name] [email]: Add address to the contact of address book**: Add email to the contact of address book

- **phone [name]**: Show the phone list of a contact.

- **show all**: Show the entire address book.

- **pages [size]**: Show the address book in pages, where the size is the number of records per page.

- **search [string]**: Perform a matching search for a name or phone number in the address book.

- **remove [name]**: Delete a contact from the address book. Provide the contact's name to be removed.

- **celebrators [days to celebrate]**: View a list of upcoming celebrators.

- **notes [name] [note]**: Add a note to a contact in the address book. Provide the contact's name and the note.

- **show notes [name]**: Show notes for a specific contact.

- **good bye, close, exit**: Print "Good bye!" and exit the application.

- **help**: Show this help message.

## Usage:

1. Run the application by executing the script.

2. Enter commands as described above.

3. Type 'exit' to end the application.

Enjoy managing your address book through the command line!
