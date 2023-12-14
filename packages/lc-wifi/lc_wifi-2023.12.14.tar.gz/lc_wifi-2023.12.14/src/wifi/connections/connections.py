from operators.con import con, add_connection, redis, http, kafka, elastic, clickhouse
from wifi.connections import elastic as es
from wifi.connections import clickhouse as ch


# define available connection ops (e.g. "con.redis")
allcons = redis.redis, http.http, kafka.kafka, elastic.elastic, clickhouse.clickhouse
[add_connection(cls, cls.__name__) for cls in allcons]
add_connection(http.http, 'http_bulk_data', req_conf=True)
con.elastic.con_attributes = es.Attrs
con.clickhouse.con_attributes = ch.Attrs
