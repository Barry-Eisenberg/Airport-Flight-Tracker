import { useState, useCallback, useRef } from 'react';
import { GoogleMap, useJsApiLoader, Marker, InfoWindow } from '@react-google-maps/api';
import type { Airport } from '../types';

const mapContainerStyle = {
  width: '100%',
  height: '500px',
};

const defaultCenter = {
  lat: 39.8283,
  lng: -98.5795, // Center of USA
};

const mapOptions: google.maps.MapOptions = {
  disableDefaultUI: false,
  zoomControl: true,
  mapTypeControl: true,
  streetViewControl: false,
  styles: [
    {
      featureType: 'all',
      elementType: 'geometry',
      stylers: [{ color: '#1e293b' }],
    },
    {
      featureType: 'all',
      elementType: 'labels.text.stroke',
      stylers: [{ color: '#1e293b' }],
    },
    {
      featureType: 'all',
      elementType: 'labels.text.fill',
      stylers: [{ color: '#94a3b8' }],
    },
    {
      featureType: 'water',
      elementType: 'geometry',
      stylers: [{ color: '#0f172a' }],
    },
    {
      featureType: 'road',
      elementType: 'geometry',
      stylers: [{ color: '#334155' }],
    },
  ],
};

interface AirportMapProps {
  airports: Airport[];
  onAirportSelect?: (airport: Airport) => void;
  onMapClick?: (lat: number, lng: number) => void;
}

export default function AirportMap({ airports, onAirportSelect, onMapClick }: AirportMapProps) {
  const [selectedAirport, setSelectedAirport] = useState<Airport | null>(null);
  const [map, setMap] = useState<google.maps.Map | null>(null);
  const searchBoxRef = useRef<HTMLInputElement>(null);

  const { isLoaded, loadError } = useJsApiLoader({
    googleMapsApiKey: import.meta.env.VITE_GOOGLE_MAPS_API_KEY || '',
    libraries: ['places'],
  });

  const onLoad = useCallback((map: google.maps.Map) => {
    setMap(map);
    
    // Fit bounds to show all airports if we have any
    if (airports.length > 0) {
      const bounds = new google.maps.LatLngBounds();
      airports.forEach((airport) => {
        bounds.extend({ lat: airport.latitude, lng: airport.longitude });
      });
      map.fitBounds(bounds);
    }
  }, [airports]);

  const onUnmount = useCallback(() => {
    setMap(null);
  }, []);

  const handleMarkerClick = (airport: Airport) => {
    setSelectedAirport(airport);
    if (onAirportSelect) {
      onAirportSelect(airport);
    }
  };

  const handleMapClick = (e: google.maps.MapMouseEvent) => {
    setSelectedAirport(null);
    if (onMapClick && e.latLng) {
      onMapClick(e.latLng.lat(), e.latLng.lng());
    }
  };

  const handlePlaceSearch = () => {
    if (!searchBoxRef.current || !map) return;
    
    const service = new google.maps.places.PlacesService(map);
    const request = {
      query: searchBoxRef.current.value + ' airport',
      fields: ['name', 'geometry', 'formatted_address', 'types'],
    };

    service.textSearch(request, (results, status) => {
      if (status === google.maps.places.PlacesServiceStatus.OK && results && results[0]) {
        const place = results[0];
        if (place.geometry?.location) {
          map.panTo(place.geometry.location);
          map.setZoom(12);
        }
      }
    });
  };

  const getMarkerIcon = (airport: Airport): google.maps.Symbol => {
    const color = airport.has_tower ? '#3b82f6' : '#22c55e'; // Blue for towered, green for non-towered
    return {
      path: google.maps.SymbolPath.CIRCLE,
      fillColor: color,
      fillOpacity: 0.9,
      strokeColor: '#ffffff',
      strokeWeight: 2,
      scale: airport.has_tower ? 10 : 7,
    };
  };

  if (loadError) {
    return (
      <div className="bg-slate-800 rounded-lg p-8 text-center">
        <p className="text-red-400">Error loading Google Maps. Please check your API key.</p>
      </div>
    );
  }

  if (!isLoaded) {
    return (
      <div className="bg-slate-800 rounded-lg p-8 flex items-center justify-center" style={{ height: '500px' }}>
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500" />
      </div>
    );
  }

  return (
    <div className="bg-slate-800 rounded-lg overflow-hidden">
      {/* Search Bar */}
      <div className="p-4 border-b border-slate-700">
        <div className="flex gap-2">
          <input
            ref={searchBoxRef}
            type="text"
            placeholder="Search for airports or airstrips..."
            className="flex-1 px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:border-blue-500"
            onKeyDown={(e) => e.key === 'Enter' && handlePlaceSearch()}
          />
          <button
            onClick={handlePlaceSearch}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
          >
            Search
          </button>
        </div>
        <div className="flex items-center gap-4 mt-2 text-sm">
          <span className="flex items-center gap-1">
            <span className="w-3 h-3 rounded-full bg-blue-500"></span>
            <span className="text-slate-400">Towered Airport</span>
          </span>
          <span className="flex items-center gap-1">
            <span className="w-3 h-3 rounded-full bg-green-500"></span>
            <span className="text-slate-400">Non-Towered</span>
          </span>
        </div>
      </div>

      {/* Map */}
      <GoogleMap
        mapContainerStyle={mapContainerStyle}
        center={defaultCenter}
        zoom={4}
        onLoad={onLoad}
        onUnmount={onUnmount}
        onClick={handleMapClick}
        options={mapOptions}
      >
        {airports.map((airport) => (
          <Marker
            key={airport.id}
            position={{ lat: airport.latitude, lng: airport.longitude }}
            icon={getMarkerIcon(airport)}
            onClick={() => handleMarkerClick(airport)}
            title={`${airport.icao_code} - ${airport.name}`}
          />
        ))}

        {selectedAirport && (
          <InfoWindow
            position={{ lat: selectedAirport.latitude, lng: selectedAirport.longitude }}
            onCloseClick={() => setSelectedAirport(null)}
          >
            <div className="p-2 min-w-[200px]">
              <h3 className="font-bold text-lg text-gray-900">{selectedAirport.icao_code}</h3>
              <p className="text-gray-700">{selectedAirport.name}</p>
              <p className="text-gray-600 text-sm">{selectedAirport.city}, {selectedAirport.state}</p>
              <div className="mt-2 text-sm">
                <p><span className="font-medium">Type:</span> {selectedAirport.airport_type}</p>
                {selectedAirport.elevation_ft && (
                  <p><span className="font-medium">Elevation:</span> {selectedAirport.elevation_ft} ft</p>
                )}
                <p><span className="font-medium">Tower:</span> {selectedAirport.has_tower ? 'Yes' : 'No'}</p>
                {selectedAirport.ctaf_frequency && (
                  <p><span className="font-medium">CTAF:</span> {selectedAirport.ctaf_frequency}</p>
                )}
              </div>
            </div>
          </InfoWindow>
        )}
      </GoogleMap>
    </div>
  );
}
