"""
Location Detection Component for Arovia
Handles automatic geolocation and manual location input
"""
import streamlit as st
import streamlit.components.v1 as components
from typing import Optional, Tuple
import json

def location_detector() -> Tuple[Optional[str], Optional[Tuple[float, float]]]:
    """
    Location detector component that requests user's location
    
    Returns:
        Tuple of (address, coordinates) or (None, None) if not available
    """
    
    # JavaScript for geolocation
    location_js = """
    <script>
    function getLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                function(position) {
                    const lat = position.coords.latitude;
                    const lon = position.coords.longitude;
                    
                    // Store coordinates in session storage
                    sessionStorage.setItem('user_lat', lat);
                    sessionStorage.setItem('user_lon', lon);
                    
                    // Trigger a custom event
                    window.dispatchEvent(new CustomEvent('locationDetected', {
                        detail: {lat: lat, lon: lon}
                    }));
                },
                function(error) {
                    let message = "Location access denied or unavailable.";
                    switch(error.code) {
                        case error.PERMISSION_DENIED:
                            message = "Location access denied. Please allow location access.";
                            break;
                        case error.POSITION_UNAVAILABLE:
                            message = "Location information unavailable.";
                            break;
                        case error.TIMEOUT:
                            message = "Location request timed out.";
                            break;
                    }
                    alert(message);
                },
                {
                    enableHighAccuracy: true,
                    timeout: 10000,
                    maximumAge: 300000
                }
            );
        } else {
            alert("Geolocation is not supported by this browser.");
        }
    }
    
    // Auto-request location on page load
    window.addEventListener('load', function() {
        setTimeout(getLocation, 1000);
    });
    </script>
    """
    
    # Render the JavaScript
    components.html(location_js, height=0)
    
    # Check if coordinates are available in session storage
    check_coords_js = """
    <script>
    function checkCoordinates() {
        const lat = sessionStorage.getItem('user_lat');
        const lon = sessionStorage.getItem('user_lon');
        
        if (lat && lon) {
            // Send to Streamlit
            window.parent.postMessage({
                type: 'streamlit:setComponentValue',
                key: 'location_coords',
                value: {lat: parseFloat(lat), lon: parseFloat(lon)}
            }, '*');
        }
    }
    
    // Check for coordinates every 2 seconds
    setInterval(checkCoordinates, 2000);
    </script>
    """
    
    components.html(check_coords_js, height=0)
    
    # Handle coordinates if available
    if 'location_coords' in st.session_state:
        coords = st.session_state.location_coords
        lat, lon = coords['lat'], coords['lon']
        
        # Reverse geocode to get address
        try:
            from geopy.geocoders import Nominatim
            geocoder = Nominatim(user_agent="arovia-health-desk")
            location_data = geocoder.reverse(f"{lat}, {lon}")
            
            if location_data:
                address = location_data.address
                return address, (lat, lon)
            else:
                return f"Coordinates: {lat:.4f}, {lon:.4f}", (lat, lon)
                
        except Exception as e:
            st.error(f"Error processing location: {e}")
            return f"Coordinates: {lat:.4f}, {lon:.4f}", (lat, lon)
    
    return None, None


def manual_location_input() -> Optional[str]:
    """
    Manual location input fallback
    
    Returns:
        Location string or None
    """
    st.markdown("**📝 Manual Location Entry**")
    
    location = st.text_input(
        "Enter your location:",
        placeholder="Example: Hyderabad, Telangana or Banjara Hills, Hyderabad",
        help="Enter your city, area, or full address for nearby clinic recommendations"
    )
    
    return location if location else None
