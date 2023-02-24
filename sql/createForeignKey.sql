#----------------------------------------
#-- CREATION FOREIGN KEY
#----------------------------------------

#-- FK cities

ALTER TABLE cities
ADD CONSTRAINT FK_cities_countries
FOREIGN KEY (country_iso2) REFERENCES countries(country_iso2);

#-- FK airlines

DELETE FROM airlines WHERE country_iso2 not in (select country_iso2 from countries);

ALTER TABLE airlines
ADD CONSTRAINT FK_airlines_countries
FOREIGN KEY (country_iso2) REFERENCES countries(country_iso2);

#-- FK airplanes

DELETE FROM airplanes WHERE airline_iata_code not in (select iata_code from airlines);

ALTER TABLE airplanes
ADD CONSTRAINT FK_airplanes_airlines
FOREIGN KEY (airline_iata_code) REFERENCES airlines(iata_code);

#-- FK airports

DELETE FROM airports WHERE city_iata_code not in (select iata_code from cities);

ALTER TABLE airports
ADD CONSTRAINT FK_airports_cities
FOREIGN KEY (city_iata_code) REFERENCES cities(iata_code);

ALTER TABLE airports
ADD CONSTRAINT FK_airports_countries
FOREIGN KEY (country_iso2) REFERENCES countries(country_iso2);



#--ALTER TABLE cities
#--DROP FOREIGN KEY FK_cities_countries;

#--ALTER TABLE airlines
#--DROP FOREIGN KEY FK_airlines_countries;

#--ALTER TABLE airplanes
#--DROP FOREIGN KEY FK_airplanes_airlines;

#--ALTER TABLE airports
#--DROP FOREIGN KEY FK_airports_cities;

#--ALTER TABLE airports
#--DROP FOREIGN KEY FK_airports_countries;
