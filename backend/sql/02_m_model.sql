DROP TABLE IF EXISTS spvadv.m_model CASCADE;
CREATE TABLE spvadv.m_model (
  model_code char(4) NOT NULL,
  model_name varchar(50),
  sort_order int NOT NULL,
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
  PRIMARY KEY (model_code)
);