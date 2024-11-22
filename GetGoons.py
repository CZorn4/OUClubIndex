import json
import requests
from config import HEADERS, COOKIES, BASE_URL, CLUB_URL

def get_clubs(CLUB_URL):
    params = {
        "orderBy[0]": "UpperName asc",
        "top": 633,
        "filter": "",
        "query": "",
        "skip": 0
    }

    clubs = []
    try:
        response = requests.get(CLUB_URL, params=params, headers=HEADERS)
        response.raise_for_status()
        
        data = response.json()
        for item in data["value"]:
            club = {
                "name": item["Name"],
                "description": item["Description"],
                "id": item["Id"],
                "goons": []
            }
            clubs.append(club)
        
        print("Successfully fetched clubs data")
        return clubs
        
    except requests.RequestException as e:
        print(f"Error fetching clubs data: {e}")
    except json.JSONDecodeError:
        print("Error: Response contains invalid JSON")
    except KeyError as e:
        print(f"Error: Missing required key {e}")
    return []

def get_goons(clubs, BASE_URL, headers=HEADERS, cookies=COOKIES):
    for club in clubs:
        try:
            # Construct the URL to access specific club info
            response = requests.get(
                f"{BASE_URL}/{club['id']}/position",
                headers=headers,
                cookies=cookies
            )
            response.raise_for_status()
            
            data = response.json()
            
            # Check if we have the items key in the response, dont know if it will ever not be but I was getting get errors
            items = data.get('items', [])
            if not items:
                print(f"No goons found for {club['name']}")
                continue
            
            for item in items:
                try:
                    holders = item.get('holders', [])
                    if not holders:
                        continue
                    
                    # Found out holders can be a list after a billion years of death and despair
                    if isinstance(holders, list):
                        for holder in holders:
                            goon = {
                                "first_name": holder.get('firstName', ''),
                                "last_name": holder.get('lastName', ''),
                                "email": holder.get('primaryEmailAddress', ''),
                                "status": "Sponsor" if not item.get('isOfficer') else item.get('name', 'Officer')
                            }
                            club['goons'].append(goon)
                    else:
                        goon = {
                            "first_name": holders.get('firstName', ''),
                            "last_name": holders.get('lastName', ''),
                            "email": holders.get('primaryEmailAddress', ''),
                            "status": "Sponsor" if not item.get('isOfficer') else item.get('name', 'Officer')
                        }
                        club['goons'].append(goon)
                        
                except Exception as e:
                    print(f"Error processing goon in {club['name']}: {e}")
            
            print(f"Goon collection completed for {club['name']}")
            
        except requests.RequestException as e:
            if "404" in str(e):
                print(f"No position data available for {club['name']}")
            else:
                print(f"Error fetching data for club {club['name']}: {e}")

def save_output(clubs, output_filename):
    try:
        with open(output_filename, 'w') as file:
            json.dump(clubs, file, indent=2)
        print(f"Data successfully saved to {output_filename}")
    except Exception as e:
        print(f"Error saving output file: {e}")

def main():
    OUTPUT_FILE = 'index.json'

    clubs = get_clubs(CLUB_URL)
    if clubs:
        get_goons(clubs, BASE_URL)
        save_output(clubs, OUTPUT_FILE)

if __name__ == "__main__":
    main()