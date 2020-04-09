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
    "car_type": "unspecified", 
    "location": "1",
    "start_time": 1585134000, set 30 minutes as a rental time unit
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
{
    {
        "query_id":"1001", only one query id for each query, and it's from smart contract.
        "deal_id": "1586115520", set search time as deal id. It's unique.
        "cbmid":"1000021",
        "car_type":"SUV",
        "brand_id": "Mercedes Benz",
        "model_id": "s560e", 
        "price": "$80/day"
    },
    {
        "query_id":"1001",
        "deal_id": "1586116043",
        "cbmid":"1000022",
        "car_type":"SUV",
        "brand_id": "BMW",
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
    "deal_id": "1586116043", // 正常用deal id 找price
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

**URL** : `/api/order/ordercancellation`

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

## Failed Responses

**Condition** : Fail to cancel order 

**Code** : `409 Conflict`

**Content**
```json
{
    "message": "False",
    "order_id":"100001",
}
```




