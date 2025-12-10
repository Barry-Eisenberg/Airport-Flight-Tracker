import { ReactNode } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Plane, Building2, Users, ClipboardList, LayoutDashboard } from 'lucide-react';

interface LayoutProps {
  children: ReactNode;
}

const navItems = [
  { path: '/', label: 'Dashboard', icon: LayoutDashboard },
  { path: '/flights', label: 'Flights', icon: ClipboardList },
  { path: '/airports', label: 'Airports', icon: Building2 },
  { path: '/aircraft', label: 'Aircraft', icon: Plane },
  { path: '/pilots', label: 'Pilots', icon: Users },
];

export default function Layout({ children }: LayoutProps) {
  const location = useLocation();

  return (
    <div className="min-h-screen flex">
      {/* Sidebar */}
      <aside className="w-64 bg-slate-800 border-r border-slate-700">
        <div className="p-4 border-b border-slate-700">
          <Link to="/" className="flex items-center gap-2 text-xl font-bold text-white">
            <Plane className="w-8 h-8 text-blue-500" />
            Flight Tracker
          </Link>
        </div>
        <nav className="p-4">
          <ul className="space-y-2">
            {navItems.map(({ path, label, icon: Icon }) => (
              <li key={path}>
                <Link
                  to={path}
                  className={`flex items-center gap-3 px-4 py-2 rounded-lg transition-colors ${
                    location.pathname === path
                      ? 'bg-blue-600 text-white'
                      : 'text-slate-300 hover:bg-slate-700 hover:text-white'
                  }`}
                >
                  <Icon className="w-5 h-5" />
                  {label}
                </Link>
              </li>
            ))}
          </ul>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="flex-1 p-8 overflow-auto">
        {children}
      </main>
    </div>
  );
}
