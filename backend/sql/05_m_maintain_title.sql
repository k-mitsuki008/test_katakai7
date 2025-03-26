DROP TABLE IF EXISTS spvadv.m_maintain_title CASCADE;
CREATE TABLE spvadv.m_maintain_title (
  model_code char(4) NOT NULL,
  maintain_item_code char(5) NOT NULL,
  maintain_title_code char(3) NOT NULL,
  explanation_title varchar(50) NOT NULL,
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
  PRIMARY KEY (model_code, maintain_item_code, maintain_title_code),
  FOREIGN KEY (model_code, maintain_item_code) REFERENCES spvadv.m_maintain_item(model_code, maintain_item_code)
);
CREATE INDEX ON spvadv.m_maintain_title(maintain_item_code);