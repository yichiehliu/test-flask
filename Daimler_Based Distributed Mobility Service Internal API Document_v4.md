# Smart Contract-Based Distributed Mobility Service Internal API Document

***
We define the API specifications for interacting with match making algorithm (MMA) in this document including availibility check and transaction confirmation.
***

**Flow Chart**

![](https://i.imgur.com/1IX2Hxi.png)

***

## Query For Available Cars (MMA1)

**URL** : `http://127.0.0.1:5000/api/query/car?params=<Base64_Encoded_Params>`


**Method** : `GET`

**Query Conditions**
```json
{
    "query_id": "1001",
    "query_time": "1583868012",
    "car_type": "unspecified", 
    "location": "('35.815', '139.6853')",
    "start_time": 1585134000, set 30 minutes as a rental time unit, 3600 unix time == 1 hour
    "end_time": 1585137600
}
```

**Car Type: Unspecified, Sedan, SUV.**

## Success Responses

**Condition** : Successfully query but no available car.

**Code** : `200 OK`

**Content**
```json
{} //blank response
```

### OR

**Condition** : Successfully query and one or more cartypes are available.

**Code** : `200 OK`

**Content** : Array of available cartypes in JSON format

```json
[
    [
        {
            "query_id": "1003",
            "location": [
                "('35.815', '139.6853')"
            ],
            "deal_id": 1587232599,
            "brand_id": "Pontiac",
            "bmid_id": "1000022",
            "car_type": "Hatchback",
            "model_id": "SC",
            "price": "3"
        }
    ],
    [
        {
            "query_id": "1003",
            "location": [
                "('35.815', '139.6853')"
            ],
            "deal_id": 1587232600,
            "brand_id": "Nissan",
            "bmid_id": "1000023",
            "car_type": "Coupe, Convertible, Wagon, Sedan",
            "model_id": "458 Italia",
            "price": "4"
        }
    ]
]
```

***

## Transaction Confirmation (MMA4)

**URL** : `http://127.0.0.1:5000/api/order/confirm/car`

**Method** : `POST`

**Message Body**
```json
{
    "query_id": "1003",
    "deal_id": "1587221268", // 正常用deal id 找price
    "order_id":"101231126",
    "order_time": 1583868012,
    "user_id":"10001",
    "bmid": "1000022",
    "location": "('35.815', '139.6853')",
    "start_time": 1585134900, 
    "end_time": 1585138500
}	
```

## Success Responses

**Condition** : Successfully order car and update its status.

**Code** : `200 OK`

**Content**
```json
{
    "bm_id": "1000022",
    "message": true,
    "order_id": "101231126",
    "price": 3,
    "user_id": "10001"
}
```

## Failed Responses

**Condition** : Fail to order car due to resource unavailable.

**Code** : `409 Conflict`

**Content**
```json
{
    "bm_id": "1000022",
    "message": false,
    "order_id": "101231126",
    "price": 3,
    "user_id": "10001"
}
```



***

## Transaction Cancelation (MMA5)

**URL** : `http://127.0.0.1:5000/api/activate/car`

**Method** : `POST`

**Message Body**
```json
{
    "order_id": "101231125",
    "activate_time": 1583868012,
    "user_id": "10001"
}
```

## Success Responses

**Condition** : Successfully cancel the order. 

**Code** : `200 OK`

**Content**
```json
{
{
    "item_id": 1000006,
    "message": true,
    "order_id": "101231125"
}
}
```

## Failed Responses

**Condition** : Fail to cancel order 

**Code** : `409 Conflict`

**Content**
```json
{
    "message": false,
    "item_id": 1000006,
    "order_id": "101231125"
}
```




