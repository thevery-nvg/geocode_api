import re
import random
from functools import reduce
from typing import List, Tuple

patterns = {
    "pa": (r"N(0?\d{2})(\d{2})(\d{2}\.\d{1,3})", r"E(0?\d{2})(\d{2})(\d{2}\.\d{1,3})"),
    "pb": (r"N(0?\d{2})(\d{1,2}\.\d{1,3})", r"E(0?\d{2})(\d{1,2}\.\d{1,3})"),
    "pc": (r"N?(\d{2}\.\d+)", r"E?(\d{2}\.\d+)")
}


def clear_data(data: str) -> str:
    return re.sub(r"[^NE0-9.]", "", data.replace(",", "."))


def convert_coordinates_full(p: str, data: str) -> Tuple[float, float]:
    lat, lon = 0, 0
    x = re.fullmatch(p, clear_data(data)).groups()
    if len(x) == 2:
        lat, lon = float(x[0]), float(x[1])
    elif len(x) == 4:
        lat, lon = float(x[0]) + float(x[1]) / 60, float(x[2]) + float(x[3]) / 60
    elif len(x) == 6:
        lat, lon = float(x[0]) + float(x[1]) / 60 + float(x[2]) / 3600, float(x[3]) + float(
            x[4]) / 60 + float(
            x[5]) / 3600
    return round(lat, 5), round(lon, 5)


def raw_decode(data,screen=False):
    try:
        line = clear_data(data[0])
    except:
        return []
    out = []
    out_screen = []
    for pattern, (p1, p2) in patterns.items():
        d = clear_data(reduce(lambda x, y: x + y, data))
        if re.fullmatch(f"{p1}{p2}", line) or re.search(p1, d):
            lats = re.findall(p1, d)
            lons = re.findall(p2, d)
            for lat, lon in zip(lats, lons):
                coord = "N" + "".join(lat) + "E" + "".join(lon)
                out.append(convert_coordinates_full(f"{p1}{p2}", coord))
                x = convert_coordinates_full(f"{p1}{p2}", coord)
                out_screen.append(decimal_degrees_to_latlon(x[0],x[1]))
            if screen:
                return out_screen
            else:
                return out
    return []


def google_decode(data,screen=False):
    a = re.findall("\d{2}\.\d+", data)
    left = []
    right = []
    res_screen = []
    for i, val in enumerate(a):
        if i % 2:
            left.append(val)
        else:
            right.append(val)
    res = []
    for i in zip(left, right):
        res.append(i)
        res_screen.append(decimal_degrees_to_latlon(i[0], i[1]))
    if screen:
        return res_screen
    else:
        return res


def geo_decode_gpx(data):
    head = '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
    <gpx xmlns="http://www.topografix.com/GPX/1/1" creator="MapSource 6.16.3" version="1.1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">

      <metadata>
        <link href="http://www.garmin.com">
          <text>Garmin International</text>
        </link>
        <time>2024-01-23T12:24:21Z</time>
        <bounds maxlat="56.092479145154357" maxlon="55.898553002625704" minlat="53.633718425408006" minlon="51.073859967291355"/>
      </metadata>'''
    tail = '\n</gpx>'
    output = ""
    output += head
    height = random.randint(40, 60)
    for i, (lat, lon) in enumerate(data, start=1):
        temp = f'''  <wpt lat="{lat}" lon="{lon}">
                <ele>{height + random.randint(1, 5)}</ele>
                <time>2024-01-16T12:56:09Z</time>
                <name>{i:03}</name>
                <cmt>30-APR-04 0:57:35</cmt>
                <desc>30-APR-04 0:57:35</desc>
                <sym>Flag, Green</sym>
                <extensions>
                <gpxx:WaypointExtension xmlns:gpxx="http://www.garmin.com/xmlschemas/GpxExtensions/v3">
                <gpxx:DisplayMode>SymbolAndName</gpxx:DisplayMode>
                </gpxx:WaypointExtension>
                </extensions>
                </wpt>\n'''
        output += temp
    output += tail
    return output


from pyproj import Proj

wgs84 = Proj('epsg:4326')


def decimal_degrees_to_latlon(x, y):
    degrees_symbol = '° '
    minutes_symbol = "´"
    seconds_symbol = "´´"
    lat, lon = wgs84(x, y, inverse=True)
    lat_deg, lat_min, lat_sec = lat_to_dms(lat)
    lon_deg, lon_min, lon_sec = lon_to_dms(lon)
    # return (lat_deg, lat_min, lat_sec), (lon_deg, lon_min, lon_sec)
    return (f"N{lat_deg}{degrees_symbol}{lat_min}{minutes_symbol}{lat_sec}{seconds_symbol}"
            f" E{lon_deg}{degrees_symbol}{lon_min}{minutes_symbol}{lon_sec}{seconds_symbol}")


def lat_to_dms(lat):
    deg = int(lat)
    min = int((lat - deg) * 60)
    sec = int((lat - deg - min / 60) * 3600)
    return deg, min, sec


def lon_to_dms(lon):
    deg = int(lon)
    min = int((lon - deg) * 60)
    sec = int((lon - deg - min / 60) * 3600)
    return deg, min, sec


if __name__ == '__main__':
    degrees_symbol = '° '
    minutes_symbol = "´"
    seconds_symbol = "´´"
    s = [
        (60.96203, 70.87643),
        (60.96190, 70.87728),
        (60.96170, 70.87860),
        (60.96150, 70.87993),
        (60.96130, 70.88122),
        (60.96110, 70.88250),
        (60.96088, 70.88387),
        (60.96070, 70.88510),
        (60.96043, 70.88678),
        (60.96037, 70.88725),
        (60.96027, 70.88783),
    ]
    for n, i in enumerate(s):
        print(n + 1)
        print(decimal_degrees_to_latlon(i[0], i[1]))
