import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Plus, Search } from 'lucide-react';
import { airportApi } from '../services/api';

export default function Airports() {
  const [search, setSearch] = useState('');
  const [state, setState] = useState('');

  const { data: airports, isLoading } = useQuery({
    queryKey: ['airports', { search, state }],
    queryFn: () => airportApi.list({ search: search || undefined, state: state || undefined }),
  });

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-3xl font-bold text-white">Airports</h1>
        <button className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors">
          <Plus className="w-5 h-5" />
          Add Airport
        </button>
      </div>

      {/* Filters */}
      <div className="flex gap-4 mb-6">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
          <input
            type="text"
            placeholder="Search airports..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-10 pr-4 py-2 bg-slate-800 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:border-blue-500"
          />
        </div>
        <select
          value={state}
          onChange={(e) => setState(e.target.value)}
          className="px-4 py-2 bg-slate-800 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
        >
          <option value="">All States</option>
          {US_STATES.map((s) => (
            <option key={s} value={s}>{s}</option>
          ))}
        </select>
      </div>

      {/* Table */}
      <div className="bg-slate-800 rounded-lg overflow-hidden">
        <table className="w-full">
          <thead className="bg-slate-700">
            <tr>
              <th className="text-left p-4 text-slate-300">ICAO</th>
              <th className="text-left p-4 text-slate-300">Name</th>
              <th className="text-left p-4 text-slate-300">City</th>
              <th className="text-left p-4 text-slate-300">State</th>
              <th className="text-left p-4 text-slate-300">Type</th>
              <th className="text-left p-4 text-slate-300">Tower</th>
            </tr>
          </thead>
          <tbody>
            {isLoading ? (
              <tr>
                <td colSpan={6} className="p-8 text-center text-slate-400">
                  Loading...
                </td>
              </tr>
            ) : airports && airports.length > 0 ? (
              airports.map((airport) => (
                <tr key={airport.id} className="border-t border-slate-700 hover:bg-slate-700/50">
                  <td className="p-4 text-blue-400 font-mono">{airport.icao_code}</td>
                  <td className="p-4 text-white">{airport.name}</td>
                  <td className="p-4 text-slate-300">{airport.city}</td>
                  <td className="p-4 text-slate-300">{airport.state}</td>
                  <td className="p-4 text-slate-300">{airport.airport_type}</td>
                  <td className="p-4">
                    {airport.has_tower ? (
                      <span className="text-green-400">Yes</span>
                    ) : (
                      <span className="text-slate-500">No</span>
                    )}
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={6} className="p-8 text-center text-slate-400">
                  No airports found
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

const US_STATES = [
  'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
  'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
  'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
  'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
  'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
];
