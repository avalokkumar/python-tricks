import subprocess

def get_wifi_profiles_windows():
    """Get a list of Wi-Fi profiles on Windows and their passwords."""
    try:
        # Run netsh command to show all Wi-Fi profiles
        profiles_data = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], capture_output=True, text=True).stdout
        
        # Extract profile names
        profiles = [line.split(":")[1].strip() for line in profiles_data.split('\n') if "All User Profile" in line]

        wifi_details = []
        
        # Extract password for each profile
        for profile in profiles:
            profile_info = subprocess.run(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear'], capture_output=True, text=True).stdout
            
            # Extract password line, if available
            password_lines = [line for line in profile_info.split('\n') if "Key Content" in line]
            password = password_lines[0].split(":")[1].strip() if password_lines else "No Password"
            
            wifi_details.append({'Profile': profile, 'Password': password})
        
        return wifi_details

    except Exception as e:
        print(f"Error retrieving Wi-Fi profiles: {e}")
        return []

def main():
    wifi_details = get_wifi_profiles_windows()
    
    # Print the Wi-Fi details
    if wifi_details:
        for wifi in wifi_details:
            print(f"Profile: {wifi['Profile']}, Password: {wifi['Password']}")
    else:
        print("No Wi-Fi profiles found or an error occurred.")

if __name__ == "__main__":
    main()
