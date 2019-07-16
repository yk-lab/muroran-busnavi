import json
from models import Stop, StopName, StopPosition, StopUrl
from sqlalchemy.ext.declarative import DeclarativeMeta


class StopJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(o)
                          if not x.startswith('_') and x != 'metadata']:
                data = o.__getattribute__(field)
                try:
                    # will fail on non-encodable values, like other classes
                    json.dumps(data)
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields
        if isinstance(o, Stop):
            if o.name:
                self.default(o.name)
            return {"id": o.id}
        if isinstance(o, StopName):
            return {"name": o.name}
        if isinstance(o, StopPosition):
            return {"quadkey": o.quadkey}
        if isinstance(o, StopUrl):
            return {"stop": o.stop_code}
        return super(StopJSONEncoder, self).default(o)
