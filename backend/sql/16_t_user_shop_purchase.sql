DROP TABLE IF EXISTS spvadv.t_user_shop_purchase;
CREATE TABLE spvadv.t_user_shop_purchase (
  user_vehicle_id int NOT NULL,
  gigya_uid varchar(50) NOT NULL,
  shop_name varchar(255) NOT NULL,
  shop_tel varchar(15),
  shop_location text,
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
  PRIMARY KEY (user_vehicle_id),
  FOREIGN KEY (user_vehicle_id) REFERENCES spvadv.t_user_vehicle(user_vehicle_id)
);
