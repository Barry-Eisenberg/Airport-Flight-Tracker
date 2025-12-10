import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Plus, Search } from 'lucide-react';
import { aircraftApi } from '../services/api';

export default function Aircraft() {
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('');

  const { data: aircraft, isLoading } = useQuery({
    queryKey: ['aircraft', { search, category }],
    queryFn: () => aircraftApi.list({ 
      search: search || undefined, 
      category: category || undefined 
    }),
  });

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-3xl font-bold text-white">Aircraft Registry</h1>
        <button className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors">
          <Plus className="w-5 h-5" />
          Register Aircraft
        </button>
      </div>

      {/* Filters */}
      <div className="flex gap-4 mb-6">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
          <input
            type="text"
            placeholder="Search by tail number or owner..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-10 pr-4 py-2 bg-slate-800 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:border-blue-500"
          />
        </div>
        <select
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          className="px-4 py-2 bg-slate-800 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
        >
          <option value="">All Categories</option>
          <option value="single_engine">Single Engine</option>
          <option value="multi_engine">Multi Engine</option>
          <option value="jet">Jet</option>
          <option value="helicopter">Helicopter</option>
          <option value="glider">Glider</option>
        </select>
      </div>

      {/* Table */}
      <div className="bg-slate-800 rounded-lg overflow-hidden">
        <table className="w-full">
          <thead className="bg-slate-700">
            <tr>
              <th className="text-left p-4 text-slate-300">Tail #</th>
              <th className="text-left p-4 text-slate-300">Make/Model</th>
              <th className="text-left p-4 text-slate-300">Category</th>
              <th className="text-left p-4 text-slate-300">Year</th>
              <th className="text-left p-4 text-slate-300">Owner</th>
              <th className="text-left p-4 text-slate-300">Status</th>
            </tr>
          </thead>
          <tbody>
            {isLoading ? (
              <tr>
                <td colSpan={6} className="p-8 text-center text-slate-400">
                  Loading...
                </td>
              </tr>
            ) : aircraft && aircraft.length > 0 ? (
              aircraft.map((ac) => (
                <tr key={ac.id} className="border-t border-slate-700 hover:bg-slate-700/50">
                  <td className="p-4 text-blue-400 font-mono font-bold">{ac.tail_number}</td>
                  <td className="p-4 text-white">{ac.manufacturer} {ac.model}</td>
                  <td className="p-4 text-slate-300 capitalize">{ac.category.replace('_', ' ')}</td>
                  <td className="p-4 text-slate-300">{ac.year_built || '-'}</td>
                  <td className="p-4 text-slate-300">{ac.owner_name}</td>
                  <td className="p-4">
                    {ac.is_active ? (
                      <span className="px-2 py-1 bg-green-500/20 text-green-400 text-sm rounded">Active</span>
                    ) : (
                      <span className="px-2 py-1 bg-red-500/20 text-red-400 text-sm rounded">Inactive</span>
                    )}
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={6} className="p-8 text-center text-slate-400">
                  No aircraft found
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
