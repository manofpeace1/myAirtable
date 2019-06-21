import requests
import config


def url(x):
    endpoint = 'https://api.airtable.com/'
    ver = 'v0'
    sort_param = 'Status'
    sort_by = 'desc'
    table = config.table
    tab = config.tab
    api_key = config.api_key
    return f'{endpoint}/{ver}/{table}/{tab}?api_key={api_key}&offset={x}&sort%5B0%5D%5Bfield%5D={sort_param}&sort%5B0%5D%5Bdirection%5D={sort_by}'


def run():
    global offset
    offset = ''
    user_input = input(f"\n🌟 Select Year (empty = ALL) >>> ")
    while True:
        response = requests.get(
            url(offset)).json()
        # Get [Status, Name, Type] of every entry
        for z in response['records']:
            fields = z['fields']
            if 'Name' in fields:
                z_status = fields['Status']
                z_name = fields['Name']
                z_type = fields['Type']
                result = '{0}---{1}---{2}'.format(z_status, z_name, z_type)

                # (A) User_input is empty --> shows ALL entries OR
                if user_input == '':
                    print(result)
                # (B) User_input is e.g. 2019 --> shows entries with 2019 in Notes
                else:
                    if 'Note' in fields:
                        if user_input in fields['Note']:
                            print(result)
                        else:
                            pass
                    else:
                        pass
            else:
                pass
        # Request next page if there's offset value
        if 'offset' in response:
            offset = response['offset']

        # Stop request if there's no offset value (last page)
        else:
            break


while True:
    run()
