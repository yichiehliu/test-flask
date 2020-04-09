from models import CarStatus, OrderRecord, CarModelRelation, db
#  實作類別
first = CarStatus(sid=1, date='1585134000', location='1',
                  cbmid='1000021', carAmount=20)
second = CarStatus(sid=2, date='1585134900', location='1',
                   cbmid='1000021', carAmount=20)
third = CarModelRelation(cbmid='1000021', car_type='SUV', brand_id='BMW',
                         model_id='7070', price='75')
# second = CarStatus(sid=2, date='20200303', location='1',
#                    carType='7070', carAmount=20)

#  寫入資料
db.session.add(first)
db.session.add(second)
db.session.add(third)
db.session.commit()
