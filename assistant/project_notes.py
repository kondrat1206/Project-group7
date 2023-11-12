import json
import os

class PersonalAssistant:
    def __init__(self):
        self.notes = []
        home_directory = os.path.expanduser("~")
        self.notes_filename = os.path.join(home_directory, "notes.json")

        # Load data from JSON files during initialization
        self.load_from_json()

        # Load saved notes
        self.load_data()

    def add_note(self, text, tags):
        note = {
            "text": text,
            "tags": tags
        }
        self.notes.append(note)
        print("\nNote successfully added.")
        self.save_notes()  # Save notes

    def list_notes(self):
        if self.notes:
            print("\nList of notes:")
            for idx, note in enumerate(self.notes, start=1):
                print(f"Note #{idx}:")
                print(f"Text: {note['text']}")
                print(f"Tags: {', '.join(note['tags'])}")
                print()
        else:
            print("You don't have any saved notes.")

    def search_notes(self, query):
        found_notes = []
        for note in self.notes:
            if query.lower() in note['text'].lower() or any(tag.lower() == query.lower() for tag in note['tags']):
                found_notes.append(note)

        if found_notes:
            print("\nFound notes:")
            for idx, note in enumerate(found_notes, start=1):
                print(f"Note #{idx}:")
                print(f"Text: {note['text']}")
                print(f"Tags: {', '.join(note['tags'])}")
                print()
        else:
            print("No notes found for the given query.")

    def edit_note(self, note_id, new_text, new_tags):
        if 1 <= note_id <= len(self.notes):
            note = self.notes[note_id - 1]
            note['text'] = new_text
            note['tags'] = new_tags
            print("Note successfully edited.")
            self.save_notes()  # Save notes
        else:
            print("Incorrect note number.")

    def delete_note(self, note_id):
        if 1 <= note_id <= len(self.notes):
            deleted_note = self.notes.pop(note_id - 1)
            print(f"Note #{note_id} successfully deleted:")
            print(f"Text: {deleted_note['text']}")
            print(f"Tags: {', '.join(deleted_note['tags'])}")
            self.save_notes()  # Save notes
        else:
            print("Incorrect note number.")

    def load_data(self):
        try:
            with open(self.notes_filename, "r") as notes_file:
                self.notes = json.load(notes_file)
        except FileNotFoundError:
            self.notes = []

    def save_data(self):
        self.save_notes()

    def save_notes(self):
        with open(self.notes_filename, "w") as notes_file:
            json.dump(self.notes, notes_file)

    def save_to_json(self):
        # Save data to JSON files
        with open(self.notes_filename, 'w') as notes_file:
            json.dump(self.notes, notes_file, indent=3)

    def load_from_json(self):
        # Load data from JSON files
        try:
            with open(self.notes_filename, 'r') as notes_file:
                self.notes = json.load(notes_file)
        except FileNotFoundError:
            print(f"File '{self.notes_filename}' not found. A new file will be created.")
