from app.extensions import db  # 不用套用實例?
# from geoalchemy2 import Geometry


class EscooterAllinfo(db.Model):
    __tablename__ = 'EscooterAllinfo'
    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bmid = db.Column(db.String, default="0")
    car_type = db.Column(db.String, default="scooter")
    sub_type = db.Column(db.String, default="Wemo")
    brand_id = db.Column(db.String, default="0")
    model_id = db.Column(db.String, default="0")
    price = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String, nullable=False)
    UsedorNot = db.Column(db.Boolean, nullable=False)

    def __init__(self, location, price, UsedorNot):
        # self.bmid = bmid
        # self.car_type = car_type
        # self.sub_type = sub_type
        # self.brand_id = brand_id
        # self.model_id = model_id
        self.location = location
        self.price = price
        self.UsedorNot = UsedorNot

    def __repr__(self):
        return '<EscooterAllinfo %r>' % self.item_id


class EscooterOrderRecord(db.Model):  # After activate the reservation
    __tablename__ = 'EscooterOrderRecord'
    oid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String, nullable=False)
    # rid = db.Column(db.String, db.ForeignKey(
    #     'BookingRecord.rid'), nullable=False)
    # assign a item id
    # qd_id = db.Column(db.String, db.ForeignKey(
    #     'QueryRecord.id'), nullable=True)
    item_id = db.Column(db.String, db.ForeignKey(
        'CarAllinfo.item_id'), nullable=True)
    # bmid = db.Column(db.String, db.ForeignKey(
    #     'CarAllinfo.bmid'), nullable=False)
    created_at = db.Column(db.Integer, server_default=db.func.now())
    st = db.Column(db.Integer, nullable=False)
    et = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    # Booked and Activate and Return car using three url but same database
    # OrderConfirmed(Pending, item_id = 0)
    # -> Activated(Ready to drive(within 20 minutes), assign item_id)
    # -> Finished(Returned the car)
    # Canceled
    status = db.Column(db.String, nullable=False)

    def __init__(self, oid, uid, item_id, created_at,  st, et, location, price, status):
        # self.qd_id = qd_id
        self.uid = uid
        self.oid = oid
        self.item_id = item_id
        self.created_at = created_at
        # self.reserved_time = reserved_time # activation time ??
        self.st = st
        self.et = et
        # self.bmid = bmid
        self.location = location
        self.status = status
        self.price = price

    def __repr__(self):
        return '<EscooterOrderRecord %r>' % self.oid


class CarAllinfo(db.Model):  # 8 columns
    __tablename__ = 'CarAllinfo'
    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bmid = db.Column(db.String, nullable=False)
    car_type = db.Column(db.String, default="car")
    sub_type = db.Column(db.String, nullable=False)
    brand_id = db.Column(db.String, nullable=False)
    model_id = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String, db.ForeignKey(
        'FONLoc.loc'), nullable=False)
    UsedorNot = db.Column(db.Boolean, nullable=False)  # Used currently or not
    # cbm = db.relationship('CarStatus', backref='cbm', lazy=True)

    def __init__(self, bmid, sub_type, brand_id, location, model_id, price, UsedorNot):
        self.bmid = bmid
        # self.car_type = car_type
        self.sub_type = sub_type
        self.brand_id = brand_id
        self.model_id = model_id
        self.location = location
        self.price = price
        self.UsedorNot = UsedorNot

    def __repr__(self):
        return '<CarAllinfo %r>' % self.item_id


class FONLoc(db.Model):
    __tablename__ = 'FONLoc'
    loc = db.Column(db.String, primary_key=True)
    longnla = db.Column(db.String, nullable=False)

    def __init__(self, loc, longnla):
        self.loc = loc
        self.longnla = longnla

    def __repr__(self):
        return '<FONLoc %r>' % self.loc


class ReservedCarStatus(db.Model):
    __tablename__ = 'ReservedCarStatus'
    sid = db.Column(db.Integer, primary_key=True,
                    autoincrement=True)  # status id
    date = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String, nullable=False)
    bmid = db.Column(db.String, db.ForeignKey(
        'CarAllinfo.bmid'), nullable=False)
    carAmount = db.Column(db.Integer, nullable=False)

    def __init__(self, date, location, bmid, carAmount):
        self.date = date
        self.bmid = bmid
        self.location = location
        self.carAmount = carAmount

    def __repr__(self):
        return '<ReservedCarStatus %r>' % self.sid


class QueryRecord(db.Model):
    __tablename__ = 'QueryRecord'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    qid = db.Column(db.String, nullable=False)
    did = db.Column(db.String, nullable=False)
    created_at = db.Column(db.Integer, server_default=db.func.now())
    bmid = db.Column(db.String, db.ForeignKey(
        'CarAllinfo.bmid'), nullable=False)
    st = db.Column(db.Integer, nullable=False)
    et = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    # cbm = db.relationship('CarStatus', backref='cbm', lazy=True)

    def __init__(self, qid, did, bmid, created_at, st, et, location, price):
        self.qid = qid
        self.did = did
        self.created_at = created_at
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
    bmid = db.Column(db.String, db.ForeignKey(
        'CarAllinfo.bmid'), nullable=False)
    qdid = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    # canceled/finished/reserved
    reserveStatus = db.Column(db.String, nullable=False)

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
class OrderRecord(db.Model):  # After activate the reservation
    __tablename__ = 'OrderRecord'
    oid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String, nullable=False)
    # rid = db.Column(db.String, db.ForeignKey(
    #     'BookingRecord.rid'), nullable=False)
    # assign a item id
    qd_id = db.Column(db.String, db.ForeignKey(
        'QueryRecord.id'), nullable=True)
    item_id = db.Column(db.String, db.ForeignKey(
        'CarAllinfo.item_id'), nullable=True)
    bmid = db.Column(db.String, db.ForeignKey(
        'CarAllinfo.bmid'), nullable=False)
    created_at = db.Column(db.Integer, server_default=db.func.now())
    st = db.Column(db.Integer, nullable=False)
    et = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    # Booked and Activate and Return car using three url but same database
    # OrderConfirmed(Pending, item_id = 0)
    # -> Activated(Ready to drive(within 20 minutes), assign item_id)
    # -> Finished(Returned the car)
    # Canceled
    status = db.Column(db.String, nullable=False)

    def __init__(self, oid, uid, qd_id, item_id, created_at, bmid, st, et, location, price, status):
        self.qd_id = qd_id
        self.uid = uid
        self.oid = oid
        self.item_id = item_id
        self.created_at = created_at
        # self.reserved_time = reserved_time # activation time ??
        self.st = st
        self.et = et
        self.bmid = bmid
        self.location = location
        self.status = status
        self.price = price

    def __repr__(self):
        return '<OrderRecord %r>' % self.oid


# class OrderRecord(ActivatedReservation):
#     __tablename__ = 'OrderRecord'
    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)
class RealtimeCarDetails(db.Model):  # 8 columns
    __tablename__ = 'RealtimeCarDetails'
    item_id = db.Column(db.String, primary_key=True, unique=True)
    bmid = db.Column(db.String, nullable=False)
    car_type = db.Column(db.String, nullable=False)
    brand_id = db.Column(db.String, nullable=False)
    model_id = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String, nullable=False)
    UsedorNot = db.Column(db.String, nullable=False)  # Used currently or not
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
        return '<RealtimeCarDetails %r>' % self.item_id


class RealtimeCarOrderRecord(db.Model):  # 即時
    __tablename__ = 'RealtimeCarOrderRecord'
    item_id = db.Column(db.String, nullable=False)
    oid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    st = db.Column(db.Integer, nullable=False)
    et = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)  # Abort/Finished/Ongoing

    def __init__(self, oid, item_id, st, et, price, location, status):
        self.item_id = item_id
        self.oid = oid
        self.location = location
        # self.reserved_time = reserved_time # activation time ??
        self.st = st
        self.et = et
        self.status = status
        self.price = price

    def __repr__(self):
        return '<RealtimeCarOrderRecord %r>' % self.oid
