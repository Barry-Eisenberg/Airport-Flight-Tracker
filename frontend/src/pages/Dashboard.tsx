import { useQuery } from '@tanstack/react-query';
import { Plane, Building2, Users, ClipboardList, TrendingUp } from 'lucide-react';
import { dashboardApi } from '../services/api';
import { format } from 'date-fns';

export default function Dashboard() {
  const { data: stats, isLoading, error } = useQuery({
    queryKey: ['dashboard'],
    queryFn: dashboardApi.getStats,
  });

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <p className="text-red-400">Failed to load dashboard data</p>
      </div>
    );
  }

  return (
    <div>
      <h1 className="text-3xl font-bold text-white mb-8">Dashboard</h1>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard
          title="Flights Today"
          value={stats?.total_flights_today || 0}
          icon={<ClipboardList className="w-8 h-8" />}
          color="blue"
        />
        <StatCard
          title="Flights This Week"
          value={stats?.total_flights_week || 0}
          icon={<TrendingUp className="w-8 h-8" />}
          color="green"
        />
        <StatCard
          title="Registered Aircraft"
          value={stats?.total_aircraft || 0}
          icon={<Plane className="w-8 h-8" />}
          color="purple"
        />
        <StatCard
          title="Active Pilots"
          value={stats?.total_pilots || 0}
          icon={<Users className="w-8 h-8" />}
          color="orange"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Flights */}
        <div className="bg-slate-800 rounded-lg p-6">
          <h2 className="text-xl font-semibold text-white mb-4">Recent Flights</h2>
          {stats?.recent_flights && stats.recent_flights.length > 0 ? (
            <div className="space-y-3">
              {stats.recent_flights.slice(0, 5).map((flight) => (
                <div
                  key={flight.id}
                  className="flex items-center justify-between p-3 bg-slate-700 rounded-lg"
                >
                  <div>
                    <p className="text-white font-medium">
                      {flight.aircraft?.tail_number || 'N/A'} - {flight.operation}
                    </p>
                    <p className="text-slate-400 text-sm">
                      {flight.airport?.icao_code} • {flight.pilot?.last_name || 'Unknown'}
                    </p>
                  </div>
                  <span className="text-slate-400 text-sm">
                    {format(new Date(flight.actual_time), 'MMM d, HH:mm')}
                  </span>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-slate-400">No recent flights</p>
          )}
        </div>

        {/* Busiest Airports */}
        <div className="bg-slate-800 rounded-lg p-6">
          <h2 className="text-xl font-semibold text-white mb-4">Busiest Airports (This Week)</h2>
          {stats?.busiest_airports && stats.busiest_airports.length > 0 ? (
            <div className="space-y-3">
              {stats.busiest_airports.map((airport, index) => (
                <div
                  key={airport.id}
                  className="flex items-center justify-between p-3 bg-slate-700 rounded-lg"
                >
                  <div className="flex items-center gap-3">
                    <span className="text-2xl font-bold text-slate-500">#{index + 1}</span>
                    <div>
                      <p className="text-white font-medium">{airport.icao_code}</p>
                      <p className="text-slate-400 text-sm">{airport.name}</p>
                    </div>
                  </div>
                  <span className="text-blue-400 font-semibold">
                    {airport.flight_count} flights
                  </span>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-slate-400">No flight data available</p>
          )}
        </div>
      </div>
    </div>
  );
}

interface StatCardProps {
  title: string;
  value: number;
  icon: React.ReactNode;
  color: 'blue' | 'green' | 'purple' | 'orange';
}

function StatCard({ title, value, icon, color }: StatCardProps) {
  const colorClasses = {
    blue: 'bg-blue-500/20 text-blue-400',
    green: 'bg-green-500/20 text-green-400',
    purple: 'bg-purple-500/20 text-purple-400',
    orange: 'bg-orange-500/20 text-orange-400',
  };

  return (
    <div className="bg-slate-800 rounded-lg p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-slate-400 text-sm">{title}</p>
          <p className="text-3xl font-bold text-white mt-1">{value}</p>
        </div>
        <div className={`p-3 rounded-lg ${colorClasses[color]}`}>{icon}</div>
      </div>
    </div>
  );
}
