setting up the db with docker - triend and failed.. for now i am sticking with the normal DB style.. no docker pure DB 


giving the grants to my existing user
CREATE DATABASE eagle_horizon_legacy_database;
GRANT ALL PRIVILEGES ON DATABASE eagle_horizon_legacy_database TO chama;

GRANT ALL PRIVILEGES ON SCHEMA public TO chama;

ALTER DATABASE eagle_horizon_legacy_database OWNER TO chama;

GRANT ALL PRIVILEGES ON DATABASE eagle_horizon_legacy_database TO chama;