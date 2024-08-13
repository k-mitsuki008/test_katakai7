INSERT INTO m_spot
  (spot_type_code,spot_location,spot_place_id,rechargeable_flag,fcdyobi1,fcdyobi2,fcdyobi3,fcdyobi4,fcdyobi5,etxyobi1,etxyobi2,etxyobi3,etxyobi4,etxyobi5,
  delete_flag,delete_timestamp,delete_user_id,insert_timestamp,insert_user_id,update_timestamp,update_user_id)
VALUES
  ('10010',ST_GeomFromText('POINT(34.722973 137.876741)', 4326),'ChIJIWeYpqvlGmAR2eP_OkBAGKY',true,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,false,NULL,NULL,CURRENT_TIMESTAMP,'spvadv_admin',NULL,NULL),
  ('10010',ST_GeomFromText('POINT(35.638695 139.62601)', 4326),'ChIJSSRnCvLzGGARsb6MGz3zTho',true,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,false,NULL,NULL,CURRENT_TIMESTAMP,'spvadv_admin',NULL,NULL),
  ('10010',ST_GeomFromText('POINT(52.28267 4.759327)', 4326),'ChIJMTuLSLfgxUcRjfLJ2v8pm_0',true,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,false,NULL,NULL,CURRENT_TIMESTAMP,'spvadv_admin',NULL,NULL),
  ('10010',ST_GeomFromText('POINT(33.803711 -118.018102)', 4326),'ChIJ49gOMS0p3YAR6yvv1AaNzI4',true,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,false,NULL,NULL,CURRENT_TIMESTAMP,'spvadv_admin',NULL,NULL);
