import re
import math
import random


def get_otbr_thickness(d):
    return {d <= 25: 1, d <= 57: 1.5, d <= 114: 2, d <= 219: 2.5, d <= 325: 3, d <= 377: 3.5, d > 377: 4}[True]


def get_r(d):
    mapping = {
        57: 50 * 1.5,
        89: 80 * 1.5,
        108: 100 * 1.5,
        114: 100 * 1.5,
        159: 150 * 1.5,
        168: 150 * 1.5,
        219: 200 * 1.5,
        273: 250 * 1.5,
        325: 300 * 1.5,
        377: 350 * 1.5,
        426: 400 * 1.5
    }
    return mapping.get(d, None)


def get_allowed_tension_pipe(steel, t):
    t20 = {"ВСт3": 154,
           "сталь 10": 130,
           "сталь 20": 147,
           "09Г2С": 196,
           "16ГС": 196,
           "10Г2": 180,
           "17ГС": 183,
           "08Х18Н10Т": 168,
           "13ХФА": 207, }
    t100 = {"ВСт3": 149,
            "сталь 10": 125,
            "сталь 20": 142,
            "09Г2С": 177,
            "16ГС": 177,
            "10Г2": 160,
            "17ГС": 160,
            "08Х18Н10Т": 156,
            "13ХФА": 187}
    t150 = {"ВСт3": 145,
            "сталь 10": 122,
            "сталь 20": 139,
            "09Г2С": 171,
            "16ГС": 171,
            "10Г2": 154,
            "17ГС": 157,
            "08Х18Н10Т": 148,
            "13ХФА": 0, }
    if t < 101:
        return t100.get(steel) + (100 - t) * ((t20.get(steel) - t100.get(steel)) / 80)
    elif t < 151:
        return t150.get(steel) + (150 - t) * ((t100.get(steel) - t150.get(steel)) / 50)
    else:
        return 1


def get_passing_length(d):
    d = get_max_diameter(d)
    return {
        48: 64,
        57: 76,
        76: 89,
        89: 89,
        108: 102,
        114: 102,
        132: 127,
        159: 140,
        168: 140,
        219: 152,
        273: 178,
        325: 203,
        377: 330,
        426: 356,
        530: 508,
        630: 508,
        750: 508,
        720: 508
    }[d]


def get_sr_pipe(sigma, d, p):
    return ((p * d) / (2 * sigma + p))


def get_sr_bend(sigma, d, p):
    r = get_r(d)
    sr = get_sr_pipe(sigma, d, p)
    x = round(((4 * (r / (d + sr))) - 1) / ((4 * (r / (d + sr))) - 2), 1)
    k = max(x, 1)
    return sr * k


def get_sr_passing(sigma, d, p):
    d1, d2 = split_diameter(d)
    d = max(d1, d2)
    passing_length = get_passing_length(d)
    alpha = math.atan(abs(d1 - d2) / (2 * passing_length))
    return (p * d) / (2 * sigma * math.cos(alpha) + p)


def split_diameter(d):
    if "/" in d:
        d = re.sub(r"/", "f", d)
        d1, d2 = list(map(int, d.split("f")))
        return d1, d2
    else:
        return d, d


def get_sr_tripler(sigma, d, p):
    d = get_max_diameter(d)
    return get_sr_pipe(sigma, d, p)


def get_sr_ellypse_stub(sigma, d, p):
    h = d / 4
    return (((p * d) / (4 * sigma + p))) * (d / (2 * h))


def get_sr_flat_stub(sigma, d, smin, p):
    return ((0.53 * (d - smin)) / 1) * (p / (sigma * 0.8)) ** 0.5


def get_sr_valve(sigma, d, p):
    return (p * d) / ((2 * sigma) - p)


def get_sr_flanc_stub(sigma, d, p):
    return 0.5 * d * (p / sigma) ** 0.5


def get_max_diameter(d):
    if isinstance(d, int):
        return d
    elif "/" in d:
        d = re.sub(r"/", "f", d)
        d = max(map(int, d.split("f")))
    return int(d)


def parse_pipeline(data: dict):
    pipeline = {}
    other = {}
    for k in data.keys():
        if k in ("p", "t"):
            other[k] = data[k]
        else:
            s = data[k].split('f')
            pipeline[k] = [s[0].strip(), s[1], float(s[2]), float(s[3]), s[4], int(s[5])]
    result = create_measures(pipeline, other)

    return result
    # return pipeline, other


def create_measures(pipeline, other):
    t = other["t"]
    p = other['p']
    result = {}
    for k, v in pipeline.items():
        name = v[0]
        snom = v[2]
        smin = v[3]
        if abs(snom - smin) < 0.5:
            delta = 0.2
        else:
            delta = 0.5
        steel = v[4]
        sigma = get_allowed_tension_pipe(steel, t)
        if name == "труба":
            d = get_max_diameter(v[1])
            sr = round(get_sr_pipe(sigma, d, p) + 1, 1)
            sr_gost = get_otbr_thickness(d)
            rnd = [str(round(random.uniform(smin + delta, smin), 1)) for _ in range(4)] + ["-"] * 6
            pos = random.randint(0, 3)
            rnd[pos]=str(smin)
            # result[k] = "f".join([str(name), str(d), str(snom), str(smin), str(max(sr, sr_gost)), *rnd])
        elif name == "отвод":
            d = get_max_diameter(v[1])
            sr = round(get_sr_bend(sigma, d, p) + 1, 1)
            sr_gost = get_otbr_thickness(d)
            rnd = [str(round(random.uniform(smin + delta, smin), 1)) for _ in range(6)] + ["-"] * 4
            pos = random.randint(0, 5)
            rnd[pos]=str(smin)
            # result[k] = "f".join([str(name), str(d), str(snom), str(smin), str(max(sr, sr_gost)), *rnd])
        elif name == "переход":
            d = v[1]
            sr = round(get_sr_passing(sigma, d, p) + 1, 1)
            d = get_max_diameter(d)
            sr_gost = get_otbr_thickness(d)
            rnd = [str(round(random.uniform(smin + delta, smin), 1)) for _ in range(8)] + ["-"]*2
            pos = random.randint(0, 7)
            rnd[pos]=str(smin)
            # result[k] = "f".join([str(name), str(d), str(snom), str(smin), str(max(sr, sr_gost)), *rnd])
        elif name == "тройник":
            d = get_max_diameter(v[1])
            sr = round(get_sr_tripler(sigma, d, p) + 1, 1)
            sr_gost = get_otbr_thickness(d)
            rnd = [str(round(random.uniform(smin + delta, smin), 1)) for _ in range(9)]
            pos = random.randint(0, 8)
            rnd[pos]=str(smin)
            # result[k] = "f".join([str(name), str(d), str(snom), str(smin), str(max(sr, sr_gost)), *rnd])
        elif re.search(r"элл",name):
            d = get_max_diameter(v[1])
            sr = round(get_sr_ellypse_stub(sigma, d, p) + 1, 1)
            sr_gost = get_otbr_thickness(d)
            rnd = [str(round(random.uniform(smin + delta, smin), 1)) for _ in range(5)] + ["-"] * 5
            pos = random.randint(0, 4)
            rnd[pos]=str(smin)
            # result[k] = "f".join([str(name), str(d), str(snom), str(smin), str(max(sr, sr_gost)), *rnd])
        elif re.search(r"плоск",name):
            d = get_max_diameter(v[1])
            sr = round(get_sr_flat_stub(sigma, d,smin, p) + 1, 1)
            sr_gost = get_otbr_thickness(d)
            rnd = [str(round(random.uniform(smin + delta, smin), 1)) for _ in range(5)] + ["-"] * 5
            pos = random.randint(0, 4)
            rnd[pos]=str(smin)
            # result[k] = "f".join([str(name), str(d), str(snom), str(smin), str(max(sr, sr_gost)), *rnd])
        elif re.search(r"фланц",name):
            d = get_max_diameter(v[1])
            sr = round(get_sr_flanc_stub(sigma, d, p) + 1, 1)
            sr_gost = get_otbr_thickness(d)
            rnd = [str(round(random.uniform(smin + delta, smin), 1)) for _ in range(5)] + ["-"] * 5
            pos = random.randint(0, 4)
            rnd[pos]=str(smin)
        result[k] = "f".join([str(name), str(d), str(snom), str(smin), str(max(sr, sr_gost)), *rnd])

    return result


if __name__ == '__main__':
    t150 = {"ВСт3": 145,
            "сталь 10": 122,
            "сталь 20": 139,
            "09Г2С": 171,
            "16ГС": 171,
            "10Г2": 154,
            "17ГС": 157,
            "08Х18Н10Т": 148,
            "13ХФА": 0, }
    for steel in t150:
        print(get_allowed_tension_pipe(steel, 47))
