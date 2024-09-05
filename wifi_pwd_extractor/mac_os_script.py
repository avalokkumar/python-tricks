## For Mac OS
## Script to extract Wi-Fi profiles and their passwords stored in Keychain

import subprocess

def get_wifi_profiles_macos():
    """Get a list of Wi-Fi profiles on macOS and their passwords."""
    wifi_details = []
    
    # Fetch all Wi-Fi profiles stored in Keychain
    try:
        profiles_data = subprocess.run(
            ['security', 'find-generic-password', '-D', 'AirPort network password', '-ga', ''],
            capture_output=True, text=True
        ).stderr

        profiles = []
        
        # Split the output lines and extract Wi-Fi names
        for line in profiles_data.split('\n'):
            if 'acct<' in line:
                profile_name = line.split('"')[1]  # Extract the profile name
                profiles.append(profile_name)
        
        for profile in profiles:
            try:
                profile_info = subprocess.run(
                    ['security', 'find-generic-password', '-D', 'AirPort network password', '-ga', profile],
                    capture_output=True, text=True
                ).stderr
                password_line = [line for line in profile_info.split('\n') if "password:" in line]
                password = password_line[0].split('"')[1] if password_line else "No Password"
            except IndexError:
                password = "No Password"
            
            wifi_details.append({'Profile': profile, 'Password': password})
    
    except Exception as e:
        print(f"Error retrieving Wi-Fi profiles: {e}")
    
    return wifi_details

def main():
    wifi_details = get_wifi_profiles_macos()
    
    # Print the Wi-Fi details
    if wifi_details:
        for wifi in wifi_details:
            print(f"Profile: {wifi['Profile']}, Password: {wifi['Password']}")
    else:
        print("No Wi-Fi profiles found or access denied.")

if __name__ == "__main__":
    main()
