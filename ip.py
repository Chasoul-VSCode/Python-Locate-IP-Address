import sys
import platform
import socket
import requests # type: ignore
import subprocess
import re
import json
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import time
import random
import geoip2.database
from user_agents import parse
import pytz

try:
    from geopy.geocoders import Nominatim
    from geopy.exc import GeocoderTimedOut, GeocoderServiceError
except ImportError:
    print("Modul geopy tidak ditemukan. Menginstall geopy...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "geopy"])
    from geopy.geocoders import Nominatim
    from geopy.exc import GeocoderTimedOut, GeocoderServiceError

if sys.platform.startswith('win'):
    import winreg
    from winreg import WindowsError
else:
    class WindowsError(Exception):
        pass

def get_chrome_email():
    return "Email tidak tersedia"

def get_windows_location():
    return "Informasi lokasi Windows tidak tersedia"

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "IP lokal tidak tersedia"

def get_detailed_location(latitude, longitude):
    try:
        time.sleep(random.uniform(1, 3))
        
        geolocator = Nominatim(user_agent="MyApp/1.0")
        location = geolocator.reverse(f"{latitude}, {longitude}", exactly_one=True, language='id')
        
        if location:
            address = location.raw['address']
            
            road = address.get('road', 'Tidak tersedia')
            house_number = address.get('house_number', 'Tidak tersedia')
            neighbourhood = address.get('neighbourhood', 'Tidak tersedia')
            suburb = address.get('suburb', 'Tidak tersedia')
            city = address.get('city', address.get('town', address.get('village', 'Tidak tersedia')))
            district = address.get('county', address.get('state_district', 'Tidak tersedia'))
            state = address.get('state', 'Tidak tersedia')
            country = address.get('country', 'Tidak tersedia')
            postcode = address.get('postcode', 'Tidak tersedia')
            
            detailed_location = f"""
            Koordinat: {latitude}, {longitude}
            Jalan: {road}
            Nomor: {house_number}
            Lingkungan: {neighbourhood}
            Kelurahan/Desa: {suburb}
            Kota/Kabupaten: {city}
            Kecamatan: {district}
            Provinsi: {state}
            Negara: {country}
            Kode Pos: {postcode}
            """
            
            return detailed_location.strip()
        else:
            return "Lokasi detail tidak ditemukan"
    
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        return f"Layanan geolokasi tidak tersedia: {str(e)}"
    except Exception as e:
        return f"Terjadi kesalahan: {str(e)}"

def get_phone_number(ip_address):
    try:
        response = requests.get(f"https://ipapi.co/{ip_address}/json/", timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get('country_calling_code', '') + data.get('phone', 'Tidak tersedia')
    except:
        return "Nomor telepon tidak tersedia"

def get_device_info(user_agent_string):
    user_agent = parse(user_agent_string)
    device_type = "Perangkat Mobile" if user_agent.is_mobile else "Desktop/Laptop"
    os_family = user_agent.os.family
    browser_family = user_agent.browser.family
    device_brand = user_agent.device.brand if user_agent.device.brand else "Tidak diketahui"
    device_model = user_agent.device.model if user_agent.device.model else "Tidak diketahui"
    
    return f"{device_type}, OS: {os_family}, Browser: {browser_family}, Merek: {device_brand}, Model: {device_model}"

def get_location_and_device(ip_address):
    try:
        location_response = requests.get(f"https://ipapi.co/{ip_address}/json/", timeout=10)
        location_response.raise_for_status()
        location_data = location_response.json()
        
        latitude = location_data.get('latitude', 'Tidak tersedia')
        longitude = location_data.get('longitude', 'Tidak tersedia')
        
        detailed_location = get_detailed_location(latitude, longitude)
        
        user_agent_response = requests.get(f"http://ip-api.com/json/{ip_address}?fields=mobile,query,status,message", timeout=10)
        user_agent_response.raise_for_status()
        user_agent_data = user_agent_response.json()
        
        if user_agent_data.get('status') == 'success':
            user_agent_string = requests.get('http://httpbin.org/user-agent').json()['user-agent']
            device_info = get_device_info(user_agent_string)
        else:
            device_info = "Informasi perangkat tidak tersedia"

        device = f"Perangkat: {device_info}, ISP: {location_data.get('org', 'Tidak tersedia')}, AS: {location_data.get('asn', 'Tidak tersedia')}"
        
        phone_number = get_phone_number(ip_address)
        
        return detailed_location, device, phone_number, "Tidak tersedia", "Tidak tersedia", "Tidak tersedia", latitude, longitude
    except requests.RequestException as e:
        print(f"Terjadi kesalahan saat mengambil data: {e}")
    except ValueError as e:
        print(f"Terjadi kesalahan saat memproses data JSON: {e}")
    except Exception as e:
        print(f"Terjadi kesalahan yang tidak terduga: {e}")
    
    return ("Lokasi tidak tersedia", 
            "Informasi perangkat tidak tersedia", 
            "Tidak tersedia", 
            "Tidak tersedia", 
            "Tidak tersedia", 
            "Tidak tersedia", 
            "Tidak tersedia", 
            "Tidak tersedia")

def get_info_by_phone(phone_number):
    try:
        # Gunakan API untuk mendapatkan informasi berdasarkan nomor telepon
        # Catatan: Ini adalah contoh dan mungkin memerlukan API yang sesuai
        response = requests.get(f"https://api.example.com/phone/{phone_number}", timeout=10)
        response.raise_for_status()
        data = response.json()
        
        ip_address = data.get('ip_address', 'Tidak tersedia')
        location = data.get('location', 'Lokasi tidak tersedia')
        device = data.get('device', 'Informasi perangkat tidak tersedia')
        
        return ip_address, location, device
    except:
        return "Tidak tersedia", "Lokasi tidak tersedia", "Informasi perangkat tidak tersedia"

def main():
    try:
        while True:
            print("\nPilih metode pelacakan:")
            print("1. Melacak melalui alamat IP")
            print("2. Melacak melalui nomor HP")
            print("3. Keluar")
            
            choice = input("Masukkan pilihan (1/2/3): ")
            
            if choice == '1':
                ip_address = input("Masukkan alamat IP: ")
                location, device, phone_number, user_name, instagram_username, email, latitude, longitude = get_location_and_device(ip_address)
                print(f"\nLokasi Detail:\n{location}")
                print(f"Koordinat: Latitude {latitude}, Longitude {longitude}")
                print(f"{device}")
                print(f"Nomor HP: {phone_number}")
                print(f"Nama Pengguna: {user_name}")
                print(f"Username Instagram: {instagram_username}")
                print(f"Alamat Email: {email}")
            elif choice == '2':
                phone_number = input("Masukkan nomor HP: ")
                ip_address, location, device = get_info_by_phone(phone_number)
                print(f"\nAlamat IP: {ip_address}")
                print(f"Lokasi: {location}")
                print(f"Informasi Perangkat: {device}")
            elif choice == '3':
                break
            else:
                print("Pilihan tidak valid. Silakan coba lagi.")
            
            print()
    except KeyboardInterrupt:
        print("\nProgram dihentikan oleh pengguna.")
    except Exception as e:
        print(f"Terjadi kesalahan dalam program utama: {e}")
    finally:
        print("Program selesai.")
        sys.exit(0)

if __name__ == "__main__":
    main()