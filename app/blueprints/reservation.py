from datetime import datetime

import numpy as np
from math import *
from flask import Flask, render_template, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask import request, Blueprint
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
import os
from sqlalchemy import and_, func
import json
from datetime import timedelta
import time
from app.models import EscooterAllinfo, EscooterOrderRecord, CarAllinfo, FONLoc, RealtimeCarDetails, RealtimeCarOrderRecord, ReservedCarStatus, QueryRecord, BookingRecord, OrderRecord
from app.extensions import db
from ast import literal_eval as make_tuple

import random
from faker import Faker
from math import radians, sin, cos, acos
import base64
fake = Faker()

resrv_bp = Blueprint('resrv', __name__)
# app = Blueprint('app', __name__)


# ==========================================================================================================================


def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    lat1 = radians(float(lat1))
    lat2 = radians(float(lat2))
    lon1 = radians(float(lon1))
    lon2 = radians(float(lon2))
    radius = 6371  # km
    dist = 6371.01 * acos(sin(lat1)*sin(lat2) + cos(lat1)
                          * cos(lat2)*cos(lon1 - lon2))
    d = dist

    return d  # km


@resrv_bp.route('/query/escooter/123456', methods=['GET', 'POST'])
def test():
    return Response(json.dumps({'output': 123}), mimetype='application/json')


@resrv_bp.route('/query/escooter/', methods=['GET', 'POST'])
def escooter():
    # return render_template('404.html')
    # return Response(json.dumps({'output': 123}), mimetype='application/json')
    params = request.args.get('params', type=str)
    decoded = base64.urlsafe_b64decode(
        params.encode('utf-8')).decode('utf-8')
    data = json.loads(decoded)
    st = data['start_time']
    et = data['end_time']
    user_longnla = data['location']
    sub_type = data['subtype']
    qid = data['query_id']
    query_time = data['query_time']

    rentalperiodcnt = (et-st)/3600

    loc_query = db.session.query(EscooterAllinfo).all()

    output = []

    cntd = 0
    for i in loc_query:
        if (distance(eval(i.location), eval(user_longnla)) <= 5):  # within 5km
            if(i.UsedorNot == False):
                did = str(int(time.time()) + int(qid) + cntd)

                output.append({'query_id': qid, 'location': i.location, 'deal_id': did,
                               'brand_id': i.brand_id, 'bmid': i.bmid, "vehicle_type": "ecsooter",
                               'subtype': i.sub_type, 'item_id': str(i.item_id),
                               'model_id': i.model_id, 'price': str(i.price*rentalperiodcnt)})
                cntd += 1

    return jsonify(output)
    # Response(json.dumps(output), mimetype='application/json')
    # jsonify(output)


@resrv_bp.route('/order/confirm/escooter', methods=['GET', 'POST'])
def scooterorderconfirm():
    output = {}
    if request.is_json:
        data = request.get_json()

    rentalperiodcnt = 0
    rentalperiodcnt = (et-st)/3600
    rentalcnt = 0

    oid = data['order_id']
    uid = data['user_id']
    st = data['start_time']
    et = data['end_time']
    loc = data['location']
    item_id = data['item_id']
    bm_id = data['bm_id']
    scooter = db.session.query(EscooterAllinfo).filter(
        EscooterAllinfo.item_id == item_id, EscooterAllinfo.UsedorNot == False).one()
    output = {
        "message": False,
        "order_id": oid,
        "user_id": uid,
        "bmid": bm_id
    }
    # return {"1": scooter.price}
    if(str(scooter.item_id) == item_id):
        scooter.UsedorNot = True

        order = EscooterOrderRecord(
            oid=data['order_id'],
            uid=data['user_id'],
            created_at=data['order_time'],
            st=data['start_time'],
            et=data['end_time'],
            location=loc,
            item_id=item_id,
            # bmid=data['bmid'],
            # price 應該要用deal id 但目前沒有dynamic pricing 所以就再去db撈一次
            price=scooter.price,
            # bm_id=bm_id,
            status="Confirmed"
        )
        output.update({
            "price": str(db.session.query(EscooterAllinfo).filter(EscooterAllinfo.item_id == item_id).one().price * rentalperiodcnt),
            "message": True
        })
        db.session.add(order)
        db.session.commit()
    else:
        output.update({
            "price": str(db.session.query(EscooterAllinfo).filter(EscooterAllinfo.item_id == item_id).one().price * rentalperiodcnt),
            "message": False
        })

    return jsonify(output)


# 1.Read parameters sended from Blockchain
# 2.Find rental spots within 10km, using Rental Spot & Geographic coordinates Conversion Table to calculate the distances
# 3.Using Car Status Table, which lists out the car amount of the time(one hour basis),
#  the location, and the car type
#  to check the available car type by given the 10-km-apart rental spots firstly,
# user's rental period secondly, and the specified car type thirdly.
# 4.Return the query result of Step 5.3
# 5. Update the the Query_Record Table, the query details
#  the available Car Type, the abailable rental Location, the available Rental time,
# and check if the car amount of those condition is enough

@resrv_bp.route('/query/car', methods=['GET', 'POST'])
def queryforcar():
    params = request.args.get('params', type=str)
    decoded = base64.urlsafe_b64decode(
        params.encode('utf-8')).decode('utf-8')
    # params.decode('utf-8')
    # from queryform import FormSearchCars
    # data = request.get_json(force=True)
    # if request.is_json:
    #     data = request.get_json()
    # else:
    data = json.loads(decoded)
    # st = request.args.get('start_time', type=int)
    # et = request.args.get('end_time', type=int)
    # user_longnla = request.args.get(
    #     'location', default='*', type=str)  # long&lat user_location
    # sub_type = request.args.get('sub_type', default='*', type=str)
    # qid = request.args.get('query_id', type=str)
    # query_time = request.args.get('query_time', type=int)

    # content_dict = request.get_json()
    # form = FormSearchCars()
    st = data['start_time']
    et = data['end_time']
    user_longnla = data['location']
    sub_type = data['subtype']
    qid = data['query_id']
    query_time = data['query_time']

    # find the corresponding long&lat in FONLOC table
    loc_query = db.session.query(FONLoc).all()

    loc_fon = []
    for i in loc_query:
        if (distance(eval(i.longnla), eval(user_longnla)) <= 10):  # within 5km

            loc_fon.append(i.loc)
        print(i.longnla, user_longnla)
        print(distance(eval(i.longnla), eval(user_longnla)))

    print(loc_fon)
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
    # for loc in loc_fon:
    if (sub_type == 'unspecified'):
        for i in loc_fon:
            carlist = db.session.query(CarAllinfo).join(ReservedCarStatus, ReservedCarStatus.bmid == CarAllinfo.bmid).\
                filter(and_(CarAllinfo.location == i, ReservedCarStatus.location == i, ReservedCarStatus.carAmount >
                            0, ReservedCarStatus.date >= st, ReservedCarStatus.date < et)).\
                group_by(ReservedCarStatus.bmid)
    else:
        carlist = db.session.query(CarAllinfo).join(ReservedCarStatus).\
            filter(and_(CarAllinfo.sub_type == sub_type,  ReservedCarStatus.location.in_(loc_fon),
                        ReservedCarStatus.carAmount > 0, ReservedCarStatus.date >= st, ReservedCarStatus.date < et)).\
            group_by(ReservedCarStatus.bmid).\
            having(func.count('*') == 2)
        # .\having(func.count('*') == rentalperiodcnt).all()

    output = []
    print(carlist)
    cntd = 1
    for i in carlist:
        locwlong = ''
        # try:
        print(i)
        did = str(int(time.time()) + int(qid) + cntd)
        locwlong = db.session.query(FONLoc.longnla).filter(
            FONLoc.loc == i.location).one()

        locwlong = "".join(locwlong)

        output.append({'query_id': qid, 'location': locwlong, 'deal_id': did,
                       'brand_id': i.brand_id, 'bmid': i.bmid, "vehicle_type": "car",
                       'subtype': i.sub_type,
                       'model_id': i.model_id, 'price': str(i.price*rentalperiodcnt)})
        db.session.add(QueryRecord(created_at=query_time, qid=qid, did=did, bmid=i.bmid,
                                   st=st, et=et, location=i.location, price=i.price*rentalperiodcnt))
        # db.session.commit()
        # except:
        #     did = int(time.time()) + int(qid) + 1
        #     output.update(
        #         {'query_id': qid, 'deal_id': did, 'brand_id': i.brand_id, 'bmid_id': i.bmid, 'sub_type': i.sub_type, 'model_id': i.model_id, 'price': str(i.price*rentalperiodcnt)})
        #     db.session.add(QueryRecord(id=int(qid)+int(did), qid=qid, did=did, bmid=i.bmid,
        #                                st=st, et=et, location=user_longnla, price=i.price))
        cntd += 1
        print(output)
    db.session.commit()
    return jsonify(output)
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


@resrv_bp.route('/post', methods=['GET', 'POST'])
def post():
    output = {}
    if request.is_json:
        data = request.get_json()
    print(123333, data)


# 1.Read parameters sended from Blockchain
# 2.Using Car Status Table to check the car amount of the car type that user selected,
# with the same logics of Step 5.3
# 3.Return the query result of Step 12.2

# 12.4 If the car amount is enough
# 12.4.1 Update the Car Status Table, the car amount of the choosen car type should minus 1
# 12.4.2 Update the Order Record Table, kept the comfirmed order details
# 12.4.3 Return the order-succeeded messge
# 12.5 If the car amount is not enough
# 12.5.1 The Order is failed, return the order-failed message


@resrv_bp.route('/order/confirm/car/', methods=['GET', 'POST'])
def orderconfirmation():
    output = {}
    if request.is_json:
        data = request.get_json()

    rentalperiodcnt = 0
    rentalcnt = 0
    # API oid, uid, order_time, location, st, et, query_id, deal_id, bm_id
    # DB  uid, oid, created_at, st, et, location,  qd_id, item_id, price, status
    # (不用bm_id price用qdid找) (新增 status, 派item_id)

    oid = data['order_id']
    uid = data['user_id']
    st = data['start_time']
    et = data['end_time']
    locwlong = data['location']
    loc = db.session.query(FONLoc).filter(
        FONLoc.longnla == locwlong).first().loc
    print(loc)
    did = data['deal_id']
    # 應該用did找
    qid = data['query_id']
    bm_id = data['bmid']
    output = {
        "message": False,
        "order_id": oid,
        "user_id": uid,
        "bmid": bm_id
    }

    for i in range(st, et, 3600):  # 1hr = 3600 unix time
        rentalperiodcnt += 1

    # try:
        # 用bm_id看實際上是不是真的這種車有足夠的rental period
        # confirm = db.session.query(CarAllinfo).join(ReservedCarStatus).\
        #     filter(and_(ReservedCarStatus.bmid == bm_id, ReservedCarStatus.location == loc,
        #                 ReservedCarStatus.carAmount > 0, ReservedCarStatus.date >= st, ReservedCarStatus.date < et))
        # rentalcnt = confirm.count()
        # print(rentalcnt, rentalperiodcnt)
        # if (rentalcnt == rentalperiodcnt):
    alteramount = db.session.query(ReservedCarStatus).\
        filter(and_(ReservedCarStatus.bmid == bm_id, ReservedCarStatus.location == loc,
                    ReservedCarStatus.carAmount > 0, ReservedCarStatus.date >= st, ReservedCarStatus.date < et))
    rentalcnt = db.session.query(ReservedCarStatus).\
        filter(and_(ReservedCarStatus.bmid == bm_id, ReservedCarStatus.location == loc,
                    ReservedCarStatus.carAmount > 0, ReservedCarStatus.date >= st, ReservedCarStatus.date < et)).count()

    if (rentalcnt == rentalperiodcnt):
        for i in alteramount:
            i.carAmount = i.carAmount - 1
            print(i.carAmount)
        output.update({
            "price": str(db.session.query(QueryRecord).filter(and_(QueryRecord.qid == qid, QueryRecord.did == did)).first().price),
            "message": True
        })
    else:
        output.update({
            "price": str(db.session.query(QueryRecord).filter(and_(QueryRecord.qid == qid, QueryRecord.did == did)).first().price),
            "message": [rentalcnt, rentalperiodcnt]
        })
        return jsonify(output)

    qdid = db.session.query(QueryRecord).filter(
        and_(QueryRecord.qid == qid, QueryRecord.did == did)).first().id

    order = OrderRecord(
        oid=data['order_id'],
        uid=data['user_id'],
        created_at=data['order_time'],
        qd_id=qdid,
        st=data['start_time'],
        et=data['end_time'],
        location=loc,
        item_id=None,
        # bmid=data['bmid'],
        # price 應該要用deal id 但目前沒有dynamic pricing 所以就再去db撈一次
        price=db.session.query(QueryRecord).filter(
            and_(QueryRecord.qid == qid, QueryRecord.did == did)).first().price,
        bmid=bm_id,
        status="Confirmed"
    )
    db.session.add(order)
    db.session.commit()
    return jsonify(output)
    # else:
    #     return output
    # except (NoResultFound):
    #     return None


@resrv_bp.route('/order/cancel/car', methods=['GET', 'POST'])
def ordercancellation():
    output = {}
    if request.is_json:
        data = request.json

    # find rental st et,car info
    oid = data['order_id']

    findorder = db.session.query(OrderRecord).\
        filter(OrderRecord.oid == oid)

    for i in findorder:
        st = i.st
        et = i.et
        loc = i.location
        bm_id = i.bmid
        i.status = 'Canceled'

    # alter car status
    alteramount = db.session.query(ReservedCarStatus).\
        filter(and_(ReservedCarStatus.bmid == bm_id, ReservedCarStatus.location == loc,
                    ReservedCarStatus.carAmount > 0, ReservedCarStatus.date >= st, ReservedCarStatus.date < et))

    for i in alteramount:
        i.carAmount = i.carAmount+1

    # alter resrv status to canceled

    output.update({'message': True, 'order_id': oid})

    db.session.commit()

    return jsonify(output)


# assign item id(car_id)
@resrv_bp.route('/activate/car', methods=['GET', 'POST'])
def activatecar():
    if(request.method == 'POST'):
        print(12344)
    output = {}
    if request.is_json:
        data = request.get_json()
    oid = data['order_id']

    findorder = db.session.query(OrderRecord).\
        filter(OrderRecord.oid == oid).one()

    st = findorder.st
    et = findorder.et
    loc = findorder.location
    price = findorder.price
    uid = findorder.uid
    bmid = findorder.bmid
    findorder.status = 'activated'

    item_id_first = db.session.query(CarAllinfo).filter(
        and_(CarAllinfo.bmid == bmid, CarAllinfo.UsedorNot == False)).first()

    item_id = str(item_id_first.item_id)
    findorder.item_id = item_id
    item_id_first.UsedorNot = True

    # order = OrderRecord(
    #     oid=data['order_id'],
    #     uid=uid,
    #     order_time=data['order_time'],
    #     item_id=item_id,
    #     st=st,
    #     et=et,
    #     location=loc,
    #     bmid=bmid,
    #     # price 應該要用deal id 但目前沒有dynamic pricing 所以就再去db撈一次
    #     price=price,
    #     status="Ongoing"
    # )
    # db.session.add(order)
    db.session.commit()

    output.update({'message': True, 'order_id': oid, 'item_id': item_id})
    return output


@resrv_bp.route('/return/car', methods=['GET', 'POST'])
def returncar():
    output = {}
    if request.is_json:
        data = request.get_json()

    oid = data['order_id']
    item_id = data['item_id']
    findcar = db.session.query(CarAllinfo).filter(
        CarAllinfo.item_id == item_id).one()
    findodr = db.session.query(OrderRecord).filter(
        OrderRecord.oid == oid).one()

    findcar.UsedorNot = False
    findodr.status = "finished"

    db.session.commit()
    output.update({'message': True, 'order_id': oid, 'item_id': item_id})
    return output
