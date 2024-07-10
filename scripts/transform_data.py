import json


def transform_data():
    with open('/tmp/nogizaka46_data.json') as infile:
        raw_data = json.load(infile)

    transformed_data = []
    for member in raw_data['data']:
        member_data = {
            'code': member['code'],
            'name': member['name'].strip(),
            'english_name': member.get('english_name', '').strip(),
            'kana': member.get('kana', '').strip(),
            'category': member.get('cate', '').strip(),
            'image_url': member.get('img', '').strip(),
            'profile_link': member.get('link', '').strip(),
            'pick': member.get('pick', '').strip(),
            'god': member.get('god', '').strip(),
            'under': member.get('under', '').strip(),
            'birthday': member.get('birthday', '').strip(),
            'blood_type': member.get('blood', '').strip(),
            'constellation': member.get('constellation', '').strip(),
            'graduation': member.get('graduation', 'NO').strip(),
        }
        transformed_data.append(member_data)

    with open('/tmp/transformed_nogizaka46_data.json', 'w') as outfile:
        json.dump(transformed_data, outfile)
    print("Data successfully transformed and saved to /tmp/transformed_nogizaka46_data.json")