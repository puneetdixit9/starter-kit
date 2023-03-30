data = {
    "2023-03-26": {
        "Category 1": {
            "created_on": "Fri, 24 Mar 2023 12:05:28 GMT",
            "demand": 308,
            "id": 1,
            "updated_on": "Fri, 24 Mar 2023 12:05:28 GMT"
        },
        "Category 2": {
            "created_on": "Fri, 24 Mar 2023 12:05:28 GMT",
            "demand": 553,
            "id": 2,
            "updated_on": "Fri, 24 Mar 2023 12:05:28 GMT"
        },
        "Category 3": {
            "created_on": "Fri, 24 Mar 2023 12:05:28 GMT",
            "demand": 900,
            "id": 3,
            "updated_on": "Fri, 24 Mar 2023 12:05:28 GMT"
        },
        "Category 4": {
            "created_on": "Fri, 24 Mar 2023 12:05:28 GMT",
            "demand": 500,
            "id": 4,
            "updated_on": "Fri, 24 Mar 2023 12:05:28 GMT"
        },
        "total": 2261
    },
    "2023-03-27": {
        "Category 1": {
            "created_on": "Fri, 24 Mar 2023 12:05:28 GMT",
            "demand": 983,
            "id": 5,
            "updated_on": "Fri, 24 Mar 2023 12:05:28 GMT"
        },
        "Category 2": {
            "created_on": "Fri, 24 Mar 2023 12:05:28 GMT",
            "demand": 530,
            "id": 6,
            "updated_on": "Fri, 24 Mar 2023 12:05:28 GMT"
        },
        "Category 3": {
            "created_on": "Fri, 24 Mar 2023 12:05:28 GMT",
            "demand": 90,
            "id": 7,
            "updated_on": "Fri, 24 Mar 2023 12:05:28 GMT"
        },
        "Category 4": {
            "created_on": "Fri, 24 Mar 2023 12:05:28 GMT",
            "demand": 562,
            "id": 8,
            "updated_on": "Fri, 24 Mar 2023 12:05:28 GMT"
        },
        "total": 2165
    },
    "2023-03-28": {
        "Category 1": {
            "created_on": "Fri, 24 Mar 2023 12:05:28 GMT",
            "demand": 380,
            "id": 9,
            "updated_on": "Fri, 24 Mar 2023 12:05:28 GMT"
        },
        "Category 2": {
            "created_on": "Fri, 24 Mar 2023 12:05:28 GMT",
            "demand": 532,
            "id": 10,
            "updated_on": "Fri, 24 Mar 2023 12:05:28 GMT"
        },
        "Category 3": {
            "created_on": "Fri, 24 Mar 2023 12:05:28 GMT",
            "demand": 234,
            "id": 11,
            "updated_on": "Fri, 24 Mar 2023 12:05:28 GMT"
        },
        "Category 4": {
            "created_on": "Fri, 24 Mar 2023 12:05:28 GMT",
            "demand": 456,
            "id": 12,
            "updated_on": "Fri, 24 Mar 2023 12:05:28 GMT"
        },
        "total": 1602
    },
    "extra": {
        "Category 1": 1671,
        "Category 2": 1615,
        "Category 3": 1224,
        "Category 4": 1518,
        "total": 6028
    }
}

output = []
for date in data:
    if date == "extra":
        continue
    for cat in data[date]:
        if cat == "total":
            continue
        print(cat)
        data[date][cat].update({
            "date": date,
            "category": cat,
        })
        output.append(data[date][cat])

print(output)
