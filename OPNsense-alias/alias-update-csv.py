import json
import uuid
import csv
#script by skatopn on the OPNsense forums
#original source: https://forum.opnsense.org/index.php?topic=36687.msg192872#msg192872

jsonfile = 'C:/path/to/aliases.json'
csvfile = 'C:/path/to/opnsense_alias.csv'
# jsonfile = '/path/to/aliases.json'
# csvfile = '/path/to/opnsense_alias.csv'

with open(jsonfile) as user_file:
    parsed_json = json.load(user_file)

cur_items=parsed_json['aliases']['alias']

with open(csvfile, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        #print(row)
        item_name = row['name']
        item_data = row['data']
        item_type = row['type']
        item_description = row['description']

        if len(row['data'].split(" "))>1:
            item_data = "\n".join(row['data'].split(" "))

        item_uuid = str(uuid.uuid4())

        new_alias =    {'enabled': '1',
                'name': item_name,
                'type': item_type,
                'proto': '',
                'interface': '',
                'counters': '0',
                'updatefreq': '',
                'content': item_data,
                'categories': '',
                'description': item_description
            }

        cur_items[item_uuid] = new_alias

with open(jsonfile, 'w', encoding="utf-8") as f:
    json.dump(parsed_json, f, indent=2)