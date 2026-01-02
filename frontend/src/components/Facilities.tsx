import React, { useState, useEffect } from 'react';
import { MapPinIcon, PhoneIcon, ClockIcon } from '@heroicons/react/24/outline';
import type { Facility } from '../types';

interface FacilitiesProps {
  facilities: Facility[];
  loading: boolean;
}

const Facilities: React.FC<FacilitiesProps> = ({ facilities, loading }) => {
  const [searchLocation, setSearchLocation] = useState('');
  const [filteredFacilities, setFilteredFacilities] = useState<Facility[]>(facilities);

  useEffect(() => {
    setFilteredFacilities(facilities);
  }, [facilities]);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchLocation.trim()) return;

    try {
      const response = await fetch('http://localhost:8000/facilities', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ location: searchLocation }),
      });

      if (response.ok) {
        const data = await response.json();
        setFilteredFacilities(data);
      }
    } catch (error) {
      console.error('Error searching facilities:', error);
    }
  };

  const getFacilityTypeColor = (type: string) => {
    switch (type) {
      case 'government': return 'bg-blue-100 text-blue-800';
      case 'private': return 'bg-green-100 text-green-800';
      case 'ngo': return 'bg-yellow-100 text-yellow-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getFacilityTypeIcon = (type: string) => {
    switch (type) {
      case 'government': return '🏛️';
      case 'private': return '🏥';
      case 'ngo': return '🤝';
      default: return '🏢';
    }
  };

  if (loading) {
    return (
      <div className="max-w-6xl mx-auto">
        <div className="card text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Finding Facilities</h2>
          <p className="text-gray-600">Searching for nearby healthcare centers...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto">
      {/* Header */}
      <div className="card mb-6">
        <div className="flex items-center mb-6">
          <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center mr-4">
            <MapPinIcon className="w-6 h-6 text-purple-600" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Healthcare Facilities</h1>
            <p className="text-gray-600">Find nearby medical centers and hospitals</p>
          </div>
        </div>

        {/* Search Form */}
        <form onSubmit={handleSearch} className="flex gap-4">
          <div className="flex-1">
            <input
              type="text"
              value={searchLocation}
              onChange={(e) => setSearchLocation(e.target.value)}
              placeholder="Enter city, state (e.g., Mumbai, Maharashtra)"
              className="input-field"
            />
          </div>
          <button type="submit" className="btn-primary">
            Search
          </button>
        </form>
      </div>

      {/* Results */}
      {filteredFacilities.length > 0 ? (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold text-gray-900">
              Found {filteredFacilities.length} facilities
            </h2>
            <div className="text-sm text-gray-600">
              Sorted by distance
            </div>
          </div>

          {filteredFacilities.map((facility, index) => (
            <div key={index} className="card hover:shadow-md transition-shadow duration-200">
              <div className="flex justify-between items-start mb-4">
                <div className="flex-1">
                  <div className="flex items-center space-x-3 mb-2">
                    <h3 className="text-lg font-semibold text-gray-900">{facility.name}</h3>
                    <span className={`status-badge ${getFacilityTypeColor(facility.facility_type)}`}>
                      {getFacilityTypeIcon(facility.facility_type)} {facility.facility_type}
                    </span>
                    {index === 0 && (
                      <span className="status-badge bg-yellow-100 text-yellow-800">
                        ⭐ Recommended
                      </span>
                    )}
                  </div>

                  <div className="flex items-center text-gray-600 mb-2">
                    <MapPinIcon className="w-4 h-4 mr-1" />
                    <span className="text-sm">{facility.address}</span>
                  </div>

                  <div className="flex items-center space-x-4 text-sm text-gray-600">
                    <span className="flex items-center">
                      <ClockIcon className="w-4 h-4 mr-1" />
                      {facility.distance_km} km away
                    </span>
                    <span className="text-blue-600 font-medium">{facility.specialty_match}</span>
                  </div>
                </div>

                <div className="text-right">
                  <div className="text-2xl font-bold text-primary-600">
                    #{index + 1}
                  </div>
                  <div className="text-sm text-gray-500">Priority</div>
                </div>
              </div>

              {/* Services */}
              {facility.services.length > 0 && (
                <div className="mb-4">
                  <h4 className="text-sm font-medium text-gray-700 mb-2">Services Available:</h4>
                  <div className="flex flex-wrap gap-2">
                    {facility.services.map((service, serviceIndex) => (
                      <span
                        key={serviceIndex}
                        className="px-2 py-1 bg-gray-100 text-gray-700 rounded-md text-xs"
                      >
                        {service}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Contact and Actions */}
              <div className="flex items-center justify-between pt-4 border-t border-gray-200">
                <div className="flex items-center space-x-4">
                  {facility.contact && (
                    <div className="flex items-center text-sm text-gray-600">
                      <PhoneIcon className="w-4 h-4 mr-1" />
                      <span>{facility.contact}</span>
                    </div>
                  )}
                  <a
                    href={facility.map_link}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                  >
                    View on Map →
                  </a>
                </div>

                <div className="flex space-x-2">
                  <button className="btn-secondary text-sm">
                    Save
                  </button>
                  <button className="btn-primary text-sm">
                    Get Directions
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="card text-center">
          <MapPinIcon className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">No Facilities Found</h3>
          <p className="text-gray-600 mb-4">
            Try searching for a different location or check your spelling.
          </p>
          <button
            onClick={() => setSearchLocation('')}
            className="btn-primary"
          >
            Clear Search
          </button>
        </div>
      )}
    </div>
  );
};

export default Facilities;
