"""Shared geometry: atlas place frame (x east, z south, metres; Mercator scaled at anchor,
as tools/build_osm_context.py Frame) and Web-Mercator tile maths."""
import math

R = 6371008.8


def merc_x(lon): return (180 + lon) / 360


def merc_y(lat): return (180 - (180 / math.pi * math.log(math.tan(math.pi / 4 + lat * math.pi / 360)))) / 360


def lat_from_merc_y(y): return 360 / math.pi * math.atan(math.exp((180 - y * 360) * math.pi / 180)) - 90


def lon_from_merc_x(x): return x * 360 - 180


class Frame:
    def __init__(self, lat, lon):
        self.ox, self.oy = merc_x(lon), merc_y(lat)
        self.scale = 1 / (2 * math.pi * R) / math.cos(math.radians(lat_from_merc_y(self.oy)))

    def xz(self, lat, lon):
        return ((merc_x(lon) - self.ox) / self.scale, (merc_y(lat) - self.oy) / self.scale)

    def latlon(self, x, z):
        return (lat_from_merc_y(self.oy + z * self.scale), lon_from_merc_x(self.ox + x * self.scale))


def rot_cw(x, z, deg):
    """Turn (x east, z south) clockwise on the map by deg (east towards south)."""
    t = math.radians(deg)
    return (x * math.cos(t) - z * math.sin(t), x * math.sin(t) + z * math.cos(t))


def ground_m_per_mercunit(lat):
    return 2 * math.pi * R * math.cos(math.radians(lat))


def dist_m(lat1, lon1, lat2, lon2):
    f = Frame(lat1, lon1)
    x, z = f.xz(lat2, lon2)
    return math.hypot(x, z)
