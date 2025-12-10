/**
 * TypeScript types for Airport Flight Tracker
 */

// Enums
export type AircraftCategory = 
  | 'single_engine'
  | 'multi_engine'
  | 'jet'
  | 'helicopter'
  | 'glider'
  | 'balloon'
  | 'other';

export type PilotCertificate = 
  | 'student'
  | 'sport'
  | 'recreational'
  | 'private'
  | 'commercial'
  | 'atp';

export type FlightType = 
  | 'training'
  | 'pleasure'
  | 'business'
  | 'charter'
  | 'maintenance'
  | 'other';

export type FlightOperation = 'takeoff' | 'landing' | 'touch_and_go';

// Models
export interface Airport {
  id: number;
  icao_code: string;
  faa_code?: string;
  name: string;
  city: string;
  state: string;
  county?: string;
  latitude: number;
  longitude: number;
  elevation_ft?: number;
  airport_type: string;
  ownership?: string;
  runways?: string;
  fuel_types?: string;
  has_tower: boolean;
  ctaf_frequency?: string;
  created_at: string;
  updated_at: string;
}

export interface Aircraft {
  id: number;
  tail_number: string;
  manufacturer: string;
  model: string;
  year_built?: number;
  category: AircraftCategory;
  engine_type?: string;
  num_engines: number;
  max_passengers?: number;
  owner_name: string;
  owner_address?: string;
  owner_city?: string;
  owner_state?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Pilot {
  id: number;
  certificate_number: string;
  first_name: string;
  last_name: string;
  certificate_type: PilotCertificate;
  ratings?: string;
  medical_class?: string;
  medical_expiry?: string;
  total_flight_hours: number;
  email?: string;
  phone?: string;
  city?: string;
  state?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Flight {
  id: number;
  airport_id: number;
  aircraft_id: number;
  pic_id: number;
  flight_type: FlightType;
  operation: string;
  runway?: string;
  scheduled_time?: string;
  actual_time: string;
  origin_airport?: string;
  destination_airport?: string;
  passengers: number;
  cargo_weight_lbs?: number;
  fuel_gallons?: number;
  remarks?: string;
  squawk_code?: string;
  airport?: Airport;
  aircraft?: Aircraft;
  pilot?: Pilot;
  created_at: string;
  updated_at: string;
}

// Form types
export interface AirportCreate {
  icao_code: string;
  faa_code?: string;
  name: string;
  city: string;
  state: string;
  latitude: number;
  longitude: number;
  elevation_ft?: number;
  airport_type?: string;
  has_tower?: boolean;
}

export interface AircraftCreate {
  tail_number: string;
  manufacturer: string;
  model: string;
  year_built?: number;
  category: AircraftCategory;
  engine_type?: string;
  num_engines?: number;
  max_passengers?: number;
  owner_name: string;
  owner_city?: string;
  owner_state?: string;
}

export interface PilotCreate {
  certificate_number: string;
  first_name: string;
  last_name: string;
  certificate_type: PilotCertificate;
  total_flight_hours?: number;
  email?: string;
  phone?: string;
  city?: string;
  state?: string;
}

export interface FlightCreate {
  airport_id: number;
  aircraft_id: number;
  pic_id: number;
  flight_type: FlightType;
  operation: string;
  runway?: string;
  actual_time?: string;
  origin_airport?: string;
  destination_airport?: string;
  passengers?: number;
  remarks?: string;
}

// Dashboard
export interface DashboardStats {
  total_flights_today: number;
  total_flights_week: number;
  total_aircraft: number;
  total_pilots: number;
  total_airports: number;
  recent_flights: Flight[];
  busiest_airports: {
    id: number;
    icao_code: string;
    name: string;
    flight_count: number;
  }[];
}
