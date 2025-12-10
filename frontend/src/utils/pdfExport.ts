/**
 * PDF Export utility for generating reports
 */
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';
import { format } from 'date-fns';
import type { Airport, Aircraft, Pilot, Flight } from '../types';

const HEADER_COLOR: [number, number, number] = [30, 58, 138]; // Blue-900
const ALT_ROW_COLOR: [number, number, number] = [241, 245, 249]; // Slate-100

function addHeader(doc: jsPDF, title: string) {
  doc.setFontSize(20);
  doc.setTextColor(30, 58, 138);
  doc.text(title, 14, 20);
  
  doc.setFontSize(10);
  doc.setTextColor(100);
  doc.text(`Generated: ${format(new Date(), 'MMMM d, yyyy h:mm a')}`, 14, 28);
  doc.text('Airport Flight Tracker', doc.internal.pageSize.width - 14, 28, { align: 'right' });
  
  // Add a line under header
  doc.setDrawColor(200);
  doc.line(14, 32, doc.internal.pageSize.width - 14, 32);
}

function addFooter(doc: jsPDF) {
  const pageCount = doc.getNumberOfPages();
  for (let i = 1; i <= pageCount; i++) {
    doc.setPage(i);
    doc.setFontSize(8);
    doc.setTextColor(150);
    doc.text(
      `Page ${i} of ${pageCount}`,
      doc.internal.pageSize.width / 2,
      doc.internal.pageSize.height - 10,
      { align: 'center' }
    );
  }
}

export function exportAirportsPDF(airports: Airport[]) {
  const doc = new jsPDF();
  addHeader(doc, 'Airports Report');

  autoTable(doc, {
    startY: 40,
    head: [['ICAO', 'FAA', 'Name', 'City', 'State', 'Type', 'Tower']],
    body: airports.map(airport => [
      airport.icao_code,
      airport.faa_code || '-',
      airport.name,
      airport.city,
      airport.state,
      airport.airport_type,
      airport.has_tower ? 'Yes' : 'No'
    ]),
    headStyles: { fillColor: HEADER_COLOR },
    alternateRowStyles: { fillColor: ALT_ROW_COLOR },
    styles: { fontSize: 9 },
  });

  addFooter(doc);
  doc.save(`airports-report-${format(new Date(), 'yyyy-MM-dd')}.pdf`);
}

export function exportAircraftPDF(aircraft: Aircraft[]) {
  const doc = new jsPDF();
  addHeader(doc, 'Aircraft Report');

  autoTable(doc, {
    startY: 40,
    head: [['Tail Number', 'Manufacturer', 'Model', 'Year', 'Category', 'Owner']],
    body: aircraft.map(a => [
      a.tail_number,
      a.manufacturer,
      a.model,
      a.year_built?.toString() || '-',
      a.category,
      a.owner_name
    ]),
    headStyles: { fillColor: HEADER_COLOR },
    alternateRowStyles: { fillColor: ALT_ROW_COLOR },
    styles: { fontSize: 9 },
  });

  addFooter(doc);
  doc.save(`aircraft-report-${format(new Date(), 'yyyy-MM-dd')}.pdf`);
}

export function exportPilotsPDF(pilots: Pilot[]) {
  const doc = new jsPDF();
  addHeader(doc, 'Pilots Report');

  autoTable(doc, {
    startY: 40,
    head: [['Name', 'Certificate #', 'Certificate Type', 'Ratings', 'Medical Class', 'Total Hours']],
    body: pilots.map(pilot => [
      `${pilot.first_name} ${pilot.last_name}`,
      pilot.certificate_number,
      pilot.certificate_type,
      pilot.ratings || '-',
      pilot.medical_class || '-',
      pilot.total_flight_hours?.toString() || '0'
    ]),
    headStyles: { fillColor: HEADER_COLOR },
    alternateRowStyles: { fillColor: ALT_ROW_COLOR },
    styles: { fontSize: 9 },
  });

  addFooter(doc);
  doc.save(`pilots-report-${format(new Date(), 'yyyy-MM-dd')}.pdf`);
}

export function exportFlightsPDF(flights: Flight[]) {
  const doc = new jsPDF('landscape');
  addHeader(doc, 'Flights Report');

  autoTable(doc, {
    startY: 40,
    head: [['Date/Time', 'Airport', 'Operation', 'Aircraft', 'Pilot', 'Runway', 'Remarks']],
    body: flights.map(flight => [
      format(new Date(flight.actual_time), 'MM/dd/yyyy HH:mm'),
      flight.airport?.icao_code || '-',
      flight.operation,
      flight.aircraft?.tail_number || '-',
      flight.pilot ? `${flight.pilot.last_name}` : '-',
      flight.runway || '-',
      flight.remarks || '-'
    ]),
    headStyles: { fillColor: HEADER_COLOR },
    alternateRowStyles: { fillColor: ALT_ROW_COLOR },
    styles: { fontSize: 8 },
    columnStyles: {
      6: { cellWidth: 50 } // Remarks column wider
    }
  });

  addFooter(doc);
  doc.save(`flights-report-${format(new Date(), 'yyyy-MM-dd')}.pdf`);
}
