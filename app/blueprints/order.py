# from flask import Flask, render_template, jsonify
# from flask_sqlalchemy import SQLAlchemy
# from flask import request, Blueprint
# from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
# import os
# from sqlalchemy import and_, func
# import json
# from datetime import timedelta
# import time
# from app.models import CarStatus, OrderRecord, CarModelRelation, QueryRecord

# order_bp = Blueprint('order', __name__)

# @order_bp.route('/orderconfirmation', methods=['GET', 'POST'])
# def orderconfirmation():
#     output = {}
#     if request.is_json:
#         data = request.get_json()

#     rentalperiodcnt = 0
#     rentalcnt = 0

#     oid = data['order_id']
#     uid = data['user_id']
#     st = data['start_time']
#     et = data['end_time']
#     loc = data['location']
#     cbm_id = data['cbmid']
#     output = {
#         "message": "False",
#         "order_id": oid,
#         "user_id": uid,
#         "cbm_id": cbm_id
#     }

#     for i in range(st, et, 3600):
#         rentalperiodcnt += 1

#     try:
#         confirm = db.session.query(CarModelRelation).join(CarStatus).\
#             filter(and_(CarStatus.cbmid == cbm_id, CarStatus.location == loc,
#                         CarStatus.carAmount > 0, CarStatus.date >= st, CarStatus.date < et))
#         rentalcnt = confirm.count()
#         if (rentalcnt == rentalperiodcnt):
#             alteramount = db.session.query(CarStatus).\
#                 filter(and_(CarStatus.cbmid == cbm_id, CarStatus.location == loc,
#                             CarStatus.carAmount > 0, CarStatus.date >= st, CarStatus.date < et))
#             for i in alteramount:
#                 i.carAmount = i.carAmount-1
#             output.update({
#                 "message": "True"
#             })

#             order = OrderRecord(
#                 oid=data['order_id'],
#                 uid=data['user_id'],
#                 order_time=data['order_time'],
#                 ST=data['start_time'],
#                 ET=data['end_time'],
#                 location=data['location'],
#                 cbmid=data['cbmid'],
#                 # price 應該要用deal id 但目前沒有dynamic pricing 所以就再去db撈一次
#                 price=confirm.first().price,
#                 orderStatus="Confirmed"
#             )
#             db.session.add(order)
#             db.session.commit()
#             return output
#         else:
#             return output
#     except (NoResultFound):
#         return output


# @order_bp.route('/ordercancelation', methods=['POST'])
# def ordercancelation():
#     output = {}
#     if request.is_json:
#         data = request.get_json()

#     # find rental st et,car info
#     oid = data['order_id']

#     findorder = db.session.query(OrderRecord).\
#         filter(OrderRecord.oid == oid)

#     for i in findorder:
#         st = i.ST
#         et = i.ET
#         loc = i.location
#         cbm_id = i.cbmid
#         i.orderStatus = 'Canceled'

#     # alter car status
#     alteramount = db.session.query(CarStatus).\
#         filter(and_(CarStatus.cbmid == cbm_id, CarStatus.location == loc,
#                     CarStatus.carAmount > 0, CarStatus.date >= st, CarStatus.date < et))

#     for i in alteramount:
#         i.carAmount = i.carAmount+1

#     # alter order status to canceled

#     output.update({'message': True, 'order_id': oid})

#     db.session.commit()

#     return output
