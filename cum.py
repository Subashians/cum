import requests
import time
from discord_webhook import DiscordWebhook

webhook_url = 'https://discord.com/api/webhooks/1249091717928583249/CztKWXQHXRU7kTVs1PqRg4EZxA8mwGE4llKgVsDGw9rEyiPrGNtrj27s3RiewyQNW0cW'
webhook = DiscordWebhook(url=webhook_url, content='SCRIPT INITIALIZED')
response = webhook.execute()

def fetch_data():
    url = "https://biggamesapi.io/api/clan/Gewp"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "YOUR_API_KEY"
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    return data
def get_user_points(data, roblox_id):
    for point_contribution in data['data']['Battles']['HackerBattle']['PointContributions']:
        if point_contribution['UserID'] == roblox_id:
            return point_contribution['Points']
    return 0

def fetch_roblox_username(roblox_id):
    url = f"https://users.roblox.com/v1/users/{roblox_id}"
    response = requests.get(url)
    data = response.json()
    return data['name'] if 'name' in data else 'Unknown'
def send_discord_message(webhook_url, discord_id, message):
    webhook = DiscordWebhook(url=webhook_url, content=f"<@{discord_id}> {message}")
    response = webhook.execute()
    print(f"Sent message to Discord: {response}")
def send_hourly_summary(webhook_url, points_gained):
    summary_message = "POINTS GAINED FOR THE LAST HOUR\n"
    for roblox_id, points in points_gained.items():
        username = fetch_roblox_username(roblox_id)
        summary_message += f"{username}: {points} points\n"
    send_discord_message(webhook_url, '', summary_message)


users = {
    902729116535644220: 1487341993,
    1130177212738449438: 3049767178,
    1002184274792960130: 2899769274,
    784755403849596949: 3448775790,
    345029498535804928: 194425224,
    576799969697333268: 1172304127,
    456507414318022657: 46490088,
    399015465684566016: 3990213197,
}

alert_webhook_url = 'https://discord.com/api/webhooks/1249091717928583249/CztKWXQHXRU7kTVs1PqRg4EZxA8mwGE4llKgVsDGw9rEyiPrGNtrj27s3RiewyQNW0cW'  
summary_webhook_url = 'https://discord.com/api/webhooks/1249331331163226153/udpCAGw1Y3xyJTWGVuqy5srZduOBFrpnloizJBk4xV26X940hy7_ZhRDh_xghECduLM0'


def main():
    last_points_check = {roblox_id: time.time() for roblox_id in users.values()}
    last_points = {roblox_id: 0 for roblox_id in users.values()}
    initial_points = {roblox_id: 0 for roblox_id in users.values()}
    message_sent = {roblox_id: False for roblox_id in users.values()}
    last_hour_check = time.time()
    data = fetch_data()
    for roblox_id in users.values():
        initial_points[roblox_id] = get_user_points(data, roblox_id)
        last_points[roblox_id] = initial_points[roblox_id]

    while True:
        data = fetch_data()
        for discord_id, roblox_id in users.items():
            current_points = get_user_points(data, roblox_id)
            print(f"Current points for user {roblox_id}: {current_points}")

            if current_points > last_points[roblox_id]:
                last_points[roblox_id] = current_points
                last_points_check[roblox_id] = time.time()
                message_sent[roblox_id] = False
                print(f"Points increased for user {roblox_id}. New points: {current_points}. Resetting timer.")
            
            elif (time.time() - last_points_check[roblox_id]) >= 900: 
                if not message_sent[roblox_id]:
                    print(f"No points gained in the last 5 minutes for user {roblox_id}. Sending Discord message...")
                    send_discord_message(alert_webhook_url, discord_id, "YOUR FATASS IS OFFLINE!!!!!!!!!")
                    message_sent[roblox_id] = True
        if (time.time() - last_hour_check) >= 3600:
            points_gained = {roblox_id: last_points[roblox_id] - initial_points[roblox_id] for roblox_id in users.values()}
            print("Sending hourly summary...")
            send_hourly_summary(summary_webhook_url, points_gained)
            initial_points = last_points.copy()
            last_hour_check = time.time()

        print(f"Sleeping for 60 seconds. Current time: {time.time()}")
        time.sleep(60) 
if __name__ == "__main__":
    main()
