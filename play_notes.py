from project_notes import PersonalAssistant


if __name__ == "__main__":
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