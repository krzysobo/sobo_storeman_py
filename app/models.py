import datetime as dt
import services as srv


class ConnectionData:
    def __init__(self, bucket_service_obj, conn_id, name=None):
        self.conn_bucket_service = bucket_service_obj
        self.dt_created = dt.datetime.now(tz=dt.timezone.utc)
        self.name = name
        self.conn_id = conn_id
        self.name = f"unnamed {conn_id}" if name is None or name == "" else name

    def __str__(self):
        return f"[{self.conn_id}] ({self.name}) {self.dt_created.strftime('%Y-%m-%d %H:%M:%S')}"


class S3ConnectionManager:
    connections: list[ConnectionData] = []

    @classmethod
    def list_connections(cls):
        return cls.connections

    @classmethod
    def list_connection_names(cls):
        res = [c.name for c in cls.connections]
        return res

    @classmethod
    def _find_max_id(cls):
        id_max = 0
        if len(cls.connections) > 0:
            for conn in cls.connections:
                if conn.conn_id > id_max:
                    id_max = conn.conn_id
        return id_max

    @classmethod
    def add_connection_for_service(cls, bucket_service: srv.S3BucketService):
        id_max = cls._find_max_id()
        conn_id = id_max + 1
        new_conn = ConnectionData(bucket_service, conn_id=conn_id)
        cls.connections.append(new_conn)
        return new_conn.name