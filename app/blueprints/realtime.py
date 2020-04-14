from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import request, Blueprint
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy import and_, func
from datetime import timedelta
from app.models import realtime_models, reserve_models
from app.extensions import db
import random, math, time, json, os
from ast import literal_eval as make_tuple

realtime_bp = Blueprint('realtime', __name__)

def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 # km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d #km

@realtime_bp.route('/query/car', methods=['GET', 'POST'])
def realtimequeryforcar():
    cars = {}
    # from queryform import FormSearchCars
    # data = request.get_json(force=True)
    if request.is_json:
        data = request.get_json()
        
    user_loc = make_tuple(data['user_loc'])
    # item_id = data['item_id']
    
    item_id_all = db.session.query(RealtimeCarDetails).filter(RealtimeCarDetails.UsedorNot == False)
    
    for i in item_id_all:
        carloc = make_tuple(i.location)
        if(distance(carloc,user_loc) <= 5): #within 5km
            cars.update({i.item_id, i.price})

    return cars


@realtime_bp.route('/activate/car', methods=['GET', 'POST']) # assign item id(car_id)
def realtimeactivatecar():
    output = {}
    if request.is_json:
        data = request.get_json()
        
    item_id = data['item_id']
    
    item_id_all = db.session.query(RealtimeCarDetails).filter(RealtimeCarDetails.item_id == item_id)

    for i in item_id_all:
        i.UsedorNot = True
        price=i.price                                          

        order = RealtimeCarOrderRecord(
            oid=data['order_id'],
            uid=data['uid'],
            order_time=data['order_time'],
            item_id = item_id,
            st=data['start_time'],
            et=data['end_time'],
            location=i.location,
            # price 應該要用deal id 但目前沒有dynamic pricing 所以就再去db撈一次
            price=i.price, #應該用租的時間再算一次
            status="Ongoing"
        )
    db.session.add(order)
    db.session.commit()
    
    output.update({'message': True, 'order_id': oid, 'price':price})
    return output


@realtime_bp.route('/return/car', methods=['GET', 'POST']) 
def realtimereturncar():
    output = {}
    if request.is_json:
        data = request.get_json()
    
    
    oid = data['order_id']
    item_id = data['item_id']
    et = date['end_time']
    findcar = db.session.query(RealtimeCarDetails).filter(RealtimeCarDetails.item_id == item_id)
    findodr = db.session.query(RealtimeCarOrderRecord).filter(RealtimeCarOrderRecord.oid == oid)
    
    for i in findcar:
        i.UsedorNot = False #訂單完成，車子歸還
        break
    for i in findodr:
        #確認還車時間和當初填的order一樣
        if(i.et == et):
            i.status = "finished" #訂單完成，狀態變更
            output.update({'message': True, 'order_id': oid})
        else:
            output.update({'message': False, 'order_id': oid}) #另外算price，這裡先不定義price應該要怎麼算，先回傳false
        break
    
    db.session.commit()
    
    return output