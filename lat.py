import requests
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

def get_detailed_location(latitude, longitude):
    try:
        # Initialize Nominatim API
        geolocator = Nominatim(user_agent="myGeocoder")
        
        # Reverse geocoding
        location = geolocator.reverse(f"{latitude}, {longitude}")
        
        if location:
            address = location.raw['address']
            
            # Extract detailed information
            road = address.get('road', address.get('street', 'N/A'))  # Try to get road or street name
            house_number = address.get('house_number', 'N/A')
            neighbourhood = address.get('neighbourhood', 'N/A')
            suburb = address.get('suburb', 'N/A')
            city = address.get('city', address.get('town', 'N/A'))
            state = address.get('state', 'N/A')
            country = address.get('country', 'N/A')
            postcode = address.get('postcode', 'N/A')
            
            # If road is still not found, try to construct it from other available information
            if road == 'N/A':
                road_components = [
                    address.get('road_reference', ''),
                    address.get('road_type', ''),
                    address.get('road_name', '')
                ]
                road = ' '.join(filter(None, road_components)) or 'Tidak diketahui'
            
            detailed_location = f"""
            Koordinat: {latitude}, {longitude}
            Jalan: {road}
            Nomor: {house_number}
            Lingkungan: {neighbourhood}
            Kelurahan/Desa: {suburb}
            Kota: {city}
            Provinsi: {state}
            Negara: {country}
            Kode Pos: {postcode}
            """
            
            return detailed_location.strip()
        else:
            return "Lokasi tidak ditemukan"
    
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        return f"Error: Layanan geocoding tidak tersedia - {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    try:
        latitude = float(input("Masukkan latitude: "))
        longitude = float(input("Masukkan longitude: "))
        
        detailed_location = get_detailed_location(latitude, longitude)
        print(detailed_location)
    
    except ValueError:
        print("Error: Masukkan latitude dan longitude yang valid (angka desimal)")
    except Exception as e:
        print(f"Terjadi kesalahan: {str(e)}")

if __name__ == "__main__":
    main()
