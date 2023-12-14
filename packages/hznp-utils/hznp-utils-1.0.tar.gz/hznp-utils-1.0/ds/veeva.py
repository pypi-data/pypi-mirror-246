try:
    from google.cloud import secretmanager
except:
    import pip
    print("Installing google-cloud-secret-manager")
    pip.main(['install', 'google-cloud-secret-manager'])
    from google.cloud import secretmanager
import pandas as pd
import requests
import pip



def npi_data(npis): 
    # Define a place to store the returning DataFrame
    
    client = secretmanager.SecretManagerServiceClient()
    username = client.access_secret_version(request={"name": "projects/511675646729/secrets/VEEVA_NETWORK_USER/versions/latest"}).payload.data.decode("UTF-8")
    password = client.access_secret_version(request={"name": "projects/511675646729/secrets/VEEVA_NETWORK_PASS/versions/latest"}).payload.data.decode("UTF-8")
    df = pd.DataFrame({})
    # Define information needed for response 
    headers = { 'Content-Type': 'application/x-www-form-urlencoded',} 
    data = f'username={username}&password={password}'
    session_response = requests.post('https://horizon.veevanetwork.com/api/v1.0/auth', headers=headers, data=data)
    session_response = session_response.json()
    session_response 
    headers = {
    'Authorization': session_response['sessionId'],
    }
    server = 'horizon.veevanetwork.com'
        
    # Define a place to hold the list of dictionaries and the dictionary to append on
    dictionaries = []

    # Iterate through each id in the list of ids and create a list of dictionaries
    for npi in npis:
        try:
            dictionary = {}
            npi_for_response = str(npi)
            # response = requests.get(f'https://{server}/api/v29.0/entity/{id_for_response}', headers=headers)
            response = requests.get(f'https://{server}/api/v30.0/search?q=*&nestChildObjectFieldQueries=true&types=HCP&filters=~hcp.npi_num__v:{npi_for_response}', headers=headers)
            data = response.json()
            for item in data["entities"]:
                for first_key, first_value in (item.items()):
                    if first_key != "entity":
                        dictionary[first_key] =  first_value
                    if first_key == "entity":
                        for second_key, second_value in first_value.items():
                            if second_key == "addresses__v":
                                for item in second_value:
                                    for key, value in item.items():
                                        dictionary[key] = value  
                            elif second_key == "custom_keys__v":
                                for item in second_value:
                                    for key, value in item.items():
                                        dictionary[key] = value 
                            elif second_key == "licenses__v":
                                for item in second_value:
                                    for key, value in item.items():
                                        dictionary[key] = value 
                            elif second_key == "parent_hcos__v":
                                for item in second_value:
                                    for key, value in item.items():
                                        if key == "custom_keys__v":
                                            for item in value:
                                                for key, value in item.items():
                                                    dictionary[key] = value 
                                        if key != "custom_keys__v":
                                            dictionary[key] = value
                            else:
                                dictionary[second_key] = second_value              
                                                            
                dictionaries.append(dictionary) 
        except Exception as e:
            print(e)
                                       
        
    # Convert the list of dictionaries to a DataFrame    
    df = pd.DataFrame.from_records(dictionaries)
        
    # Return DataFrame
    return df