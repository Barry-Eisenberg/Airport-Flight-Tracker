import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Plus, Search, Plane, Calendar, FileDown } from 'lucide-react';
import { format } from 'date-fns';
import { flightApi, airportApi } from '../services/api';
import { exportFlightsPDF } from '../utils/pdfExport';

export default function Flights() {
  const [search, setSearch] = useState('');
  const [flightType, setFlightType] = useState('');
  const [airportId, setAirportId] = useState('');
  const [dateFrom, setDateFrom] = useState('');
  const [dateTo, setDateTo] = useState('');

  const { data: flights, isLoading } = useQuery({
    queryKey: ['flights', { search, flightType, airportId, dateFrom, dateTo }],
    queryFn: () => flightApi.list({ 
      flight_type: flightType || undefined,
      airport_id: airportId ? parseInt(airportId) : undefined,
      date_from: dateFrom || undefined,
      date_to: dateTo || undefined,
    }),
  });

  const { data: airports } = useQuery({
    queryKey: ['airports'],
    queryFn: () => airportApi.list({}),
  });

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-3xl font-bold text-white">Flight Logs</h1>
        <div className="flex gap-2">
          <button 
            onClick={() => flights && exportFlightsPDF(flights)}
            disabled={!flights || flights.length === 0}
            className="flex items-center gap-2 bg-slate-600 hover:bg-slate-500 disabled:opacity-50 disabled:cursor-not-allowed text-white px-4 py-2 rounded-lg transition-colors"
          >
            <FileDown className="w-5 h-5" />
            Export PDF
          </button>
          <button className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors">
            <Plus className="w-5 h-5" />
            Log Flight
          </button>
        </div>
      </div>

      {/* Filters */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 mb-6">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
          <input
            type="text"
            placeholder="Search flights..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-10 pr-4 py-2 bg-slate-800 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:border-blue-500"
          />
        </div>
        <select
          value={flightType}
          onChange={(e) => setFlightType(e.target.value)}
          className="px-4 py-2 bg-slate-800 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
        >
          <option value="">All Types</option>
          <option value="local">Local</option>
          <option value="cross_country">Cross Country</option>
          <option value="training">Training</option>
          <option value="charter">Charter</option>
          <option value="cargo">Cargo</option>
          <option value="other">Other</option>
        </select>
        <select
          value={airportId}
          onChange={(e) => setAirportId(e.target.value)}
          className="px-4 py-2 bg-slate-800 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
        >
          <option value="">All Airports</option>
          {airports?.map((airport) => (
            <option key={airport.id} value={airport.id}>
              {airport.faa_code} - {airport.name}
            </option>
          ))}
        </select>
        <div className="relative">
          <Calendar className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
          <input
            type="date"
            value={dateFrom}
            onChange={(e) => setDateFrom(e.target.value)}
            placeholder="From date"
            className="w-full pl-10 pr-4 py-2 bg-slate-800 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
          />
        </div>
        <div className="relative">
          <Calendar className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
          <input
            type="date"
            value={dateTo}
            onChange={(e) => setDateTo(e.target.value)}
            placeholder="To date"
            className="w-full pl-10 pr-4 py-2 bg-slate-800 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
          />
        </div>
      </div>

      {/* Table */}
      <div className="bg-slate-800 rounded-lg overflow-hidden">
        <table className="w-full">
          <thead className="bg-slate-700">
            <tr>
              <th className="text-left p-4 text-slate-300">Date/Time</th>
              <th className="text-left p-4 text-slate-300">Aircraft</th>
              <th className="text-left p-4 text-slate-300">Route</th>
              <th className="text-left p-4 text-slate-300">Type</th>
              <th className="text-left p-4 text-slate-300">Pilot</th>
              <th className="text-left p-4 text-slate-300">PAX</th>
              <th className="text-left p-4 text-slate-300">Operation</th>
            </tr>
          </thead>
          <tbody>
            {isLoading ? (
              <tr>
                <td colSpan={7} className="p-8 text-center text-slate-400">
                  Loading...
                </td>
              </tr>
            ) : flights && flights.length > 0 ? (
              flights.map((flight) => (
                <tr key={flight.id} className="border-t border-slate-700 hover:bg-slate-700/50">
                  <td className="p-4 text-slate-300">
                    {format(new Date(flight.actual_time), 'MMM d, yyyy HH:mm')}
                  </td>
                  <td className="p-4">
                    <div className="flex items-center gap-2">
                      <Plane className="w-4 h-4 text-blue-400" />
                      <span className="text-white font-mono">{flight.aircraft?.tail_number || '-'}</span>
                    </div>
                  </td>
                  <td className="p-4 text-white">
                    <span className="text-blue-400">{flight.origin_airport || flight.airport?.faa_code || '???'}</span>
                    <span className="text-slate-500 mx-2">→</span>
                    <span className="text-green-400">{flight.destination_airport || '???'}</span>
                  </td>
                  <td className="p-4">
                    <span className={`px-2 py-1 rounded text-sm ${getFlightTypeColor(flight.flight_type)}`}>
                      {formatFlightType(flight.flight_type)}
                    </span>
                  </td>
                  <td className="p-4 text-slate-300">
                    {flight.pilot ? `${flight.pilot.first_name} ${flight.pilot.last_name}` : '-'}
                  </td>
                  <td className="p-4 text-slate-300">{flight.passengers}</td>
                  <td className="p-4">
                    <OperationBadge operation={flight.operation} />
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={7} className="p-8 text-center text-slate-400">
                  No flights found
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
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
