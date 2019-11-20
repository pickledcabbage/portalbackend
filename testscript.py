from src.db.dba import DBAccessor

dba = DBAccessor()
print(dba.get_table_names())

print(dba.get_config_token())