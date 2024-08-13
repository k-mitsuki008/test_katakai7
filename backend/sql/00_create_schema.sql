CREATE SCHEMA IF NOT EXISTS spvadv;
ALTER USER "admin" SET search_path TO "$user", public, topology, tiger, spvadv;
