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


def raw_decode(data):
    try:
        line = clear_data(data[0])
    except:
        return []
    out = []
    for pattern, (p1, p2) in patterns.items():
        d = clear_data(reduce(lambda x, y: x + y, data))
        if re.fullmatch(f"{p1}{p2}", line) or re.search(p1, d):
            lats = re.findall(p1, d)
            lons = re.findall(p2, d)
            for lat, lon in zip(lats, lons):
                coord = "N" + "".join(lat) + "E" + "".join(lon)
                out.append(convert_coordinates_full(f"{p1}{p2}", coord))
            return out
    return []


def google_decode(data):
    a = re.findall("\d{2}\.\d+", data)
    left = []
    right = []
    for i, val in enumerate(a):
        if i % 2:
            left.append(val)
        else:
            right.append(val)
    res = []
    for i in zip(left, right):
        res.append(i)
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
