from ..extensions import db  # 不用套用實例?


class CarAllinfo(db.Model): # 8 columns
    __tablename__ = 'CarAllinfo'
    item_id = db.Column(db.String, primary_key=True, unique=True)
    bmid = db.Column(db.String, nullable=False)
    car_type = db.Column(db.String, nullable=False)
    brand_id = db.Column(db.String, nullable=False)
    model_id = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String, nullable=False)
    UsedorNot = db.Column(db.String, nullable=False) # Used currently or not
    # cbm = db.relationship('CarStatus', backref='cbm', lazy=True)

    def __init__(self, item_id, bmid, car_type, brand_id, location, model_id, price, UsedorNot):
        self.bmid = bmid
        self.item_id = item_id
        self.car_type = car_type
        self.brand_id = brand_id
        self.model_id = model_id
        self.location = location        
        self.price = price
        self.UsedorNot = UsedorNot

    def __repr__(self):
        return '<CarAllinfo %r>' % self.item_id

class ReservedCarStatus(db.Model):  
    __tablename__ = 'ReservedCarStatus'
    sid = db.Column(db.Integer, primary_key=True, autoincrement=True) # status id
    date = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String, nullable=False)
    bmid = db.Column(db.String, db.ForeignKey('CarAllinfo.bmid'), nullable=False)
    carAmount = db.Column(db.Integer, nullable=False)

    def __init__(self, sid, date, location, bmid, carAmount):
        self.sid = sid
        self.date = date
        self.bmid = bmid
        self.location = location
        self.carAmount = carAmount

    def __repr__(self):
        return '<ReservedCarStatus %r>' % self.sid

class QueryRecord(db.Model):
    __tablename__ = 'QueryRecord'
    qdid = db.Column(db.String, primary_key=True, unique=True)
    qid = db.Column(db.String, nullable=False)
    did = db.Column(db.String, nullable=False)
    bmid = db.Column(db.String, nullable=False)
    st = db.Column(db.Integer, nullable=False)
    et = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    # cbm = db.relationship('CarStatus', backref='cbm', lazy=True)

    def __init__(self, qdid, qid, did, bmid, st, et, location, price):
        self.qdid = qdid
        self.qid = qid
        self.did = did
        self.bmid = bmid
        self.location = location
        self.st = st
        self.et = et
        self.price = price

    def __repr__(self):
        return '<QueryRecord %r>' % self.qdid


# class CarIDAssign(db.Model):
#     __tablename__ = 'IDAssign'
#     cbmid = db.Column(db.Integer, primary_key=True)
#     itemid = db.Column(db.String, nullable=False)

#     def __init__(self, cbmid, itemid):
#         self.cbmid = cbmid
#         self.itemid = itemid

class BookingRecord(db.Model):
    __tablename__ = 'BookingRecord'
    rid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String, nullable=False)
    reserved_time = db.Column(db.Integer, nullable=False)
    st = db.Column(db.Integer, nullable=False)
    et = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String, nullable=False)
    bmid = db.Column(db.String, nullable=False)
    qdid = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    reserveStatus = db.Column(db.String, nullable=False) # canceled/finished/reserved

    def __init__(self, rid, uid, qdid, reserved_time, st, et, location, bmid, price, reserveStatus):
        self.rid = rid
        self.uid = uid
        self.qdid = qdid
        self.reserved_time = reserved_time
        self.st = st
        self.et = et
        self.location = location
        self.bmid = bmid
        self.price = price
        self.reserveStatus = reserveStatus

    def __repr__(self):
        return '<ReservationRecord %r>' % self.rid
        
        
# 真正有租賃紀錄的record
class OrderRecord(db.Model): # After activate the reservation
    __tablename__ = 'OrderRecord'
    oid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rid = db.Column(db.String, nullable=False)
    item_id = db.Column(db.String, nullable=False) # assign a item id
    st = db.Column(db.Integer, nullable=False)
    et = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String, nullable=False) # Abort/Finished/Ongoing

    def __init__(self, rid, oid, item_id, st, et, location, price, status):
        self.rid = rid
        self.oid = oid
        self.item_id = item_id
        # self.reserved_time = reserved_time # activation time ??
        self.st = st
        self.et = et
        self.location = location
        self.status = status
        self.price = price

    def __repr__(self):
        return '<OrderRecord %r>' % self.oid
        
        

# class OrderRecord(ActivatedReservation):
#     __tablename__ = 'OrderRecord'
    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)