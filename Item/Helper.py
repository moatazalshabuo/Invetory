from msal import ConfidentialClientApplication
import requests
import json
from msgraph import GraphServiceClient
from azure.identity.aio import ClientSecretCredential

def get_token():
    CLIENT_ID = 'f532584a-9de6-418e-a24d-0abc38539309'
    CLIENT_SECRET = 'Mf~8Q~7Nf75Bojbi4n~2WC36bABHrDsYQHnCTaax'
    TENANT_ID = '406d5069-8b90-4f51-b457-3b20d604f540'
    # MSAL configuration
    authority = 'https://login.microsoftonline.com/' + TENANT_ID
    app = ConfidentialClientApplication(
        CLIENT_ID,
        authority=authority,
        client_credential=CLIENT_SECRET,
    )

    # Get a token
    token_response = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    return token_response['access_token']

def users():
    access_token = get_token()
    params = {'$select': 'id,displayName,state,usageLocation,userPrincipalName'}
    users = requests.get(url = "https://graph.microsoft.com/v1.0/users",headers={
        'Authorization':"Bearer "+access_token,
        'Content-Type':'application/json'
    },params = params)
    
    all_users = []
    while('@odata.nextLink' in users.json().keys()):
        all_users.extend(users.json().get('value'))
        users = requests.get(url = users.json()['@odata.nextLink'],headers={
        'Authorization':"Bearer "+access_token,
        'Content-Type':'application/json'})
    
    return all_users

def user(id):
    access_token = get_token()
    params = {'$select': 'id,displayName,state,usageLocation,userPrincipalName'}

    users = requests.get(url = 'https://graph.microsoft.com/v1.0/users/'+id,headers={
        'Authorization':"Bearer "+access_token,
        'Content-Type':'application/json'
    },params = params)
    
    return users.json()
def search(name):
    access_token = get_token()
    params = {
        '$select': 'id,displayName,state,usageLocation,userPrincipalName',
        '$search':f'"displayName:{name}" OR "state:{name}"'
        }

    users = requests.get(url = 'https://graph.microsoft.com/v1.0/users',headers={
        'Authorization':"Bearer "+access_token,
        'Content-Type':'application/json',
        'ConsistencyLevel': 'eventual',
    },params = params)    
    return users.json()['value']

def sendMail(id):
    access_token = get_token()
    id = "55587c62-0bd4-4e01-b860-1e336fa9c091"
    endpoint = f'https://graph.microsoft.com/v1.0/users/{id}/sendMail'
    toUserEmail = [{
        'EmailAddress': {'Address':"muetaz.alsahbu@zallaf.com"},
        },{
        'EmailAddress': {'Address':"Aboulqasim.Abdulrahman@zallaf.com"},
        }]
    
    content = """<table width='100%' border='1' cellpadding='5' style='border-collapse:collapse;border:1px solid black;'>
                    <tbody>
                        <tr style='background-color:#EFEFEF;'>
                            <th>Zallaf ID</th>
                            <th>Employee Name</th>
                            <th>Department</th>
                            <th>Device Name</th>
                            <th>Device ST</th>
                            <th>Given On</th></tr>
                        <tr>
                            <td>ZL0379 </td>
                            <td>Aboulqasim Abdulrahman </td>
                            <td>ICT </td>
                            <td>Lenovo ThinkPad E14 Gen 2 </td>
                            <td>PF39ZQEQ </td>
                            <td>1/2/2024 </td>
                        </tr>
                        </tbody>
                    </table>
                    """
    email_msg = {'Message': {'Subject': "Test Sending Email from Python",
                             'Body': {'ContentType': 'HTML', 'Content':content },
                             'ToRecipients': toUserEmail
                             },
                 'SaveToSentItems': 'true'}
    try:
         r = requests.post(endpoint,
                      headers={'Authorization': 'Bearer ' + access_token}, json=email_msg)
    except Exception :
        return False
   
    return True