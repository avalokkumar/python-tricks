import subprocess

def get_wifi_profiles_linux():
    """Get a list of Wi-Fi profiles on Linux and their passwords."""
    try:
        # Run nmcli command to show all Wi-Fi profiles
        profiles_data = subprocess.run(['nmcli', '-t', '-f', 'NAME', 'connection', 'show'], capture_output=True, text=True).stdout
        
        # Extract profile names
        profiles = [line.strip() for line in profiles_data.split('\n') if line.strip()]

        wifi_details = []
        
        # Extract password for each profile
        for profile in profiles:
            # Use nmcli to get the Wi-Fi password for the profile
            profile_info = subprocess.run(['nmcli', '-s', '-g', '802-11-wireless-security.psk', 'connection', 'show', profile], capture_output=True, text=True).stdout.strip()
            
            password = profile_info if profile_info else "No Password"
            
            wifi_details.append({'Profile': profile, 'Password': password})
        
        return wifi_details

    except Exception as e:
        print(f"Error retrieving Wi-Fi profiles: {e}")
        return []

def main():
    wifi_details = get_wifi_profiles_linux()
    
    # Print the Wi-Fi details
    if wifi_details:
        for wifi in wifi_details:
            print(f"Profile: {wifi['Profile']}, Password: {wifi['Password']}")
    else:
        print("No Wi-Fi profiles found or an error occurred.")

if __name__ == "__main__":
    main()
