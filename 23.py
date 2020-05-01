from math import radians, sin, cos, acos
import json
import base64


def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    lat1 = radians(float(lat1))
    lat2 = radians(float(lat2))
    lon1 = radians(float(lon1))
    lon2 = radians(float(lon2))
    radius = 6371  # km
    dist = 6371.01 * acos(sin(lat1)*sin(lat2) + cos(lat1)
                          * cos(lat2)*cos(lon1 - lon2))

    # dlat = math.radians(lat2-lat1)
    # dlon = math.radians(lon2-lon1)
    # a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
    #     * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    # c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = dist

    return d


print(distance(eval("('39.32288', '-76.72803')"), eval("('39.32288', '-76.72803')")))
params = 'ewogICAgInF1ZXJ5X2lkIjogIjEwMDMiLAogICAgInF1ZXJ5X3RpbWUiOiAxNTgzODY4MDEyLAogICAgImNhcl90eXBlIjogInVuc3BlY2lmaWVkIiwKICAgICJsb2NhdGlvbiI6ICIoJzM0LjgxNjY3JywgJzEzNy40JykiLAogICAgInN0YXJ0X3RpbWUiOiAxNTg1MTM0OTAwLCAKICAgICJlbmRfdGltZSI6IDE1ODUxMzg1MDAKfQk='
decoded = base64.urlsafe_b64decode(
    params.encode('utf-8')).decode('utf-8')

print(json.loads(decoded))
