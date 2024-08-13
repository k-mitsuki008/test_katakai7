DROP TABLE IF EXISTS spvadv.t_ride_track;
CREATE TABLE spvadv.t_ride_track (
  ride_history_id varchar(50) NOT NULL,
  track_id bigint NOT NULL,
  user_vehicle_id int NOT NULL,
  latitude  double precision,
  longitude double precision,
  fcdyobi1 varchar(10),
  fcdyobi2 varchar(10),
  fcdyobi3 varchar(10),
  fcdyobi4 varchar(10),
  fcdyobi5 varchar(10),
  etxyobi1 varchar(50),
  etxyobi2 varchar(50),
  etxyobi3 varchar(50),
  etxyobi4 varchar(50),
  etxyobi5 varchar(50),
  delete_flag boolean DEFAULT false,
  delete_timestamp timestamp(3) without time zone,
  delete_user_id varchar(50),
  insert_timestamp timestamp(3) without time zone,
  insert_user_id varchar(50),
  update_timestamp timestamp(3) without time zone,
  update_user_id varchar(50),
  PRIMARY KEY (ride_history_id, track_id),
  FOREIGN KEY (ride_history_id) REFERENCES spvadv.t_ride_history(ride_history_id)
);
CREATE INDEX ON spvadv.t_ride_track(ride_history_id);