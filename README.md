# API
---
## Get n latest pictures

**URL** : `/api/<n>`

**Parameter format** : Integer in range 1-256

**Method** : `GET`

**Success response example**:

```json
[
    {
        "date": "02-10-2017",
        "image": "21191304_10212053347583920_608589068_o.jpg"
    },
    {
        "date": "01-10-2017",
        "image": "21191188_10212053348583945_2086216017_o.jpg"
    },
    ...
]
```

## Get picture at specific date

**URL** : `/api/date/<date>`

**Parameter format** : dd-mm-yyyy

**Method** : `GET`

**Success response example**:

```json
[
    {
        "date": "02-10-2017",
        "image": "21191304_10212053347583920_608589068_o.jpg"
    }
]
```