import subprocess

# Get the list of Wi-Fi profiles
try:
    data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors="backslashreplace").split('\n')
except subprocess.CalledProcessError as e:
    print("Failed to retrieve Wi-Fi profiles:", e)
    exit(1)

profiles = []
for line in data:
    if "All User Profile" in line:
        # Extract the profile name
        profile_name = line.split(":")[1][1:-1]
        profiles.append(profile_name)

# Print the Wi-Fi profiles and their passwords
print("{:<30} | {:<}".format("Profile Name", "Password"))
print("-" * 50)

for profile in profiles:
    try:
        # Get the details of each profile
        results = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles', profile, 'key=clear']).decode('utf-8', errors="backslashreplace").split('\n')
        password = ""
        
        for line in results:
            if "Key Content" in line:
                password = line.split(":")[1][1:-1]  # Extract the password
                break

        print("{:<30} | {:<}".format(profile, password if password else "No Password"))
    except subprocess.CalledProcessError as e:
        print("{:<30} | {:<}".format(profile, "ERROR OCCURRED"))
