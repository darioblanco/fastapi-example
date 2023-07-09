-- The database is created by the docker-compose.yml
-- entrypoint using the credentials specified in the env variables
SET search_path TO postgres;

CREATE ROLE sampleapi LOGIN PASSWORD 'secret';

CREATE DATABASE sampleapi OWNER sampleapi;

CREATE DATABASE test_sampleapi OWNER sampleapi;
