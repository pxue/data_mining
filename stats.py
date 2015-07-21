# -*- coding: utf-8 -*-

import os
from collections import defaultdict

items = defaultdict(list)
for fname in [f for f in os.listdir(".") if "tsv" in f][-1:]:
    with open(fname) as file:

        for line in file:
            name, price, unit, type = line.strip().split("\t")
            if type != "Meat":
                continue

            items[name.decode("utf-8")].append(float(price))

print [(k, v) for k, v in items.iteritems() if v[-1] < 5]
