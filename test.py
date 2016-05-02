
access_token = 'KLpQjSt6D8EY8895cj9OQgUCvLtXho'

def use_system():

    # need to add more code below
    import requests

    headers = {
        'Authorization': 'Bearer %s' % access_token,
    }

    patients = []
    patients_url = 'https://drchrono.com/api/patients'
    while patients_url:
        data = requests.get(patients_url, headers=headers).json()
        patients.extend(data['results'])
        patients_url = data['next'] # A JSON null on the last page

    print patients











