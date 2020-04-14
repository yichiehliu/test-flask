from models import realtime_models, reserve_models
#  實作類別
# CarAllinfo
# ReservedCarStatus
# QueryRecord
# BookingRecord
# OrderRecord
# RealtimeCarDetails
# RealtimeCarOrderRecord

first = ReservedCarStatus(sid=1, date='1585134000', location='1',
                  bmid='1000021', carAmount=20)

second = ReservedCarStatus(sid=2, date='1585134900', location='1',
                   bmid='1000021', carAmount=20)

third = CarAllinfo(item_id='100000000', bmid='1000021', car_type='SUV', brand_id='BMW',
                         model_id='7070', price='75', location='1', UsedorNot = False)

four = CarAllinfo(item_id='100000001', bmid='1000021', car_type='SUV', brand_id='BMW',
                         model_id='7070', price='75',location='1', UsedorNot = False)

fif = CarAllinfo(item_id='100000002', bmid='1000021', car_type='SUV', brand_id='BMW',
                         model_id='7070', price='75',location='1', UsedorNot = False)

six = RealtimeCarDetails(item_id='100000010', bmid='1000021', car_type='SUV', brand_id='BMW',
                         model_id='7070', price='75', location='(110.0123,23.32435)', UsedorNot = False)

sev = RealtimeCarDetails(item_id='100000012', bmid='1000021', car_type='SUV', brand_id='BMW',
                         model_id='7070', price='75', location='(110.0123,23.32435)', UsedorNot = False)

# second = CarStatus(sid=2, date='20200303', location='1',
#                    carType='7070', carAmount=20)

#  寫入資料
db.session.add(first)
db.session.add(second)
db.session.add(third, four, fif, six ,sev)
db.session.commit()
