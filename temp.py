import json
import requests
from config import HEADERS, COOKIES, BASE_URL

def debug_club_response(club_id):
    try:
        # Using the same URL pattern as in get_goons
        url = f"{BASE_URL}/{club_id}/position"
        
        response = requests.get(
            url,
            headers=HEADERS,
            cookies=COOKIES
        )
        response.raise_for_status()
        
        # Pretty print the JSON response
        data = response.json()
        print("Full API Response:")
        print(json.dumps(data, indent=2))
        
        # Print some basic stats about the response
        if 'items' in data:
            print(f"\nNumber of items found: {len(data['items'])}")
            
            # Print first item structure if available
            if data['items']:
                print("\nFirst item structure:")
                print(json.dumps(data['items'][0], indent=2))
                
    except requests.RequestException as e:
        print(f"Error making request: {e}")
    except json.JSONDecodeError:
        print("Error: Response contains invalid JSON")
        print("Raw response:", response.text)
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    club_id = "318622"
    debug_club_response(club_id)