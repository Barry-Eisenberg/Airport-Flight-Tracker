import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Plus, Search, User, Clock, Plane } from 'lucide-react';
import { format } from 'date-fns';
import { pilotApi, flightApi } from '../services/api';
import type { Pilot } from '../types';

export default function Pilots() {
  const [pilotSearch, setPilotSearch] = useState('');
  const [yearsBack, setYearsBack] = useState('10');
  const [certificateType, setCertificateType] = useState('');
  const [selectedPilot, setSelectedPilot] = useState<Pilot | null>(null);

  // Search for pilots
  const { data: pilots, isLoading: pilotsLoading } = useQuery({
    queryKey: ['pilots', { search: pilotSearch, certificateType }],
    queryFn: () => pilotApi.list({ 
      search: pilotSearch || undefined, 
      certificate_type: certificateType || undefined 
    }),
    enabled: pilotSearch.length > 0 || certificateType.length > 0,
  });

  // Get flight history for selected pilot
  const { data: pilotFlights, isLoading: flightsLoading, isFetching } = useQuery({
    queryKey: ['pilot-flights', selectedPilot?.id, yearsBack],
    queryFn: () => flightApi.getPilotHistory(selectedPilot!.id, parseInt(yearsBack), 500),
    enabled: !!selectedPilot,
  });

  const handlePilotSelect = (pilot: Pilot) => {
    setSelectedPilot(pilot);
  };

  const handleClearSelection = () => {
    setSelectedPilot(null);
  };

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-3xl font-bold text-white">Pilot Flight History</h1>
          <p className="text-slate-400 mt-1">Search for a pilot to view their complete flight history</p>
        </div>
        <button className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors">
          <Plus className="w-5 h-5" />
          Add Pilot
        </button>
      </div>

      {/* Pilot Search - Primary Filter */}
      <div className="bg-slate-800 rounded-lg p-4 mb-4">
        <div className="flex items-center gap-2 mb-3">
          <User className="w-5 h-5 text-blue-400" />
          <span className="text-white font-medium">Search for Pilot</span>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="relative md:col-span-2">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
            <input
              type="text"
              placeholder="Enter pilot name (first or last name)..."
              value={pilotSearch}
              onChange={(e) => {
                setPilotSearch(e.target.value);
                if (selectedPilot) setSelectedPilot(null);
              }}
              className="w-full pl-10 pr-4 py-3 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:border-blue-500 text-lg"
            />
          </div>
          <select
            value={certificateType}
            onChange={(e) => setCertificateType(e.target.value)}
            className="px-4 py-3 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
          >
            <option value="">All Certificates</option>
            <option value="student">Student</option>
            <option value="sport">Sport</option>
            <option value="recreational">Recreational</option>
            <option value="private">Private</option>
            <option value="commercial">Commercial</option>
            <option value="atp">ATP</option>
          </select>
          <div className="flex items-center gap-2">
            <Clock className="w-5 h-5 text-slate-400" />
            <select
              value={yearsBack}
              onChange={(e) => setYearsBack(e.target.value)}
              className="flex-1 px-4 py-3 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
            >
              <option value="1">Last 1 year</option>
              <option value="5">Last 5 years</option>
              <option value="10">Last 10 years</option>
              <option value="15">Last 15 years</option>
              <option value="20">Last 20 years</option>
              <option value="30">Last 30 years</option>
              <option value="50">All time (50 years)</option>
            </select>
          </div>
        </div>
      </div>

      {/* Pilot Search Results */}
      {pilotSearch && !selectedPilot && (
        <div className="bg-slate-800 rounded-lg p-4 mb-4">
          <h3 className="text-white font-medium mb-3">
            {pilotsLoading ? 'Searching...' : `Found ${pilots?.length || 0} pilots matching "${pilotSearch}"`}
          </h3>
          {pilots && pilots.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
              {pilots.map((pilot) => (
                <button
                  key={pilot.id}
                  onClick={() => handlePilotSelect(pilot)}
                  className="flex items-center gap-3 p-3 bg-slate-700 hover:bg-slate-600 rounded-lg transition-colors text-left"
                >
                  <div className="w-10 h-10 bg-blue-500/20 rounded-full flex items-center justify-center">
                    <User className="w-5 h-5 text-blue-400" />
                  </div>
                  <div>
                    <div className="text-white font-medium">{pilot.first_name} {pilot.last_name}</div>
                    <div className="text-slate-400 text-sm">
                      {pilot.certificate_type.toUpperCase()} • {pilot.total_flight_hours.toFixed(0)} hrs
                    </div>
                  </div>
                </button>
              ))}
            </div>
          ) : !pilotsLoading ? (
            <p className="text-slate-400">No pilots found. Try a different search term.</p>
          ) : null}
        </div>
      )}

      {/* Selected Pilot Info & Flight History */}
      {selectedPilot && (
        <>
          {/* Pilot Card */}
          <div className="bg-gradient-to-r from-blue-900/50 to-slate-800 border border-blue-500/30 rounded-lg p-4 mb-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <div className="w-14 h-14 bg-blue-500/20 rounded-full flex items-center justify-center">
                  <User className="w-7 h-7 text-blue-400" />
                </div>
                <div>
                  <h2 className="text-2xl font-bold text-white">{selectedPilot.first_name} {selectedPilot.last_name}</h2>
                  <div className="flex items-center gap-4 mt-1">
                    <span className={`px-2 py-1 rounded text-sm ${getCertificateColor(selectedPilot.certificate_type)}`}>
                      {selectedPilot.certificate_type.toUpperCase()}
                    </span>
                    <span className="text-slate-400">Certificate: {selectedPilot.certificate_number}</span>
                    <span className="text-slate-400">{selectedPilot.total_flight_hours.toFixed(1)} total hours</span>
                    {selectedPilot.city && selectedPilot.state && (
                      <span className="text-slate-400">{selectedPilot.city}, {selectedPilot.state}</span>
                    )}
                  </div>
                </div>
              </div>
              <button
                onClick={handleClearSelection}
                className="px-4 py-2 bg-slate-700 hover:bg-slate-600 text-white rounded-lg transition-colors"
              >
                Search Another Pilot
              </button>
            </div>
          </div>

          {/* Results Summary */}
          <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-4 mb-4">
            <div className="flex items-center justify-between">
              <div>
                <span className="text-slate-400">Found </span>
                <span className="text-white font-bold text-xl">{pilotFlights?.length || 0}</span>
                <span className="text-slate-400"> flights in the last {yearsBack} year{parseInt(yearsBack) !== 1 ? 's' : ''}</span>
              </div>
              {isFetching && (
                <span className="text-slate-400 text-sm">Loading flight history...</span>
              )}
            </div>
          </div>

          {/* Flight History Table */}
          <div className="bg-slate-800 rounded-lg overflow-hidden">
            <table className="w-full">
              <thead className="bg-slate-700">
                <tr>
                  <th className="text-left p-4 text-slate-300">Date/Time</th>
                  <th className="text-left p-4 text-slate-300">Aircraft</th>
                  <th className="text-left p-4 text-slate-300">Airport</th>
                  <th className="text-left p-4 text-slate-300">Route</th>
                  <th className="text-left p-4 text-slate-300">Flight Type</th>
                  <th className="text-left p-4 text-slate-300">Operation</th>
                  <th className="text-left p-4 text-slate-300">PAX</th>
                </tr>
              </thead>
              <tbody>
                {flightsLoading ? (
                  <tr>
                    <td colSpan={7} className="p-8 text-center text-slate-400">
                      Loading flight history...
                    </td>
                  </tr>
                ) : pilotFlights && pilotFlights.length > 0 ? (
                  pilotFlights.map((flight) => (
                    <tr key={flight.id} className="border-t border-slate-700 hover:bg-slate-700/50">
                      <td className="p-4 text-slate-300">
                        {format(new Date(flight.actual_time), 'MMM d, yyyy HH:mm')}
                      </td>
                      <td className="p-4">
                        <div className="flex items-center gap-2">
                          <Plane className="w-4 h-4 text-blue-400" />
                          <span className="text-white font-mono">{flight.aircraft?.tail_number || '-'}</span>
                        </div>
                        {flight.aircraft && (
                          <div className="text-slate-500 text-sm">
                            {flight.aircraft.manufacturer} {flight.aircraft.model}
                          </div>
                        )}
                      </td>
                      <td className="p-4 text-white">
                        {flight.airport?.faa_code || flight.airport?.icao_code || '-'}
                        {flight.airport && (
                          <div className="text-slate-500 text-sm">{flight.airport.name}</div>
                        )}
                      </td>
                      <td className="p-4 text-white">
                        <span className="text-blue-400">{flight.origin_airport || '???'}</span>
                        <span className="text-slate-500 mx-2">→</span>
                        <span className="text-green-400">{flight.destination_airport || '???'}</span>
                      </td>
                      <td className="p-4">
                        <span className={`px-2 py-1 rounded text-sm ${getFlightTypeColor(flight.flight_type)}`}>
                          {formatFlightType(flight.flight_type)}
                        </span>
                      </td>
                      <td className="p-4">
                        <OperationBadge operation={flight.operation} />
                      </td>
                      <td className="p-4 text-slate-300">{flight.passengers}</td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan={7} className="p-8 text-center text-slate-400">
                      No flights found for this pilot in the selected time period
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </>
      )}

      {/* Initial State - No Search */}
      {!pilotSearch && !selectedPilot && (
        <div className="bg-slate-800/50 border border-slate-700 border-dashed rounded-lg p-12 text-center">
          <User className="w-16 h-16 text-slate-600 mx-auto mb-4" />
          <h3 className="text-xl font-medium text-slate-400 mb-2">Search for a Pilot</h3>
          <p className="text-slate-500">Enter a pilot's name above to view their complete flight history</p>
        </div>
      )}
    </div>
  );
}

function OperationBadge({ operation }: { operation: string }) {
  const styles: Record<string, string> = {
    takeoff: 'bg-blue-500/20 text-blue-400',
    landing: 'bg-green-500/20 text-green-400',
    touch_and_go: 'bg-purple-500/20 text-purple-400',
  };
  const labels: Record<string, string> = {
    takeoff: 'Takeoff',
    landing: 'Landing',
    touch_and_go: 'Touch & Go',
  };
  return (
    <span className={`px-2 py-1 rounded text-sm ${styles[operation] || 'bg-slate-500/20 text-slate-400'}`}>
      {labels[operation] || operation}
    </span>
  );
}

function getCertificateColor(cert: string): string {
  const colors: Record<string, string> = {
    student: 'bg-yellow-500/20 text-yellow-400',
    sport: 'bg-cyan-500/20 text-cyan-400',
    recreational: 'bg-teal-500/20 text-teal-400',
    private: 'bg-blue-500/20 text-blue-400',
    commercial: 'bg-purple-500/20 text-purple-400',
    atp: 'bg-green-500/20 text-green-400',
  };
  return colors[cert] || 'bg-slate-500/20 text-slate-400';
}

function getFlightTypeColor(type: string): string {
  const colors: Record<string, string> = {
    local: 'bg-blue-500/20 text-blue-400',
    cross_country: 'bg-purple-500/20 text-purple-400',
    training: 'bg-yellow-500/20 text-yellow-400',
    charter: 'bg-green-500/20 text-green-400',
    cargo: 'bg-orange-500/20 text-orange-400',
    other: 'bg-slate-500/20 text-slate-400',
  };
  return colors[type] || 'bg-slate-500/20 text-slate-400';
}

function formatFlightType(type: string): string {
  const labels: Record<string, string> = {
    local: 'Local',
    cross_country: 'Cross Country',
    training: 'Training',
    charter: 'Charter',
    cargo: 'Cargo',
    other: 'Other',
  };
  return labels[type] || type;
}
