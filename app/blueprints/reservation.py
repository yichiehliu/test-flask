from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import request, Blueprint
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
import os
from sqlalchemy import and_, func
import json
from datetime import timedelta
import time
from app.models import realtime_models, reserve_models
from app.extensions import db

import random

resrv_bp = Blueprint('resrv', __name__)

@resrv_bp.route('/query/car', methods=['GET', 'POST'])
def queryforcar():
    # from queryform import FormSearchCars
    # data = request.get_json(force=True)
    if request.is_json:
        data = request.get_json()
    # content_dict = request.get_json()
    # form = FormSearchCars()
    st = data['start_time']
    et = data['end_time']
    loc = data['location']
    car_type = data['car_type']
    qid = data['query_id']

    rentalperiodcnt = 0

    for i in range(st, et, 3600):
        rentalperiodcnt += 1
    # print(rentalpreriodcnt)

    # if ReservedCarStatus
    # rentalperiod = dict()
    # for i in range(st, et + 1):
    #     rentalperiod.update(i: 0)
    # result = db.session.execute(
    #     'SELECT * FROM ReservedCarStatus WHERE location = :loc and carAmount > 0 and date >=:st and date <= :et').fetchall()
    if(car_type == 'unspecified'):
        carlist = db.session.query(CarAllinfo).join(ReservedCarStatus).\
            filter(and_(ReservedCarStatus.location == loc, ReservedCarStatus.carAmount > 0, ReservedCarStatus.date >= st, ReservedCarStatus.date < et)).\
            group_by(ReservedCarStatus.bmid).\
            having(func.count('*') == rentalperiodcnt)
    else:
        carlist = db.session.query(CarAllinfo).join(ReservedCarStatus).\
            filter(and_(CarAllinfo.car_type == car_type,  ReservedCarStatus.location == loc, ReservedCarStatus.carAmount > 0, ReservedCarStatus.date >= st, ReservedCarStatus.date < et)).\
            group_by(ReservedCarStatus.bmid).\
            having(func.count('*') == rentalperiodcnt)

    output = {}

    for i in carlist:
        did = random.randint() + int(time.time()) + qid
        output.update(
            {'query_id': qid, 'deal_id': did, 'brand_id': i.brand_id, 'bmid_id': i.bmid, 'car_type': i.car_type, 'model_id': i.model_id, 'price': i.price})
        db.session.add(QueryRecord(qid=qid, did=did, bmid=i.bmid, st = st,et = et,location = location, price=i.price))
        db.session.commit()
    return output
    # for i in range(st, et + timedelta(days=1)):
    #
    #     rentalperiod.append(i)

    # if form.validate_on_submit():
    #     carlist = ReservedCarStatus.query.filter(
    #         and_(ReservedCarStatus.location == loc, ReservedCarStatus.carAmount > 0)).group_by(ReservedCarStatus.carType)

    #
    #         if (i.carType not in output.values()):
    #             output.update({'carType': i.carType})
    #     return jsonify(output)
    # return render_template('search.html', form=form)



@resrv_bp.route('/booking/confirm/car', methods=['GET', 'POST'])
def bookingconfirmation():
    output = {}
    if request.is_json:
        data = request.get_json()

    rentalperiodcnt = 0
    rentalcnt = 0

    rid = data['resrv_id']
    st = data['start_time']
    et = data['end_time']
    loc = data['location']
    bm_id = data['bmid']
    output = {
        "message": "False",
        "resrv_id": rid,
        "user_id": uid,
        "bm_id": bm_id
    }

    for i in range(st, et, 3600): #1hr = 3600 unix time
        rentalperiodcnt += 1

    try:
        confirm = db.session.query(CarAllinfo).join(ReservedCarStatus).\
            filter(and_(ReservedCarStatus.bmid == bm_id, ReservedCarStatus.location == loc,
                        ReservedCarStatus.carAmount > 0, ReservedCarStatus.date >= st, ReservedCarStatus.date < et))
        rentalcnt = confirm.count()
        if (rentalcnt == rentalperiodcnt):
            alteramount = db.session.query(ReservedCarStatus).\
                filter(and_(ReservedCarStatus.bmid == bm_id, ReservedCarStatus.location == loc,
                            ReservedCarStatus.carAmount > 0, ReservedCarStatus.date >= st, ReservedCarStatus.date < et))
            for i in alteramount:
                i.carAmount = i.carAmount-1
            output.update({
                "price":confirm.first().price,
                "message": "True"
            })

            resrv = resrvRecord(
                rid=data['resrv_id'],
                uid=data['user_id'],
                resrv_time=data['resrv_time'],
                did = data['did'],
                st=data['start_time'],
                et=data['end_time'],
                location=data['location'],
                bmid=data['bmid'],
                # price 應該要用deal id 但目前沒有dynamic pricing 所以就再去db撈一次
                price=confirm.first().price,
                resrvStatus="Confirmed"
            )
            db.session.add(resrv)
            db.session.commit()
            return output
        else:
            return output
    except (NoResultFound):
        return output


@resrv_bp.route('/booking/cancel/car', methods=['POST'])
def resrvcancellation():
    output = {}
    if request.is_json:
        data = request.get_json()

    # find rental st et,car info
    rid = data['resrv_id']

    findresrv = db.session.query(resrvRecord).\
        filter(resrvRecord.rid == rid)

    for i in findresrv:
        st = i.st
        et = i.et
        loc = i.location
        bm_id = i.bmid
        i.resrvStatus = 'Canceled'

    # alter car status
    alteramount = db.session.query(ReservedCarStatus).\
        filter(and_(ReservedCarStatus.bmid == bm_id, ReservedCarStatus.location == loc,
                    ReservedCarStatus.carAmount > 0, ReservedCarStatus.date >= st, ReservedCarStatus.date < et))

    for i in alteramount:
        i.carAmount = i.carAmount+1

    # alter resrv status to canceled

    output.update({'message': True, 'resrv_id': rid})

    db.session.commit()

    return output


@resrv_bp.route('/activate/car', methods=['GET', 'POST']) # assign item id(car_id)
def activatecar():
    output = {}
    if request.is_json:
        data = request.get_json()
    bmid = data['bmid']
    rid = data['resrv_id']
    
    findresrv = db.session.query(resrvRecord).\
        filter(resrvRecord.rid == rid)

    for i in findresrv:
        st = i.st
        et = i.et
        loc = i.location
        price = i.price
        uid = i.uid
        i.resrvStatus = 'finished'
    
    item_id_all = db.session.query(CarAllinfo).filter(and_(CarAllinfo.bmid == bmid, CarAllinfo.UsedorNot == False))
    
    for i in item_id_all:
        item_id = i.item_id
        i.UsedorNot = True
        break                                                
    
    order = OrderRecord(
        oid=data['order_id'],
        rid=rid,
        uid=uid,
        order_time=data['order_time'],
        item_id = item_id,
        st=st,
        et=et,
        location=loc,
        bmid=bmid,
        # price 應該要用deal id 但目前沒有dynamic pricing 所以就再去db撈一次
        price=price,
        status="Ongoing"
    )
    db.session.add(order)
    db.session.commit()
    
    output.update({'message': True, 'order_id': oid, 'car_id': item_id})
    return output



@resrv_bp.route('/return/car', methods=['GET', 'POST']) 
def returncar():
    output = {}
    if request.is_json:
        data = request.get_json()
    
    
    oid = data['oid']
    item_id = data['item_id']
    findcar = db.session.query(CarAllinfo).filter(CarAllinfo.item_id == item_id)
    findodr = db.session.query(OrderRecord).filter(OrderRecord.oid == oid)
    
    for i in findcar:
        i.UsedorNot = False
        break
    for i in findodr:
        i.status = "finished"
        break
    
    db.session.commit()
    output.update({'message': True, 'order_id': oid, 'car_id': item_id})
    return output