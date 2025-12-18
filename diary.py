"""
Diary Management System
Author: Tanmay Vijay Sherkar
Date: December 2025
Description: A Python-based diary system created as part of my case study.
"""
import json
import os
entries = []

def diary_menu():
    print("\n ==========DIARY MANGEMENT MENU==========")
    print("1. Add New Entry")
    print("2. View All Entry")
    print("3. Search Entry")
    print("4. Update Entry")
    print("5. Delete Entry")
    print("6. View Statistics")
    print("7. Exit")

def add_record():
    print("\n -----ADD NEW ENTRY-----")
    date_str = input("Enter Date (YYYY-MM-DD): ")
    title = input("Enter Title: ")
    content = input("Enter the content: ")
    tags = input("Enter Tags (comma separated): ")
    mood = input("Enter Mood: ")
    
    if entries:
        new_id = max(entry['id'] for entry in entries) + 1
    else:
        new_id = 1
        
    new_entry = {
        'id': new_id,
        'date': date_str,
        'title': title,
        'content': content,
        'tags': tags,
        'mood': mood
    }
    
    entries.append(new_entry)
    save_data()
    print("Entry added successfully!")

def save_data():
    try:
        with open('diary.txt', 'w') as f:
            json.dump(entries, f, indent=4)
    except Exception as e:
        print(f"Error saving data: {e}")

def load_data():
    global entries
    if os.path.exists('diary.txt'):
        try:
            with open('diary.txt', 'r') as f:
                entries = json.load(f)
        except Exception as e:
            print(f"Error loading data: {e}")
            entries = []

def view_all_records():
    print("\n -----VIEW ALL ENTRIES-----")
    if not entries:
        print("No entries found!")
    else:
        for entry in entries:
            print(f"ID: {entry['id']}")
            print(f"Date: {entry['date']}")
            print(f"Title: {entry['title']}")
            print(f"Content: {entry['content']}")
            print(f"Tags: {entry.get('tags', 'N/A')}")
            print(f"Mood: {entry.get('mood', 'N/A')}")
            print("-" * 15)

def search_record():
    print("\n -----SEARCH ENTRIES-----")
    keyword = input("Enter keyword to search: ").lower()
    
    found_entries = [
        e for e in entries 
        if keyword in e['title'].lower() or 
           keyword in e['content'].lower() or 
           keyword in e['date'] or 
           keyword in e.get('tags', '').lower() or 
           keyword in e.get('mood', '').lower()
    ]
    
    if not found_entries:
        print("No entries found matching the keyword.")
    else:
        for entry in found_entries:
            print(f"\nID: {entry['id']}")
            print(f"Date: {entry['date']}")
            print(f"Title: {entry['title']}")
            print(f"Content: {entry['content']}")
            print(f"Tags: {entry.get('tags', 'N/A')}")
            print(f"Mood: {entry.get('mood', 'N/A')}")

def delete_record():
    view_all_records()
    print("\n -----DELETE ENTIRES-----")
    try:
        entry_id = int(input("Enter the entry ID you wish to delete: "))
        
        index_to_delete = None
        for i, entry in enumerate(entries):
            if entry['id'] == entry_id:
                index_to_delete = i
                break
        
        if index_to_delete is not None:
            entries.pop(index_to_delete)
            save_data()
            print(f"Entry {entry_id} deleted successfully!")
        else:
            print("Invalid entry ID.")
            
    except ValueError:
        print("Please enter a valid entry ID (integer).")

def update_record():
    view_all_records()
    print("\n -----UPDATE ENTRIES-----")
    try:
        entry_id = int(input("Enter the entry ID you wish to update: "))
        
        entry_found = False
        for entry in entries:
            if entry['id'] == entry_id:
                entry_found = True
                print(f"\nUpdating Entry {entry_id}:")
                
                new_date = input(f"Enter New Date (YYYY-MM-DD) [Current: {entry['date']}]: ")
                if new_date:
                    entry['date'] = new_date
                
                new_title = input(f"Enter New Title [Current: {entry['title']}]: ")
                if new_title:
                    entry['title'] = new_title
                
                new_content = input(f"Enter New Content [Current: {entry['content']}]: ")
                if new_content:
                    entry['content'] = new_content

                new_tags = input(f"Enter New Tags [Current: {entry.get('tags', '')}]: ")
                if new_tags:
                    entry['tags'] = new_tags

                new_mood = input(f"Enter New Mood [Current: {entry.get('mood', '')}]: ")
                if new_mood:
                    entry['mood'] = new_mood
                
                break
        
        if entry_found:
            save_data()
            print("Entry updated successfully!")
        else:
            print("Invalid entry ID.")
            
    except ValueError:
        print("Please enter a valid entry ID.")

def view_statistics():
    print("\n -----DIARY STATISTICS-----")
    if not entries:
        print("No entries available for statistics.")
        return

    total_entries = len(entries)
    
    from datetime import datetime
    current_month = datetime.now().strftime("%Y-%m")
    entries_this_month = sum(1 for e in entries if e['date'].startswith(current_month))
    
    total_words = sum(len(e['content'].split()) for e in entries)
    avg_length = total_words // total_entries if total_entries > 0 else 0

    all_tags = []
    for e in entries:
        tags = e.get('tags', '').split(',')
        all_tags.extend([t.strip() for t in tags if t.strip()])
    
    most_used_tag = "N/A"
    if all_tags:
        from collections import Counter
        tag_counts = Counter(all_tags)
        most_used_tag = f"{tag_counts.most_common(1)[0][0]} ({tag_counts.most_common(1)[0][1]} times)"
        
    moods = [e.get('mood', 'Unknown') for e in entries]
    from collections import Counter
    mood_counts = Counter(moods)

    print(f"Total Entries: {total_entries}")
    print(f"Entries This Month: {entries_this_month}")
    print(f"Average Entry Length: {avg_length} words")
    print(f"Most Used Tag: {most_used_tag}")
    print("Mood Distribution:")
    for mood, count in mood_counts.items():
        percentage = (count / total_entries) * 100
        print(f"- {mood}: {count} entries ({percentage:.0f}%)")

def main():
    load_data()
    while True:
        diary_menu()
        choice = input("Enter your choice (1-7): ")

        if choice == '1':
            add_record()
        elif choice == '2':
            view_all_records()
        elif choice == '3':
            search_record()
        elif choice == '4':
            update_record()
        elif choice == '5':
            delete_record()
        elif choice == '6':
            view_statistics()
        elif choice == '7':
            print("\n -----THANK YOU FOR USING THE DIARY MANAGEMENT SYSTEM-----")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
