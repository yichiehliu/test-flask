# from flask import render_template, flash, redirect, url_for, Blueprint, Flask, render_template, request, jsonify
# from app.models import CarStatus, OrderRecord, CarModelRelation, QueryRecord


# query_bp = Blueprint('query', __name__)

# @query_bp.route('/queryforcars', methods=['GET', 'POST'])
# def queryforcar():
#     # from queryform import FormSearchCars
#     # data = request.get_json(force=True)
#     if request.is_json:
#         data = request.get_json()
#     # content_dict = request.get_json()
#     # form = FormSearchCars()
#     st = data['start_time']
#     et = data['end_time']
#     loc = data['location']
#     car_type = data['car_type']
#     qid = data['query_id']

#     rentalperiodcnt = 0

#     for i in range(st, et, 3600):
#         rentalperiodcnt += 1
#     # print(rentalpreriodcnt)

#     # if CarStatus
#     # rentalperiod = dict()
#     # for i in range(st, et + 1):
#     #     rentalperiod.update(i: 0)
#     # result = db.session.execute(
#     #     'SELECT * FROM CarStatus WHERE location = :loc and carAmount > 0 and date >=:st and date <= :et').fetchall()
#     if(car_type == 'unspecified'):
#         carlist = db.session.query(CarModelRelation).join(CarStatus).\
#             filter(and_(CarStatus.location == loc, CarStatus.carAmount > 0, CarStatus.date >= st, CarStatus.date < et)).\
#             group_by(CarStatus.cbmid).\
#             having(func.count('*') == rentalperiodcnt)
#     else:
#         carlist = db.session.query(CarModelRelation).join(CarStatus).\
#             filter(and_(CarModelRelation.car_type == car_type,  CarStatus.location == loc, CarStatus.carAmount > 0, CarStatus.date >= st, CarStatus.date < et)).\
#             group_by(CarStatus.cbmid).\
#             having(func.count('*') == rentalperiodcnt)

#     output = {}

#     for i in carlist:
#         did = int(time.time())
#         output.update(
#             {'query_id': qid, 'deal_id': did, 'brand_id': i.brand_id, 'cbmid_id': i.cbmid, 'car_type': i.car_type, 'model_id': i.model_id, 'price': i.price})
#         db.session.add(QueryRecord(qid=qid, did=did, cbmid=i.cbmid, car_type=i.car_type,
#                                    brand_id=i.brand_id, model_id=i.model_id, price=i.price))
#         db.session.commit()
#     return output
#     # for i in range(st, et + timedelta(days=1)):
#     #
#     #     rentalperiod.append(i)

#     # if form.validate_on_submit():
#     #     carlist = CarStatus.query.filter(
#     #         and_(CarStatus.location == loc, CarStatus.carAmount > 0)).group_by(CarStatus.carType)

#     #
#     #         if (i.carType not in output.values()):
#     #             output.update({'carType': i.carType})
#     #     return jsonify(output)
#     # return render_template('search.html', form=form)
