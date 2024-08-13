def create_update_set_sql(**kwargs):
    """
    updateのset文を組み立て
    """
    place_holder_values_list = []
    for k in kwargs:
        place_holder = f'{k} = %({k})s'
        place_holder_values_list.append(place_holder)
    return "\n, ".join(place_holder_values_list) + f"\n ,update_timestamp = %(now_str)s \n ,update_user_id = %(gigya_uid)s"
