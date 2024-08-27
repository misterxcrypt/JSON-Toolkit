import json
import csv

def add_serial_number(data):
    """Add serial numbers to each object in the JSON array."""
    for index, obj in enumerate(data):
        obj['no'] = index + 1
    return data

def delete_attribute(data, attribute):
    """Delete a specific attribute from each object in the JSON array."""
    for obj in data:
        if attribute in obj:
            del obj[attribute]
    return data

def count_objects(data):
    """Count the number of objects in the JSON array."""
    count = len(data)
    print(f"Total number of objects: {count}")

def collect_keys(data, attributes, output_format, output_file_prefix):
    """Collect all unique values of specific attributes and save them in the specified format."""
    all_keys = {}
    
    for attribute in attributes:
        keys = {obj.get(attribute) for obj in data if attribute in obj}
        all_keys[attribute] = keys
    
    if output_format == 'json':
        for attribute, keys in all_keys.items():
            with open(f"{output_file_prefix}_{attribute}.json", 'w', encoding='utf-8') as file:
                json.dump(list(keys), file, indent=4, ensure_ascii=False)
    elif output_format == 'csv':
        for attribute, keys in all_keys.items():
            with open(f"{output_file_prefix}_{attribute}.csv", 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([attribute])
                for key in keys:
                    writer.writerow([key])

def remove_duplicates(data):
    """Remove duplicate JSON objects based on the '_id' attribute."""
    seen_ids = set()
    unique_data = []
    for obj in data:
        obj_id = obj.get('_id')
        if obj_id not in seen_ids:
            seen_ids.add(obj_id)
            unique_data.append(obj)
    return unique_data

def keyword_matching(data, keywords_file=None):
    """Match keywords against JSON objects and provide stats."""
    keyword_counts = {}
    keyword_object_ids = {}

    # Load keywords from file or user input
    if keywords_file:
        with open(keywords_file, 'r', encoding='utf-8') as file:
            keywords = [line.strip() for line in file]
    else:
        keywords = input("Enter keywords separated by commas: ").strip().split(',')
        keywords = [keyword.strip() for keyword in keywords]

    for keyword in keywords:
        keyword_counts[keyword] = 0
        keyword_object_ids[keyword] = set()
    
    # Process each JSON object
    for obj in data:
        obj_text = json.dumps(obj, ensure_ascii=False).lower()
        obj_id = obj.get('_id')
        for keyword in keywords:
            keyword_lower = keyword.lower()
            count = obj_text.count(keyword_lower)
            if count > 0:
                keyword_counts[keyword] += count
                keyword_object_ids[keyword].add(obj_id)

    # Output matched JSON objects
    matched_data = [obj for obj in data if any(keyword.lower() in json.dumps(obj, ensure_ascii=False).lower() for keyword in keywords)]
    output_file = input("Enter the filename for the output JSON with matched keywords: ").strip()
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(matched_data, file, indent=4, ensure_ascii=False)
    count_objects(matched_data)

    # Output stats if requested
    stats_request = input("Do you want keyword matching stats? (yes/no): ").strip().lower()
    if stats_request == 'yes':
        stats_file = input("Enter the filename for the stats CSV file: ").strip()
        with open(stats_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Keyword', 'Count', 'Object IDs'])
            for keyword in keywords:
                count = keyword_counts[keyword]
                object_ids = list(keyword_object_ids[keyword])
                writer.writerow([keyword, count, json.dumps(object_ids)])

def main():
    # Load JSON data
    input_file = input("Enter the filename of the JSON file: ").strip()
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    while True:
        choice = input("Choose an action (1: Add Serial Number, 2: Delete Attribute, 3: Count Objects, 4: Collect Keys, 5: Remove Duplicates, 6: Keyword Matching, 0: Exit): ").strip()

        if choice == '1':
            data = add_serial_number(data)
            output_file = input("Enter the filename for the output JSON: ").strip()
            with open(output_file, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

        elif choice == '2':
            attribute = input("Enter the attribute name to delete: ").strip()
            data = delete_attribute(data, attribute)
            output_file = input("Enter the filename for the output JSON: ").strip()
            with open(output_file, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

        elif choice == '3':
            count_objects(data)

        elif choice == '4':
            attributes = input("Enter the attribute names to collect keys from, separated by commas: ").strip().split(',')
            attributes = [attr.strip() for attr in attributes]
            output_format = input("Do you want the output in JSON or CSV? (json/csv): ").strip().lower()
            output_file_prefix = input("Enter the prefix for the output files: ").strip()
            collect_keys(data, attributes, output_format, output_file_prefix)

        elif choice == '5':
            data = remove_duplicates(data)
            output_file = input("Enter the filename for the output JSON: ").strip()
            with open(output_file, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

        elif choice == '6':
            keyword_source = input("Do you want to provide keywords via a file or manually? (file/manual): ").strip().lower()
            keywords_file = None
            if keyword_source == 'file':
                keywords_file = input("Enter the filename for the keyword list file: ").strip()
            keyword_matching(data, keywords_file)

        elif choice == '0':
            print("Exiting the program.")
            break

        else:
            print("Invalid Choice")

if __name__ == "__main__":
    main()
