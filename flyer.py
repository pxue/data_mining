#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests, ujson, re
from datetime import date

flyer_url = 'https://www.loblaws.ca/banners/publication/v1/en_CA/LOB/current/1000/items?start=0&rows=300&tag=%s'

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'X-Requested-With': 'XMLHttpRequest',
}

fdir = "data"
fname = '-'.join([str(d) for d in date.today().isocalendar()[:2]])
WEIGHT = re.compile(r"\d+ [g](?!\w)|\d+ lb")

with open(fdir+fname+".tsv", "w") as f:
    for cat in ["Meat", "Produce"]:
        tag = "lclonline/Flyers/Category/%s" % cat

        response = requests.post(flyer_url % tag, headers=headers)
        flyer = ujson.decode(response.text)

        for item in flyer["flyerResponse"]["docs"]:
            clean = item["priceString"].replace("<sup>", ".").\
                replace("</sup>", "").replace(".$", "").split(" lb/")

            base_unit = "lb"
            if not len(clean) > 1:
                result = WEIGHT.findall(item["description"])
                base_unit = result[0] if len(result) > 0 else ""

            f.write("%s\t%s\t%s\t%s\n" % (
                    item["productTitle"].encode("utf-8"),
                    clean[0].encode("utf-8"),
                    base_unit.encode("utf-8"),
                    cat))
