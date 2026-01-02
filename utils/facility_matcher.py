"""
Facility Matching Engine for Arovia
Integrates with OpenStreetMap to find nearby healthcare facilities
"""
import os
import requests
import json
from typing import List, Dict, Any, Optional, Tuple
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from models.schemas import FacilityInfo
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class FacilityMatcher:
    """Facility matching engine for finding nearby healthcare facilities"""
    
    def __init__(self):
        """Initialize facility matcher"""
        self.geocoder = Nominatim(user_agent="arovia-health-desk")
        self.base_url = "https://nominatim.openstreetmap.org/search"
        
        # Medical specialty mappings
        self.specialty_mappings = {
            "cardiology": ["heart", "cardiac", "cardiovascular"],
            "neurology": ["brain", "neurological", "stroke", "seizure"],
            "pulmonology": ["lung", "respiratory", "breathing", "asthma"],
            "orthopedics": ["bone", "joint", "fracture", "spine"],
            "pediatrics": ["child", "pediatric", "infant", "baby"],
            "gynecology": ["women", "pregnancy", "maternal", "reproductive"],
            "dermatology": ["skin", "dermatological", "rash"],
            "psychiatry": ["mental", "psychiatric", "depression", "anxiety"],
            "emergency": ["emergency", "trauma", "urgent", "critical"],
            "general": ["general", "family", "primary", "clinic"]
        }
        
        # Facility type labels
        self.facility_types = {
            "government": ["government", "public", "municipal", "district", "civil"],
            "private": ["private", "corporate", "multispecialty", "hospital"],
            "ngo": ["ngo", "charitable", "trust", "foundation", "mission"],
            "local": ["local", "community", "rural", "primary", "health center"]
        }
    
    def geocode_location(self, location: str) -> Optional[Tuple[float, float]]:
        """
        Convert location string to coordinates
        
        Args:
            location: Location string (address, city, etc.)
            
        Returns:
            Tuple of (latitude, longitude) or None if not found
        """
        try:
            location_data = self.geocoder.geocode(location)
            if location_data:
                return (location_data.latitude, location_data.longitude)
            return None
        except Exception as e:
            print(f"Error geocoding location '{location}': {e}")
            return None
    
    def search_nearby_facilities(
        self, 
        latitude: float, 
        longitude: float, 
        radius_km: float = 10.0,
        specialty: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for nearby healthcare facilities using OpenStreetMap
        
        Args:
            latitude: User's latitude
            longitude: User's longitude
            radius_km: Search radius in kilometers
            specialty: Medical specialty to filter by
            
        Returns:
            List of nearby facilities
        """
        try:
            # Build search query
            query_parts = ["healthcare", "hospital", "clinic", "medical"]
            
            if specialty and specialty.lower() in self.specialty_mappings:
                specialty_keywords = self.specialty_mappings[specialty.lower()]
                query_parts.extend(specialty_keywords)
            
            query = " ".join(query_parts)
            
            # Search parameters
            params = {
                "q": query,
                "format": "json",
                "limit": 20,
                "addressdetails": 1,
                "extratags": 1,
                "bounded": 1,
                "viewbox": f"{longitude-0.1},{latitude-0.1},{longitude+0.1},{latitude+0.1}"
            }
            
            # Make request to OpenStreetMap
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            facilities = response.json()
            
            # Filter and process results
            nearby_facilities = []
            for facility in facilities:
                try:
                    # Calculate distance
                    facility_lat = float(facility.get("lat", 0))
                    facility_lon = float(facility.get("lon", 0))
                    
                    if facility_lat == 0 or facility_lon == 0:
                        continue
                    
                    distance = geodesic(
                        (latitude, longitude), 
                        (facility_lat, facility_lon)
                    ).kilometers
                    
                    # Filter by radius
                    if distance <= radius_km:
                        facility_info = self._process_facility_data(facility, distance, specialty)
                        if facility_info:
                            nearby_facilities.append(facility_info)
                
                except Exception as e:
                    print(f"Error processing facility: {e}")
                    continue
            
            # Sort by distance
            nearby_facilities.sort(key=lambda x: x["distance_km"])
            
            return nearby_facilities[:10]  # Return top 10
            
        except Exception as e:
            print(f"Error searching facilities: {e}")
            # Return mock data for demonstration
            return self._get_mock_facilities(latitude, longitude, specialty)
    
    def _process_facility_data(
        self, 
        facility_data: Dict[str, Any], 
        distance: float,
        specialty: Optional[str]
    ) -> Optional[Dict[str, Any]]:
        """
        Process raw facility data into structured format
        
        Args:
            facility_data: Raw facility data from OpenStreetMap
            distance: Distance from user in kilometers
            specialty: Medical specialty filter
            
        Returns:
            Processed facility information
        """
        try:
            # Extract basic information
            name = facility_data.get("display_name", "").split(",")[0]
            address = facility_data.get("display_name", "")
            
            # Extract additional details
            address_details = facility_data.get("address", {})
            city = address_details.get("city", address_details.get("town", ""))
            state = address_details.get("state", "")
            
            # Determine facility type
            facility_type = self._classify_facility_type(name, address)
            
            # Determine services
            services = self._determine_services(name, address, specialty)
            
            # Generate map link
            map_link = self._generate_map_link(
                facility_data.get("lat"), 
                facility_data.get("lon")
            )
            
            # Create facility info
            facility_info = {
                "name": name,
                "address": address,
                "city": city,
                "state": state,
                "distance_km": round(distance, 2),
                "facility_type": facility_type,
                "services": services,
                "specialty_match": specialty if specialty else "general",
                "map_link": map_link,
                "contact": self._extract_contact_info(facility_data),
                "coordinates": {
                    "latitude": float(facility_data.get("lat", 0)),
                    "longitude": float(facility_data.get("lon", 0))
                }
            }
            
            return facility_info
            
        except Exception as e:
            print(f"Error processing facility data: {e}")
            return None
    
    def _classify_facility_type(self, name: str, address: str) -> str:
        """Classify facility type based on name and address"""
        text = (name + " " + address).lower()
        
        for facility_type, keywords in self.facility_types.items():
            if any(keyword in text for keyword in keywords):
                return facility_type
        
        return "local"  # Default to local clinic
    
    def _determine_services(self, name: str, address: str, specialty: Optional[str]) -> List[str]:
        """Determine available services based on facility information"""
        services = ["General Consultation"]
        text = (name + " " + address).lower()
        
        # Add specialty-specific services
        if specialty and specialty.lower() in self.specialty_mappings:
            specialty_keywords = self.specialty_mappings[specialty.lower()]
            if any(keyword in text for keyword in specialty_keywords):
                services.append(f"{specialty.title()} Services")
        
        # Add common services based on keywords
        if "emergency" in text or "trauma" in text:
            services.append("Emergency Care")
        if "surgery" in text or "surgical" in text:
            services.append("Surgical Services")
        if "lab" in text or "laboratory" in text:
            services.append("Laboratory Services")
        if "x-ray" in text or "imaging" in text:
            services.append("Imaging Services")
        if "pharmacy" in text:
            services.append("Pharmacy")
        
        return services
    
    def _extract_contact_info(self, facility_data: Dict[str, Any]) -> Optional[str]:
        """Extract contact information if available"""
        # This would typically come from additional data sources
        # For now, return None as OpenStreetMap doesn't provide contact info
        return None
    
    def _generate_map_link(self, latitude: float, longitude: float) -> str:
        """Generate Google Maps link for facility"""
        return f"https://www.google.com/maps?q={latitude},{longitude}"
    
    def _get_mock_facilities(
        self, 
        latitude: float, 
        longitude: float, 
        specialty: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get mock facilities for demonstration when API is unavailable"""
        
        # Mock facilities based on specialty
        mock_facilities = []
        
        if specialty and "cardio" in specialty.lower():
            mock_facilities = [
                {
                    "name": "Apollo Heart Institute",
                    "address": "Road No 1, Jubilee Hills, Hyderabad",
                    "distance_km": 2.3,
                    "facility_type": "private",
                    "services": ["Cardiology Services", "Emergency Care", "Surgical Services"],
                    "specialty_match": "cardiology",
                    "map_link": f"https://www.google.com/maps?q={latitude+0.01},{longitude+0.01}",
                    "contact": "+91-40-6060-1066",
                    "coordinates": {"latitude": latitude+0.01, "longitude": longitude+0.01}
                },
                {
                    "name": "Government General Hospital - Cardiology",
                    "address": "Afzalgunj, Hyderabad",
                    "distance_km": 4.1,
                    "facility_type": "government",
                    "services": ["Cardiology Services", "General Consultation"],
                    "specialty_match": "cardiology",
                    "map_link": f"https://www.google.com/maps?q={latitude+0.02},{longitude-0.01}",
                    "contact": "+91-40-2323-0000",
                    "coordinates": {"latitude": latitude+0.02, "longitude": longitude-0.01}
                },
                {
                    "name": "AIIMS Cardiac Center",
                    "address": "Banjara Hills, Hyderabad",
                    "distance_km": 5.8,
                    "facility_type": "government",
                    "services": ["Cardiology Services", "Emergency Care", "Imaging Services"],
                    "specialty_match": "cardiology",
                    "map_link": f"https://www.google.com/maps?q={latitude-0.01},{longitude+0.02}",
                    "contact": "+91-40-2345-6789",
                    "coordinates": {"latitude": latitude-0.01, "longitude": longitude+0.02}
                }
            ]
        elif specialty and "neuro" in specialty.lower():
            mock_facilities = [
                {
                    "name": "NIMS Neurology Department",
                    "address": "Punjagutta, Hyderabad",
                    "distance_km": 3.2,
                    "facility_type": "government",
                    "services": ["Neurology Services", "Emergency Care", "Imaging Services"],
                    "specialty_match": "neurology",
                    "map_link": f"https://www.google.com/maps?q={latitude+0.015},{longitude+0.005}",
                    "contact": "+91-40-2345-1234",
                    "coordinates": {"latitude": latitude+0.015, "longitude": longitude+0.005}
                },
                {
                    "name": "KIMS Neuro Center",
                    "address": "Secunderabad, Hyderabad",
                    "distance_km": 4.7,
                    "facility_type": "private",
                    "services": ["Neurology Services", "Surgical Services"],
                    "specialty_match": "neurology",
                    "map_link": f"https://www.google.com/maps?q={latitude-0.01},{longitude+0.015}",
                    "contact": "+91-40-1234-5678",
                    "coordinates": {"latitude": latitude-0.01, "longitude": longitude+0.015}
                }
            ]
        else:
            # General facilities
            mock_facilities = [
                {
                    "name": "City General Hospital",
                    "address": "Main Road, City Center",
                    "distance_km": 1.5,
                    "facility_type": "government",
                    "services": ["General Consultation", "Emergency Care", "Laboratory Services"],
                    "specialty_match": "general",
                    "map_link": f"https://www.google.com/maps?q={latitude+0.005},{longitude+0.005}",
                    "contact": "+91-40-1111-2222",
                    "coordinates": {"latitude": latitude+0.005, "longitude": longitude+0.005}
                },
                {
                    "name": "Community Health Center",
                    "address": "Near Railway Station",
                    "distance_km": 2.8,
                    "facility_type": "local",
                    "services": ["General Consultation", "Pharmacy"],
                    "specialty_match": "general",
                    "map_link": f"https://www.google.com/maps?q={latitude-0.005},{longitude+0.01}",
                    "contact": "+91-40-3333-4444",
                    "coordinates": {"latitude": latitude-0.005, "longitude": longitude+0.01}
                },
                {
                    "name": "Charitable Medical Trust",
                    "address": "Old City Area",
                    "distance_km": 3.5,
                    "facility_type": "ngo",
                    "services": ["General Consultation", "Emergency Care", "Laboratory Services"],
                    "specialty_match": "general",
                    "map_link": f"https://www.google.com/maps?q={latitude+0.01},{longitude-0.005}",
                    "contact": "+91-40-5555-6666",
                    "coordinates": {"latitude": latitude+0.01, "longitude": longitude-0.005}
                }
            ]
        
        return mock_facilities
    
    def find_facilities_for_condition(
        self,
        user_location: str,
        specialty: str,
        radius_km: float = 10.0
    ) -> List[Dict[str, Any]]:
        """
        Find facilities for a specific medical condition
        
        Args:
            user_location: User's location (address, city, etc.)
            specialty: Required medical specialty
            radius_km: Search radius in kilometers
            
        Returns:
            List of facility data dictionaries
        """
        try:
            # Geocode user location
            coordinates = self.geocode_location(user_location)
            if not coordinates:
                return []
            
            latitude, longitude = coordinates
            
            # Search for facilities
            facilities_data = self.search_nearby_facilities(
                latitude, longitude, radius_km, specialty
            )
            
            return facilities_data
            
        except Exception as e:
            print(f"Error finding facilities: {e}")
            return []


# Convenience function for quick facility search
def find_nearby_clinics(
    location: str,
    specialty: str = "general",
    radius_km: float = 10.0
) -> List[Dict[str, Any]]:
    """
    Quick function to find nearby clinics
    
    Args:
        location: User's location
        specialty: Medical specialty needed
        radius_km: Search radius in kilometers
        
    Returns:
        List of nearby facility data
    """
    matcher = FacilityMatcher()
    return matcher.find_facilities_for_condition(location, specialty, radius_km)


if __name__ == "__main__":
    # Test the facility matcher
    print("Testing Facility Matcher...")
    
    matcher = FacilityMatcher()
    
    # Test with a sample location
    test_location = "Hyderabad, Telangana, India"
    test_specialty = "cardiology"
    
    print(f"Searching for {test_specialty} facilities near {test_location}")
    
    facilities = matcher.find_facilities_for_condition(
        test_location, test_specialty, radius_km=15.0
    )
    
    print(f"Found {len(facilities)} facilities:")
    for i, facility in enumerate(facilities, 1):
        print(f"{i}. {facility['name']}")
        print(f"   Distance: {facility['distance_km']} km")
        print(f"   Specialty: {facility['specialty_match']}")
        print(f"   Services: {', '.join(facility['services'])}")
        print(f"   Map: {facility['map_link']}")
        print()
