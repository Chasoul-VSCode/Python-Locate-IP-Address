import sys
import requests # type: ignore

def get_location_and_device(ip_address):
    try:
        # Get location data
        location_response = requests.get(f"https://ipapi.co/{ip_address}/json/", timeout=10)
        location_response.raise_for_status()
        location_data = location_response.json()
        
        # Get more accurate location
        location = f"{location_data.get('city', 'Unknown')}, {location_data.get('region', 'Unknown')}, {location_data.get('country_name', 'Unknown')}, {location_data.get('postal', 'Unknown')}"
        latitude = location_data.get('latitude', 'Unknown')
        longitude = location_data.get('longitude', 'Unknown')
        
        # Get device information
        user_agent_response = requests.get(f"http://ip-api.com/json/{ip_address}?fields=mobile,query,status,message", timeout=10)
        user_agent_response.raise_for_status()
        user_agent = user_agent_response.json()
        
        if user_agent.get('status') == 'success':
            is_mobile = user_agent.get('mobile', False)
            device_type = "Mobile Device" if is_mobile else "Desktop/Laptop"
        else:
            device_type = "Unknown Device Type"

        device = f"Device Type: {device_type}, ISP: {location_data.get('org', 'Unknown')}, AS: {location_data.get('asn', 'Unknown')}"
        
        return location, device, latitude, longitude
    except requests.RequestException as e:
        print(f"Terjadi kesalahan saat mengambil data: {e}")
        return "Lokasi tidak tersedia", "Informasi perangkat tidak tersedia", "Unknown", "Unknown"
    except ValueError as e:
        print(f"Terjadi kesalahan saat memproses data JSON: {e}")
        return "Lokasi tidak tersedia", "Informasi perangkat tidak tersedia", "Unknown", "Unknown"
    except Exception as e:
        print(f"Terjadi kesalahan yang tidak terduga: {e}")
        return f"Error: {str(e)}", "Informasi perangkat tidak tersedia", "Unknown", "Unknown"

def main():
    try:
        while True:
            ip_address = input("Masukkan alamat IP (atau 'q' untuk keluar): ")
            if ip_address.lower() == 'q':
                break
            location, device, latitude, longitude = get_location_and_device(ip_address)
            print(f"Lokasi: {location}")
            print(f"Koordinat: Latitude {latitude}, Longitude {longitude}")
            print(f"Perangkat: {device}")
            print()
    except KeyboardInterrupt:
        print("\nProgram dihentikan oleh pengguna.")
    except Exception as e:
        print(f"Terjadi kesalahan dalam program utama: {e}")
    finally:
        sys.exit(0)

if __name__ == "__main__":
    main()