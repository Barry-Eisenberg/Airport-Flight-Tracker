"""
Seed script to populate the database with sample data including Jack Crane.
Run this script to add test pilots, aircraft, airports, and flights.
"""
import asyncio
from datetime import datetime, timedelta
import random
from sqlalchemy.ext.asyncio import AsyncSession

# Add parent directory to path
import sys
sys.path.insert(0, '.')

from app.core.database import async_session, engine
from app.models.models import Base, Airport, Aircraft, Pilot, Flight


async def seed_database():
    """Populate the database with sample data."""
    
    # Create all tables first
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with async_session() as db:
        # Check if data already exists
        from sqlalchemy import select, func
        result = await db.execute(select(func.count(Pilot.id)))
        if result.scalar() > 0:
            print("Database already has data. Skipping seed.")
            return
        
        print("Seeding database with sample data...")

        
        # ============ AIRPORTS ============
        airports = [
            Airport(
                icao_code="KFDK",
                faa_code="FDK",
                name="Frederick Municipal Airport",
                city="Frederick",
                state="MD",
                latitude=39.4176,
                longitude=-77.3742,
                elevation_ft=303,
                airport_type="public",
                ownership="public",
                has_tower=True,
                ctaf_frequency="122.725"
            ),
            Airport(
                icao_code="KGAI",
                faa_code="GAI",
                name="Montgomery County Airpark",
                city="Gaithersburg",
                state="MD",
                latitude=39.1683,
                longitude=-77.1660,
                elevation_ft=539,
                airport_type="public",
                ownership="public",
                has_tower=False,
                ctaf_frequency="123.075"
            ),
            Airport(
                icao_code="KCGS",
                faa_code="CGS",
                name="College Park Airport",
                city="College Park",
                state="MD",
                latitude=38.9806,
                longitude=-76.9225,
                elevation_ft=48,
                airport_type="public",
                ownership="public",
                has_tower=True,
                ctaf_frequency="120.2"
            ),
            Airport(
                icao_code="KFME",
                faa_code="FME",
                name="Tipton Airport",
                city="Fort Meade",
                state="MD",
                latitude=39.0854,
                longitude=-76.7594,
                elevation_ft=150,
                airport_type="military",
                ownership="military",
                has_tower=False,
                ctaf_frequency="123.0"
            ),
            Airport(
                icao_code="KADW",
                faa_code="ADW",
                name="Joint Base Andrews",
                city="Camp Springs",
                state="MD",
                latitude=38.8108,
                longitude=-76.8669,
                elevation_ft=280,
                airport_type="military",
                ownership="military",
                has_tower=True,
                ctaf_frequency="124.2"
            ),
            Airport(
                icao_code="KHGR",
                faa_code="HGR",
                name="Hagerstown Regional Airport",
                city="Hagerstown",
                state="MD",
                latitude=39.7079,
                longitude=-77.7295,
                elevation_ft=703,
                airport_type="public",
                ownership="public",
                has_tower=True,
                ctaf_frequency="119.05"
            ),
            Airport(
                icao_code="KESN",
                faa_code="ESN",
                name="Easton Airport",
                city="Easton",
                state="MD",
                latitude=38.8042,
                longitude=-76.0690,
                elevation_ft=72,
                airport_type="public",
                ownership="public",
                has_tower=False,
                ctaf_frequency="123.0"
            ),
            Airport(
                icao_code="KMTN",
                faa_code="MTN",
                name="Martin State Airport",
                city="Baltimore",
                state="MD",
                latitude=39.3257,
                longitude=-76.4138,
                elevation_ft=21,
                airport_type="public",
                ownership="public",
                has_tower=True,
                ctaf_frequency="126.25"
            ),
            # Major Regional Airports across the US
            Airport(
                icao_code="KPDK",
                faa_code="PDK",
                name="DeKalb-Peachtree Airport",
                city="Atlanta",
                state="GA",
                latitude=33.8756,
                longitude=-84.3020,
                elevation_ft=1003,
                airport_type="public",
                ownership="public",
                has_tower=True,
                ctaf_frequency="120.9"
            ),
            Airport(
                icao_code="KVNY",
                faa_code="VNY",
                name="Van Nuys Airport",
                city="Los Angeles",
                state="CA",
                latitude=34.2098,
                longitude=-118.4897,
                elevation_ft=802,
                airport_type="public",
                ownership="public",
                has_tower=True,
                ctaf_frequency="118.45"
            ),
            Airport(
                icao_code="KAPA",
                faa_code="APA",
                name="Centennial Airport",
                city="Denver",
                state="CO",
                latitude=39.5701,
                longitude=-104.8493,
                elevation_ft=5885,
                airport_type="public",
                ownership="public",
                has_tower=True,
                ctaf_frequency="118.9"
            ),
            Airport(
                icao_code="KFRG",
                faa_code="FRG",
                name="Republic Airport",
                city="Farmingdale",
                state="NY",
                latitude=40.7288,
                longitude=-73.4134,
                elevation_ft=82,
                airport_type="public",
                ownership="public",
                has_tower=True,
                ctaf_frequency="118.8"
            ),
            Airport(
                icao_code="KPWK",
                faa_code="PWK",
                name="Chicago Executive Airport",
                city="Wheeling",
                state="IL",
                latitude=42.1142,
                longitude=-87.9015,
                elevation_ft=647,
                airport_type="public",
                ownership="public",
                has_tower=True,
                ctaf_frequency="120.05"
            ),
            Airport(
                icao_code="KADS",
                faa_code="ADS",
                name="Addison Airport",
                city="Dallas",
                state="TX",
                latitude=32.9686,
                longitude=-96.8364,
                elevation_ft=644,
                airport_type="public",
                ownership="public",
                has_tower=True,
                ctaf_frequency="126.0"
            ),
            Airport(
                icao_code="KSDL",
                faa_code="SDL",
                name="Scottsdale Airport",
                city="Scottsdale",
                state="AZ",
                latitude=33.6229,
                longitude=-111.9105,
                elevation_ft=1510,
                airport_type="public",
                ownership="public",
                has_tower=True,
                ctaf_frequency="118.2"
            ),
            Airport(
                icao_code="KHEF",
                faa_code="HEF",
                name="Manassas Regional Airport",
                city="Manassas",
                state="VA",
                latitude=38.7214,
                longitude=-77.5153,
                elevation_ft=192,
                airport_type="public",
                ownership="public",
                has_tower=True,
                ctaf_frequency="124.0"
            ),
            Airport(
                icao_code="KLZU",
                faa_code="LZU",
                name="Gwinnett County Airport",
                city="Lawrenceville",
                state="GA",
                latitude=33.9781,
                longitude=-83.9624,
                elevation_ft=1061,
                airport_type="public",
                ownership="public",
                has_tower=True,
                ctaf_frequency="125.4"
            ),
            Airport(
                icao_code="KFXE",
                faa_code="FXE",
                name="Fort Lauderdale Executive",
                city="Fort Lauderdale",
                state="FL",
                latitude=26.1973,
                longitude=-80.1707,
                elevation_ft=13,
                airport_type="public",
                ownership="public",
                has_tower=True,
                ctaf_frequency="118.5"
            ),
            Airport(
                icao_code="KTMB",
                faa_code="TMB",
                name="Miami Executive Airport",
                city="Miami",
                state="FL",
                latitude=25.6479,
                longitude=-80.4328,
                elevation_ft=8,
                airport_type="public",
                ownership="public",
                has_tower=True,
                ctaf_frequency="119.0"
            ),
            Airport(
                icao_code="KBJC",
                faa_code="BJC",
                name="Rocky Mountain Metropolitan",
                city="Broomfield",
                state="CO",
                latitude=39.9089,
                longitude=-105.1172,
                elevation_ft=5673,
                airport_type="public",
                ownership="public",
                has_tower=True,
                ctaf_frequency="120.1"
            ),
            Airport(
                icao_code="KSMO",
                faa_code="SMO",
                name="Santa Monica Airport",
                city="Santa Monica",
                state="CA",
                latitude=34.0158,
                longitude=-118.4513,
                elevation_ft=177,
                airport_type="public",
                ownership="public",
                has_tower=True,
                ctaf_frequency="120.1"
            ),
            Airport(
                icao_code="KBED",
                faa_code="BED",
                name="Laurence G. Hanscom Field",
                city="Bedford",
                state="MA",
                latitude=42.4700,
                longitude=-71.2890,
                elevation_ft=133,
                airport_type="public",
                ownership="public",
                has_tower=True,
                ctaf_frequency="118.5"
            ),
            Airport(
                icao_code="KORL",
                faa_code="ORL",
                name="Orlando Executive Airport",
                city="Orlando",
                state="FL",
                latitude=28.5455,
                longitude=-81.3329,
                elevation_ft=113,
                airport_type="public",
                ownership="public",
                has_tower=True,
                ctaf_frequency="118.0"
            ),
            # Smaller regional airstrips
            Airport(
                icao_code="KCJR",
                faa_code="CJR",
                name="Culpeper Regional Airport",
                city="Culpeper",
                state="VA",
                latitude=38.5267,
                longitude=-77.8589,
                elevation_ft=316,
                airport_type="public",
                ownership="public",
                has_tower=False,
                ctaf_frequency="122.8"
            ),
            Airport(
                icao_code="KW29",
                faa_code="W29",
                name="Bay Bridge Airport",
                city="Stevensville",
                state="MD",
                latitude=38.9742,
                longitude=-76.3306,
                elevation_ft=63,
                airport_type="public",
                ownership="public",
                has_tower=False,
                ctaf_frequency="122.8"
            ),
            Airport(
                icao_code="KHWY",
                faa_code="HWY",
                name="Warrenton-Fauquier Airport",
                city="Warrenton",
                state="VA",
                latitude=38.5875,
                longitude=-77.7150,
                elevation_ft=336,
                airport_type="public",
                ownership="private",
                has_tower=False,
                ctaf_frequency="122.8"
            ),
            Airport(
                icao_code="KJYO",
                faa_code="JYO",
                name="Leesburg Executive Airport",
                city="Leesburg",
                state="VA",
                latitude=39.0778,
                longitude=-77.5575,
                elevation_ft=389,
                airport_type="public",
                ownership="public",
                has_tower=True,
                ctaf_frequency="123.075"
            ),
        ]
        
        for airport in airports:
            db.add(airport)
        await db.flush()
        print(f"  Added {len(airports)} airports")
        
        # ============ AIRCRAFT ============
        aircraft_list = [
            Aircraft(
                tail_number="N12345",
                manufacturer="Cessna",
                model="172 Skyhawk",
                year_built=1998,
                category="single_engine",
                engine_type="Lycoming O-360",
                num_engines=1,
                max_passengers=3,
                owner_name="Jack Crane",
                owner_city="Frederick",
                owner_state="MD",
                is_active=True
            ),
            Aircraft(
                tail_number="N67890",
                manufacturer="Piper",
                model="PA-28 Cherokee",
                year_built=2005,
                category="single_engine",
                engine_type="Lycoming O-360",
                num_engines=1,
                max_passengers=3,
                owner_name="Blue Sky Aviation",
                owner_city="Gaithersburg",
                owner_state="MD",
                is_active=True
            ),
            Aircraft(
                tail_number="N24680",
                manufacturer="Lockheed",
                model="C-130 Hercules",
                year_built=1985,
                category="multi_engine",
                engine_type="Allison T56-A-15",
                num_engines=4,
                max_passengers=92,
                owner_name="Maryland Air National Guard",
                owner_city="Baltimore",
                owner_state="MD",
                is_active=True
            ),
            Aircraft(
                tail_number="N13579",
                manufacturer="Beechcraft",
                model="King Air 350",
                year_built=2010,
                category="multi_engine",
                engine_type="Pratt & Whitney PT6A-60A",
                num_engines=2,
                max_passengers=8,
                owner_name="Executive Air Services",
                owner_city="Hagerstown",
                owner_state="MD",
                is_active=True
            ),
            Aircraft(
                tail_number="N98765",
                manufacturer="Douglas",
                model="DC-3",
                year_built=1944,
                category="multi_engine",
                engine_type="Pratt & Whitney R-1830",
                num_engines=2,
                max_passengers=28,
                owner_name="Vintage Wings Foundation",
                owner_city="Frederick",
                owner_state="MD",
                is_active=True
            ),
            Aircraft(
                tail_number="N55555",
                manufacturer="Cessna",
                model="182 Skylane",
                year_built=2015,
                category="single_engine",
                engine_type="Lycoming O-540",
                num_engines=1,
                max_passengers=3,
                owner_name="Jack Crane",
                owner_city="Frederick",
                owner_state="MD",
                is_active=True
            ),
        ]
        
        for aircraft in aircraft_list:
            db.add(aircraft)
        await db.flush()
        print(f"  Added {len(aircraft_list)} aircraft")
        
        # ============ PILOTS ============
        pilots = [
            Pilot(
                certificate_number="3847291",
                first_name="Jack",
                last_name="Crane",
                certificate_type="private",
                ratings="SEL, MEL, Instrument",
                medical_class="Class 3",
                medical_expiry=datetime(2026, 6, 15),
                total_flight_hours=2847.5,
                email="jack.crane@email.com",
                phone="301-555-0142",
                city="Frederick",
                state="MD",
                is_active=True
            ),
            Pilot(
                certificate_number="5928374",
                first_name="Sarah",
                last_name="Mitchell",
                certificate_type="commercial",
                ratings="SEL, MEL, Instrument, CFI, CFII",
                medical_class="Class 2",
                medical_expiry=datetime(2026, 3, 20),
                total_flight_hours=4521.0,
                email="sarah.mitchell@email.com",
                phone="301-555-0198",
                city="Gaithersburg",
                state="MD",
                is_active=True
            ),
            Pilot(
                certificate_number="1029384",
                first_name="Michael",
                last_name="Torres",
                certificate_type="atp",
                ratings="SEL, MEL, SES, Instrument, CFI, CFII, MEI",
                medical_class="Class 1",
                medical_expiry=datetime(2026, 1, 10),
                total_flight_hours=12500.0,
                email="m.torres@email.com",
                phone="410-555-0234",
                city="Baltimore",
                state="MD",
                is_active=True
            ),
            Pilot(
                certificate_number="7463829",
                first_name="Emily",
                last_name="Chen",
                certificate_type="student",
                ratings="None",
                medical_class="Class 3",
                medical_expiry=datetime(2027, 9, 5),
                total_flight_hours=45.0,
                email="emily.chen@email.com",
                phone="240-555-0167",
                city="College Park",
                state="MD",
                is_active=True
            ),
            Pilot(
                certificate_number="8574920",
                first_name="Robert",
                last_name="Anderson",
                certificate_type="private",
                ratings="SEL, Instrument",
                medical_class="Class 3",
                medical_expiry=datetime(2025, 12, 31),
                total_flight_hours=890.0,
                email="r.anderson@email.com",
                phone="301-555-0289",
                city="Hagerstown",
                state="MD",
                is_active=True
            ),
        ]
        
        for pilot in pilots:
            db.add(pilot)
        await db.flush()
        print(f"  Added {len(pilots)} pilots")
        
        # Get the created records
        airport_result = await db.execute(select(Airport))
        db_airports = {a.faa_code: a for a in airport_result.scalars().all()}
        
        aircraft_result = await db.execute(select(Aircraft))
        db_aircraft = {a.tail_number: a for a in aircraft_result.scalars().all()}
        
        pilot_result = await db.execute(select(Pilot))
        db_pilots = {f"{p.first_name} {p.last_name}": p for p in pilot_result.scalars().all()}
        
        # ============ FLIGHTS ============
        # Generate flight history for Jack Crane spanning 15 years
        jack = db_pilots["Jack Crane"]
        jack_aircraft = [db_aircraft["N12345"], db_aircraft["N55555"], db_aircraft["N24680"], db_aircraft["N98765"]]
        
        flights = []
        flight_types = ["local", "cross_country", "training", "other"]
        operations = ["takeoff", "landing", "touch_and_go"]
        
        # Generate flights for Jack Crane over 15 years
        for years_ago in range(15, 0, -1):
            # More flights in recent years
            num_flights = random.randint(8, 25) if years_ago <= 5 else random.randint(3, 12)
            
            for _ in range(num_flights):
                flight_date = datetime.now() - timedelta(days=years_ago * 365 + random.randint(0, 364))
                airport = random.choice(list(db_airports.values()))
                aircraft = random.choice(jack_aircraft)
                
                # Determine origin/destination based on flight type
                flight_type = random.choice(flight_types)
                if flight_type == "cross_country":
                    other_airports = [a for a in db_airports.values() if a.id != airport.id]
                    dest_airport = random.choice(other_airports) if other_airports else airport
                    origin = airport.faa_code
                    destination = dest_airport.faa_code
                else:
                    origin = airport.faa_code
                    destination = airport.faa_code
                
                flight = Flight(
                    airport_id=airport.id,
                    aircraft_id=aircraft.id,
                    pic_id=jack.id,
                    flight_type=flight_type,
                    operation=random.choice(operations),
                    runway=f"{random.randint(1, 36):02d}",
                    actual_time=flight_date,
                    origin_airport=origin,
                    destination_airport=destination,
                    passengers=random.randint(0, min(3, aircraft.max_passengers or 3)),
                    fuel_gallons=random.uniform(10, 80),
                    remarks=None
                )
                flights.append(flight)
        
        # Add flights for other pilots too
        for pilot_name, pilot in db_pilots.items():
            if pilot_name == "Jack Crane":
                continue
            
            num_flights = random.randint(10, 50)
            for _ in range(num_flights):
                flight_date = datetime.now() - timedelta(days=random.randint(1, 365 * 5))
                airport = random.choice(list(db_airports.values()))
                aircraft = random.choice(list(db_aircraft.values()))
                
                flight_type = random.choice(flight_types)
                if flight_type == "cross_country":
                    other_airports = [a for a in db_airports.values() if a.id != airport.id]
                    dest_airport = random.choice(other_airports) if other_airports else airport
                    origin = airport.faa_code
                    destination = dest_airport.faa_code
                else:
                    origin = airport.faa_code
                    destination = airport.faa_code
                
                flight = Flight(
                    airport_id=airport.id,
                    aircraft_id=aircraft.id,
                    pic_id=pilot.id,
                    flight_type=flight_type,
                    operation=random.choice(operations),
                    runway=f"{random.randint(1, 36):02d}",
                    actual_time=flight_date,
                    origin_airport=origin,
                    destination_airport=destination,
                    passengers=random.randint(0, min(3, aircraft.max_passengers or 3)),
                    fuel_gallons=random.uniform(10, 80),
                    remarks=None
                )
                flights.append(flight)
        
        for flight in flights:
            db.add(flight)
        
        await db.commit()
        print(f"  Added {len(flights)} flights")
        
        # Summary
        jack_flights = [f for f in flights if f.pic_id == jack.id]
        print(f"\nDatabase seeded successfully!")
        print(f"  Jack Crane has {len(jack_flights)} flights spanning 15 years")
        print(f"  Aircraft flown: Cessna 172, Cessna 182, C-130 Hercules, DC-3")


if __name__ == "__main__":
    asyncio.run(seed_database())
