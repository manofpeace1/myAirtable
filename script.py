import requests
import config


def send_request(offset):
    ver = 'v0'
    sort_param = 'Status'
    sort_by = 'desc'
    table = config.table
    tab = config.tab
    api_key = config.api_key
    return f'https://api.airtable.com/{ver}/{table}/{tab}?api_key={api_key}&offset={offset}&sort%5B0%5D%5Bfield%5D={sort_param}&sort%5B0%5D%5Bdirection%5D={sort_by}'


def collect_result():
    global result_list
    result_list = []
    offset = ''
    user_input = input(f"\n🌟 Select Year (empty = ALL) >>> ")

    while True:
        response = requests.get(
            send_request(offset)).json()
        # Get [Status, Name, Type] of every entry
        for item in response['records']:
            fields = item['fields']
            if 'Name' in fields:
                result = '{0}---{1}---{2}'.format(
                    fields['Status'], fields['Name'], fields['Type'])

                # (A) User_input is empty --> shows ALL entries OR
                if user_input == '':
                    result_list.append(result)

                # (B) User_input is e.g. 2019 --> shows entries with 2019 in Notes
                else:
                    if 'Note' in fields and user_input in fields['Note']:
                        result_list.append(result)
            else:
                pass
        # Request next page if there's offset value
        if 'offset' in response:
            offset = response['offset']
        else:
            break


def show_result():
    for result in result_list:
        print(result)
