
from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask import request
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
import os
from sqlalchemy import and_, func
import json
from datetime import timedelta
import time

#  取得啟動文件資料夾路徑
pjdir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
#  新版本的部份預設為none，會有異常，再設置True即可。
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#  設置資料庫為sqlite3
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
                                        os.path.join(
                                            pjdir, 'data0320_12.sqlite')
app.config['SECRET_KEY'] = '\xf0?a\x9a\\\xff\xd4;\x0c\xcbHi'

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)


@app.route('/api/query/queryforcars', methods=['GET', 'POST'])
def queryforcar():
    # from queryform import FormSearchCars
    from Model import CarStatus, OrderRecord, CarModelRelation, QueryRecord, db
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

    # if CarStatus
    # rentalperiod = dict()
    # for i in range(st, et + 1):
    #     rentalperiod.update(i: 0)
    # result = db.session.execute(
    #     'SELECT * FROM CarStatus WHERE location = :loc and carAmount > 0 and date >=:st and date <= :et').fetchall()
    if(car_type == 'unspecified'):
        carlist = db.session.query(CarModelRelation).join(CarStatus).\
            filter(and_(CarStatus.location == loc, CarStatus.carAmount > 0, CarStatus.date >= st, CarStatus.date < et)).\
            group_by(CarStatus.cbmid).\
            having(func.count('*') == rentalperiodcnt)
    else:
        carlist = db.session.query(CarModelRelation).join(CarStatus).\
            filter(and_(CarModelRelation.car_type == car_type,  CarStatus.location == loc, CarStatus.carAmount > 0, CarStatus.date >= st, CarStatus.date < et)).\
            group_by(CarStatus.cbmid).\
            having(func.count('*') == rentalperiodcnt)

    output = {}

    for i in carlist:
        did = int(time.time())
        output.update(
            {'query_id': qid, 'deal_id': did, 'brand_id': i.brand_id, 'cbmid_id': i.cbmid, 'car_type': i.car_type, 'model_id': i.model_id, 'price': i.price})
        db.session.add(QueryRecord(qid=qid, did=did, cbmid=i.cbmid, car_type=i.car_type,
                                   brand_id=i.brand_id, model_id=i.model_id, price=i.price))
        db.session.commit()
    return output
    # for i in range(st, et + timedelta(days=1)):
    #
    #     rentalperiod.append(i)

    # if form.validate_on_submit():
    #     carlist = CarStatus.query.filter(
    #         and_(CarStatus.location == loc, CarStatus.carAmount > 0)).group_by(CarStatus.carType)

    #
    #         if (i.carType not in output.values()):
    #             output.update({'carType': i.carType})
    #     return jsonify(output)
    # return render_template('search.html', form=form)


@app.route('/api/order/orderconfirmation', methods=['GET', 'POST'])
def orderconfirmation():
    from Model import CarStatus, OrderRecord, CarModelRelation, db
    output = {}
    if request.is_json:
        data = request.get_json()

    rentalperiodcnt = 0
    rentalcnt = 0

    oid = data['order_id']
    uid = data['user_id']
    st = data['start_time']
    et = data['end_time']
    loc = data['location']
    cbm_id = data['cbmid']
    output = {
        "message": "False",
        "order_id": oid,
        "user_id": uid,
        "cbm_id": cbm_id
    }

    for i in range(st, et, 3600):
        rentalperiodcnt += 1

    try:
        confirm = db.session.query(CarModelRelation).join(CarStatus).\
            filter(and_(CarStatus.cbmid == cbm_id, CarStatus.location == loc,
                        CarStatus.carAmount > 0, CarStatus.date >= st, CarStatus.date < et))
        rentalcnt = confirm.count()
        if (rentalcnt == rentalperiodcnt):
            alteramount = db.session.query(CarStatus).\
                filter(and_(CarStatus.cbmid == cbm_id, CarStatus.location == loc,
                            CarStatus.carAmount > 0, CarStatus.date >= st, CarStatus.date < et))
            for i in alteramount:
                i.carAmount = i.carAmount-1
            output.update({
                "message": "True"
            })

            order = OrderRecord(
                oid=data['order_id'],
                uid=data['user_id'],
                order_time=data['order_time'],
                ST=data['start_time'],
                ET=data['end_time'],
                location=data['location'],
                cbmid=data['cbmid'],
                # price 應該要用deal id 但目前沒有dynamic pricing 所以就再去db撈一次
                price=confirm.first().price,
                orderStatus="Confirmed"
            )
            db.session.add(order)
            db.session.commit()
            return output
        else:
            return output
    except (NoResultFound):
        return output


@app.route('/api/order/ordercancelation', methods=['POST'])
def ordercancelation():
    from Model import CarStatus, OrderRecord, CarModelRelation, db
    output = {}
    if request.is_json:
        data = request.get_json()

    # find rental st et,car info
    oid = data['order_id']

    findorder = db.session.query(OrderRecord).\
        filter(OrderRecord.oid == oid)

    for i in findorder:
        st = i.ST
        et = i.ET
        loc = i.location
        cbm_id = i.cbmid
        i.orderStatus = 'Canceled'

    # alter car status
    alteramount = db.session.query(CarStatus).\
        filter(and_(CarStatus.cbmid == cbm_id, CarStatus.location == loc,
                    CarStatus.carAmount > 0, CarStatus.date >= st, CarStatus.date < et))

    for i in alteramount:
        i.carAmount = i.carAmount+1

    # alter order status to canceled

    output.update({'message': True, 'order_id': oid})

    db.session.commit()

    return output


if __name__ == '__main__':
    app.debug = True
    app.run()
