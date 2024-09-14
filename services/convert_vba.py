from pyproj import Proj, Transformer
import re


def parse_utm_input(utm_string):
    """Разбирает строку UTM в формате '43 V 381324 6751887'."""
    parts = utm_string.split()
    zone = parts[0]
    lat_band = parts[1]
    easting = int(parts[2])
    northing = int(parts[3])
    # Определяем, находится ли зона в северном полушарии
    northern_hemisphere = lat_band.upper() >= 'N'
    return zone, easting, northing, northern_hemisphere


def utm_to_latlon(utm_string):
    if re.search(r"[nNeE]\d+", utm_string):
        return utm_string
    zone, easting, northing, northern_hemisphere = parse_utm_input(utm_string)

    # Создаем объекты Proj
    if northern_hemisphere:
        proj_utm = Proj(f"+proj=utm +zone={zone} +ellps=WGS84 +datum=WGS84 +units=m +no_defs")
    else:
        proj_utm = Proj(
            f"+proj=utm +zone={zone} +ellps=WGS84 +datum=WGS84 +units=m +no_defs +south")

    proj_latlon = Proj(proj="latlong", datum="WGS84")

    # Создаем трансформер
    transformer = Transformer.from_proj(proj_utm, proj_latlon)

    # Производим трансформацию
    lon, lat = transformer.transform(easting, northing)

    return degrees_to_dms(lat, lon)


def degrees_to_dms(lat, lon):
    """Helper function to convert decimal degrees to degrees, minutes, seconds in the specific format."""

    def decimal_to_dms(deg):
        d = int(deg)
        m = int((abs(deg) * 3600) % 3600 // 60)
        s = (abs(deg) * 3600) % 60
        return d, m, s

    lat_d, lat_m, lat_s = decimal_to_dms(lat)
    lon_d, lon_m, lon_s = decimal_to_dms(lon)

    lat_direction = "N" if lat >= 0 else "S"
    lon_direction = "E" if lon >= 0 else "W"

    # Форматирование строк с добавлением ведущих нулей для минут и секунд
    lat_str = f"{lat_direction}{abs(lat_d)} {lat_m:02} {lat_s:05.1f}"
    lon_str = f"{lon_direction}{abs(lon_d)} {lon_m:02} {lon_s:05.1f}"

    return f"{lat_str} {lon_str}"


def convert_coordinates(coordinates: str) -> str:
    if '°' in coordinates:
        return coordinates

    degrees_symbol = '° '
    minutes_symbol = "´"
    seconds_symbol = "´´"

    split_coordinates = coordinates.split(' ')

    degrees = split_coordinates[0] + degrees_symbol
    minutes = split_coordinates[1] + minutes_symbol + split_coordinates[2] + seconds_symbol
    first_coordinate = degrees + minutes

    second_degrees = split_coordinates[3] + degrees_symbol
    second_minutes = split_coordinates[4] + minutes_symbol + split_coordinates[5] + seconds_symbol
    second_coordinate = second_degrees + second_minutes

    converted_coordinates = first_coordinate + ' ' + second_coordinate
    return converted_coordinates


if __name__ == '__main__':
    utm_string = "43 V 381324 6751887"
    # N60 53 03.7 E72 48 48.4
    # 60 53 3.7N 72 48 48.4E
    print(utm_to_latlon(utm_string))