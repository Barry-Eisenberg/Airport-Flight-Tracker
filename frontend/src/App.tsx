import { Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Airports from './pages/Airports';
import Aircraft from './pages/Aircraft';
import Pilots from './pages/Pilots';
import Flights from './pages/Flights';

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/airports" element={<Airports />} />
        <Route path="/aircraft" element={<Aircraft />} />
        <Route path="/pilots" element={<Pilots />} />
        <Route path="/flights" element={<Flights />} />
      </Routes>
    </Layout>
  );
}

export default App;
