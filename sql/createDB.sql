#----------------------------------------
#----------------------------------------
#-- CREATION DATABASE DSTAirline
#----------------------------------------
#----------------------------------------


#----------------------------------------
#-- CREATION DATABASE
#----------------------------------------
CREATE DATABASE IF NOT EXISTS DSTAirline;

USE DSTAirline;

#----------------------------------------
#-- CREATION DES TABLES
#----------------------------------------
CREATE TABLE IF NOT EXISTS countries(
    country_iso2 VARCHAR(2) NOT NULL PRIMARY KEY,
	country_name VARCHAR(100) NOT NULL, 
	capital VARCHAR(100),
    currency_code VARCHAR(3), 
	fips_code VARCHAR(2),
    country_iso3 VARCHAR(3),
    continent VARCHAR(100), 
	country_id INT,
	currency_name VARCHAR(100),
    country_iso_numeric INT, 
	phone_prefix VARCHAR(100),
    population INT);
		
		
CREATE TABLE IF NOT EXISTS cities(
	iata_code VARCHAR(3) NOT NULL PRIMARY KEY,
	city_name VARCHAR(100) NOT NULL, 
	country_iso2 VARCHAR(2) NOT NULL, 
	gmt VARCHAR(10),
	city_id INT, 
	geoname_id INT,
	latitude FLOAT, 
	longitude FLOAT,
	timezone VARCHAR(100)
	);
	

CREATE TABLE IF NOT EXISTS airlines(
	iata_code VARCHAR(3) NOT NULL PRIMARY KEY,
	airline_name VARCHAR(100) NOT NULL, 
	country_iso2 VARCHAR(2) NOT NULL,
	fleet_average_age FLOAT,
    airline_id INT, 
	callsign VARCHAR(100),
    hub_code VARCHAR(10), 
	icao_code VARCHAR(4), 
    date_founded INT, 
	iata_prefix_accounting INT,
	country_name VARCHAR(100),
	fleet_size INT, 
	status VARCHAR(255), 
	airline_type VARCHAR(255)
	);


CREATE TABLE IF NOT EXISTS airplanes(
    airplane_id INT NOT NULL PRIMARY KEY, 
	airline_iata_code VARCHAR(3) NOT NULL, 
	iata_type VARCHAR(20), 
	iata_code_long VARCHAR(4),
	iata_code_short VARCHAR(3), 
	airline_icao_code VARCHAR(4),
	construction_number VARCHAR(50), 
	delivery_date VARCHAR(50),
	engines_count INT, 
	engines_type VARCHAR(50),
	first_flight_date VARCHAR(50),
	icao_code_hex VARCHAR(50),
	line_number VARCHAR(50), 
	model_code VARCHAR(50),					
	registration_number VARCHAR(50), 
	test_registration_number VARCHAR(100),
	plane_age INT, 
	plane_class VARCHAR(100), 
	model_name VARCHAR(100),
	plane_owner VARCHAR(100), 
	plane_series VARCHAR(100),
	plane_status VARCHAR(100), 
	production_line VARCHAR(100),
	registration_date VARCHAR(50), 
	rollout_date VARCHAR(50)
	);
										

CREATE TABLE IF NOT EXISTS airports(
	iata_code VARCHAR(3) NOT NULL PRIMARY KEY,
	airport_name VARCHAR(100) NOT NULL, 
	city_iata_code VARCHAR(3) NOT NULL, 
	country_iso2 VARCHAR(2) NOT NULL, 
	gmt VARCHAR(10),
	airport_id INT, 
	icao_code VARCHAR(4),
	geoname_id INT,
	latitude FLOAT, 
	longitude FLOAT,
	country_name VARCHAR(100),
	phone_number VARCHAR(100), 
	timezone VARCHAR(100)
	);
	
CREATE TABLE IF NOT EXISTS aircrafts(
	iata_code VARCHAR(3) NOT NULL PRIMARY KEY,
	aircraft_name VARCHAR(100) NOT NULL, 
	plane_type_id INT 
	);



