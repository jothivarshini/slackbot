import json
import urllib.request
import os
import re


slack_token = 'YOUR-TOKEN-HERE'
slack_channel = 'lambdatest'

def get_users_list(event):
    SLACK_URL = "https://slack.com/api/users.list"
    user_data = urllib.parse.urlencode({
        "token": slack_token,
    })

    user_data = user_data.encode("ascii")
    request = urllib.request.Request(SLACK_URL, data=user_data, method="POST")
    request.add_header("Content-Type", "application/x-www-form-urlencoded")
    response = urllib.request.urlopen(request).read()
    data = json.loads(response)
    
    if data['ok']:
        member_list = [member for member in data['members'] if not member['deleted']]
        return member_list
    else:
        error_message = data['error']
        print('Slack API error: {error_message}')
        return None

def find_member_with_email(members, email):
    for member in members:
        if 'email' in member['profile'] and member['profile']['email'] == email:
            return member
    return None
    
def send_text_response(event, user):
    profileDetails = user
    SLACK_URL = "https://slack.com/api/chat.postMessage" # use postMessage if we want visible for everybody
    data = urllib.parse.urlencode({
            "token": slack_token,
            'channel': slack_channel,
            'text': event['message'],
             'username': profileDetails['profile']['display_name'],
             'icon_url': profileDetails['profile']['image_48']

        })
        
    data = data.encode("ascii")
    request = urllib.request.Request(SLACK_URL, data=data, method="POST")
    request.add_header( "Content-Type", "application/x-www-form-urlencoded" )
    res = urllib.request.urlopen(request).read()
    print('res:', res)
    
def lambda_handler(event, context):
    email_to_find = event['email']
    users = get_users_list(event)
    
    if users is not None:
        member_with_email = find_member_with_email(users, email_to_find)
        if member_with_email is not None:
            print('member_with_email', member_with_email)
            send_text_response(event, member_with_email)
        else:
            print(f"No member found with email: {email_to_find}")
    
    print('event:', event)
    get_users_list(event)
    # send_text_response(event)
    return {
        'statusCode': 200,
        'body': 'OK'
    }