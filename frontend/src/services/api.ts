/**
 * API client for Airport Flight Tracker
 */
import axios from 'axios';
import type {
  Airport,
  Aircraft,
  Pilot,
  Flight,
  AirportCreate,
  AircraftCreate,
  PilotCreate,
  FlightCreate,
  DashboardStats,
} from '../types';

// Use environment variable for API URL, fallback to relative path for production
const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Airports
export const airportApi = {
  list: (params?: { state?: string; search?: string }) =>
    api.get<Airport[]>('/airports', { params }).then((res) => res.data),
  
  get: (id: number) =>
    api.get<Airport>(`/airports/${id}`).then((res) => res.data),
  
  getByCode: (icaoCode: string) =>
    api.get<Airport>(`/airports/code/${icaoCode}`).then((res) => res.data),
  
  create: (data: AirportCreate) =>
    api.post<Airport>('/airports', data).then((res) => res.data),
  
  update: (id: number, data: Partial<Airport>) =>
    api.patch<Airport>(`/airports/${id}`, data).then((res) => res.data),
  
  delete: (id: number) =>
    api.delete(`/airports/${id}`),
};

// Aircraft
export const aircraftApi = {
  list: (params?: { category?: string; search?: string; is_active?: boolean }) =>
    api.get<Aircraft[]>('/aircraft', { params }).then((res) => res.data),
  
  get: (id: number) =>
    api.get<Aircraft>(`/aircraft/${id}`).then((res) => res.data),
  
  getByTail: (tailNumber: string) =>
    api.get<Aircraft>(`/aircraft/tail/${tailNumber}`).then((res) => res.data),
  
  create: (data: AircraftCreate) =>
    api.post<Aircraft>('/aircraft', data).then((res) => res.data),
  
  update: (id: number, data: Partial<Aircraft>) =>
    api.patch<Aircraft>(`/aircraft/${id}`, data).then((res) => res.data),
  
  delete: (id: number) =>
    api.delete(`/aircraft/${id}`),
};

// Pilots
export const pilotApi = {
  list: (params?: { certificate_type?: string; search?: string; is_active?: boolean }) =>
    api.get<Pilot[]>('/pilots', { params }).then((res) => res.data),
  
  get: (id: number) =>
    api.get<Pilot>(`/pilots/${id}`).then((res) => res.data),
  
  getByCertificate: (certificateNumber: string) =>
    api.get<Pilot>(`/pilots/certificate/${certificateNumber}`).then((res) => res.data),
  
  create: (data: PilotCreate) =>
    api.post<Pilot>('/pilots', data).then((res) => res.data),
  
  update: (id: number, data: Partial<Pilot>) =>
    api.patch<Pilot>(`/pilots/${id}`, data).then((res) => res.data),
  
  delete: (id: number) =>
    api.delete(`/pilots/${id}`),
};

// Flights
export const flightApi = {
  list: (params?: {
    airport_id?: number;
    aircraft_id?: number;
    pilot_id?: number;
    pilot_name?: string;
    flight_type?: string;
    operation?: string;
    date_from?: string;
    date_to?: string;
    years_back?: number;
    limit?: number;
  }) =>
    api.get<Flight[]>('/flights', { params }).then((res) => res.data),
  
  get: (id: number) =>
    api.get<Flight>(`/flights/${id}`).then((res) => res.data),
  
  getPilotHistory: (pilotId: number, yearsBack: number = 10, limit: number = 500) =>
    api.get<Flight[]>(`/flights/pilot-history/${pilotId}`, { 
      params: { years_back: yearsBack, limit } 
    }).then((res) => res.data),
  
  create: (data: FlightCreate) =>
    api.post<Flight>('/flights', data).then((res) => res.data),
  
  update: (id: number, data: Partial<Flight>) =>
    api.patch<Flight>(`/flights/${id}`, data).then((res) => res.data),
  
  delete: (id: number) =>
    api.delete(`/flights/${id}`),
};

// Dashboard
export const dashboardApi = {
  getStats: () =>
    api.get<DashboardStats>('/dashboard').then((res) => res.data),
};

export default api;
