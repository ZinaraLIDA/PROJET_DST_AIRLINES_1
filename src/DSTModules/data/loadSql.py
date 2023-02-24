#========================================
# CREATION BASE SQL
# ALIMENTATION DES DONNEES
#========================================
from DSTModules.tools.tools import toListTuple

class loadSql:
    def __init__(self, db_mongo, db_sql, c_path):
        self.db_mongo = db_mongo
        self.db_sql = db_sql
        self.c_path = c_path

    def createTables(self):
        # Création de la base de données et des tables
        cursor_sql = self.db_sql.conn.cursor()

        with open(self.c_path["create_sql"]) as f:
            cursor_sql.execute(f.read())

        cursor_sql.close()

    def insertTable(self, query, list_values):
        tuple_values = toListTuple(list_values)

        cursor_sql = self.db_sql.conn.cursor()
        cursor_sql.executemany(query, tuple_values)
        self.db_sql.conn.commit()
        nb = cursor_sql.rowcount        
        cursor_sql.close()

        return nb

    def createForeignKey(self):
        # Création des clés étrangères
        cursor_sql = self.db_sql.conn.cursor()

        with open(self.c_path["create_fk"]) as f:
            cursor_sql.execute(f.read())

        cursor_sql.close()

    def insertCountries(self):
        list_countries = self.db_mongo["countries"].find({}, {
                "_id": 1,
	            "capital": 1,
                "continent": 1,
	            "country_id": 1,
                "country_iso3": 1,
                "country_iso_numeric": 1,
	            "country_name": 1,
                "currency_code": 1,
	            "currency_name": 1,
	            "fips_code": 1,
	            "phone_prefix": 1,
                "population": 1
            })

        query = "INSERT INTO countries ( \
            country_iso2, \
            capital, \
            continent, \
            country_id, \
            country_iso3, \
            country_iso_numeric, \
            country_name, \
            currency_code, \
            currency_name, \
            fips_code, \
            phone_prefix, \
            population) \
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

        nb = self.insertTable(query, list_countries)
        return "Nombre de lignes insérées: " + str(nb)

    def insertCities(self):
        list_cities = self.db_mongo["cities"].find({}, {
                "_id": 1,
                "city_id": 1,
                "city_name": 1,
                "country_iso2": 1,
                "geoname_id": 1,
                "gmt": 1,
                "latitude": 1,
                "longitude": 1,
                "timezone": 1
            })

        query = "INSERT INTO cities ( \
            iata_code, \
            city_id, \
            city_name, \
            country_iso2, \
            geoname_id, \
            gmt, \
            latitude, \
            longitude, \
            timezone) \
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s);"

        nb = self.insertTable(query, list_cities)

        return "Nombre de lignes insérées: " + str(nb)


    def insertAirlines(self):
        list_airlines = self.db_mongo["airlines"].find({}, {
            "_id": 1,
            "airline_id": 1,
            "airline_name": 1,
            "callsign": 1,
            "country_iso2": 1,
            "country_name": 1,
            "date_founded": 1,
            "fleet_average_age": 1,
            "fleet_size": 1,
            "hub_code": 1,
            "iata_prefix_accounting": 1,
            "icao_code": 1,
            "status": 1,
            "type": 1
            })

        query = "INSERT INTO airlines ( \
            iata_code, \
            airline_id, \
            airline_name, \
            callsign, \
            country_iso2, \
            country_name, \
            date_founded, \
            fleet_average_age, \
            fleet_size, \
            hub_code, \
            iata_prefix_accounting, \
            icao_code, \
            status, \
            airline_type) \
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

        nb = self.insertTable(query, list_airlines)

        return "Nombre de lignes insérées: " + str(nb)


    def insertAircraft(self):
        list_aircraft = self.db_mongo["aircraft_types"].find({}, {
            "_id": 1,
            "aircraft_name": 1,
            "plane_type_id": 1
            })

        query = "INSERT INTO aircrafts ( \
            iata_code, \
            aircraft_name, \
            plane_type_id) \
            values (%s, %s, %s);"

        nb = self.insertTable(query, list_aircraft)

        return "Nombre de lignes insérées: " + str(nb)


    def insertAirplanes(self):
        list_airplanes = self.db_mongo["airplanes"].find({}, {
            "_id": 1,
            "airline_iata_code": 1,
            "airline_icao_code": 1,
            "construction_number": 1,
            "delivery_date": 1,
            "engines_count": 1,
            "engines_type": 1,
            "first_flight_date": 1,
            "iata_code_long": 1,
            "iata_code_short": 1,
            "iata_type": 1,
            "icao_code_hex": 1,
            "line_number": 1,
            "model_code": 1,
            "model_name": 1,
            "plane_age": 1,
            "plane_class": 1,
            "plane_owner": 1,
            "plane_series": 1,
            "plane_status": 1,
            "production_line": 1,
            "registration_date": 1,
            "registration_number": 1,
            "rollout_date": 1,
            "test_registration_number": 1
            })

        query = "INSERT INTO airplanes ( \
            airplane_id, \
            airline_iata_code, \
            airline_icao_code, \
            construction_number, \
            delivery_date, \
            engines_count, \
            engines_type, \
            first_flight_date, \
            iata_code_long, \
            iata_code_short, \
            iata_type, \
            icao_code_hex, \
            line_number, \
            model_code, \
            model_name, \
            plane_age, \
            plane_class, \
            plane_owner, \
            plane_series, \
            plane_status, \
            production_line, \
            registration_date, \
            registration_number, \
            rollout_date, \
            test_registration_number) \
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

        nb = self.insertTable(query, list_airplanes)

        return "Nombre de lignes insérées: " + str(nb)


    def insertAirports(self):
        list_airports = self.db_mongo["airports"].find({}, {
            "_id": 1,
            "airport_id": 1,
            "airport_name": 1,
            "city_iata_code": 1,
            "country_iso2": 1,
            "country_name": 1,
            "geoname_id": 1,
            "gmt": 1,
            "icao_code": 1,
            "latitude": 1,
            "longitude": 1,
            "phone_number": 1,
            "timezone": 1
            })

        query = "INSERT INTO airports ( \
            iata_code, \
            airport_id, \
            airport_name, \
            city_iata_code, \
            country_iso2, \
            country_name, \
            geoname_id, \
            gmt, \
            icao_code, \
            latitude, \
            longitude, \
            phone_number, \
            timezone) \
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

        nb = self.insertTable(query, list_airports)

        return "Nombre de lignes insérées: " + str(nb)


