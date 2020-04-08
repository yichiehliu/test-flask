# Smart Contract-Based Distributed Mobility Service Internal API Document

***
We define the API specifications for interacting with match making algorithm (MMA) in this document including availibility check and transaction confirmation.
***

**Flow Chart**

![](https://i.imgur.com/1IX2Hxi.png)

***

## Query For Available Cars (MMA1)

**URL** : `/api/query/queryforcars

**Method** : `GET`

**Query Conditions**
```json
{
    "query_id": "1001",
    "query_time": "1583868012",
    "car_type": "unspecified", //accommodation of the car
    "location": "1",
    "start_time": 1585134000, 
    "end_time": 1585137600
}
```

**Car Type: Unspecified, Sedan, SUV.**

## Success Responses

**Condition** : Successfully query but no available car.

**Code** : `200 OK`

**Content**
```json
{"available_cars": []}
```

### OR

**Condition** : Successfully query and one or more cartypes are available.

**Code** : `200 OK`

**Content** : Array of available cartypes in JSON format

```json
{
    {
        "cbmid":"1000021",
        "brand": "Mercedes Benz",
        "model_id": "s560e", 
        "price": "$80/day"
    },
    {
        "cbmid":"1000022",
        "brand": "BMW",
        "model_id": "M3",
        "price": "$75/day"
    }
}
```

***

## Transaction Confirmation (MMA4)

**URL** : `/api/order/orderconfirmation`

**Method** : `POST`

**Message Body**
```json
{
    "order_id":"100001",
    "user_id": "10001",
    "order_time": "1583868912",
    "location": "1",
    "cbmid":"1000021",
    "start_time": "1584213612",
    "end_time": "1584559212",
}
```

## Success Responses

**Condition** : Successfully order car and update its status.

**Code** : `200 OK`

**Content**
```json
{
    "message": "True",
    "order_id":"100001",
    "user_id": "10001",
    "cbm_id":"1000021",
}
```

## Failed Responses

**Condition** : Fail to order car due to resource unavailable.

**Code** : `409 Conflict`

**Content**
```json
{
    "message": "False",
    "order_id":"100001",
    "user_id": "10001",
    "cbm_id":"1000021",
}
```



***

## Transaction Cancelation (MMA5)

**URL** : `/api/order/ordercancelation`

**Method** : `POST`

**Message Body**
```json
{
    "order_id":"100001"
}
```

## Success Responses

**Condition** : Successfully cancel the order. 

**Code** : `200 OK`

**Content**
```json
{
    "message": "True",
    "order_id":"100001",
}
```


#queryid dealid/dynamic pricing --> status as pending
#Multiple location and 24 hours 3 models