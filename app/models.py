from app.extensions import db  # 不用套用實例?

class CarStatus(db.Model):  # 三個月內?
    __tablename__ = 'CarStatus'
    sid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Integer, nullable=False)
    # location_ew = db.Column(db.String, nullable=False)
    # location_ns = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    cbmid = db.Column(db.Integer, db.ForeignKey(
        'CarModelRelation.cbmid'), nullable=False)
    carAmount = db.Column(db.Integer, nullable=False)

    def __init__(self, sid, date, location, cbmid, carAmount):
        self.sid = sid
        self.date = date
        # self.location_ew = location_ew
        # self.location_ns = location_ns
        self.cbmid = cbmid
        self.location = location
        self.carAmount = carAmount

    def __repr__(self):
        return '<CarStatus %r>' % self.sid


class CarModelRelation(db.Model):
    __tablename__ = 'CarModelRelation'
    cbmid = db.Column(db.Integer, primary_key=True, unique=True)
    car_type = db.Column(db.String, nullable=False)
    brand_id = db.Column(db.String, nullable=False)
    model_id = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    # cbm = db.relationship('CarStatus', backref='cbm', lazy=True)

    def __init__(self, cbmid, car_type, brand_id, model_id, price):
        self.cbmid = cbmid
        self.car_type = car_type
        self.brand_id = brand_id
        self.model_id = model_id
        self.price = price

    def __repr__(self):
        return '<CarModelRelation %r>' % self.cbmid


class QueryRecord(db.Model):
    __tablename__ = 'QueryRecord'
    qid = db.Column(db.String, nullable=False)
    did = db.Column(db.String, primary_key=True, unique=True)
    cbmid = db.Column(db.Integer, nullable=False)
    car_type = db.Column(db.String, nullable=False)
    brand_id = db.Column(db.String, nullable=False)
    model_id = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    # cbm = db.relationship('CarStatus', backref='cbm', lazy=True)

    def __init__(self, qid, did, cbmid, car_type, brand_id, model_id, price):
        self.qid = qid
        self.did = did
        self.cbmid = cbmid
        self.car_type = car_type
        self.brand_id = brand_id
        self.model_id = model_id
        self.price = price

    def __repr__(self):
        return '<CarModelRelation %r>' % self.cbmid


class CarIDAssign(db.Model):
    __tablename__ = 'CarIDAssign'
    cbmid = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.String, nullable=False)

    def __init__(self, cbmid, car_id):
        self.cbmid = cbmid
        self.car_id = car_id


class OrderRecord(db.Model):
    __tablename__ = 'OrderRecord'
    oid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String, nullable=False)
    order_time = db.Column(db.Integer, nullable=False)
    ST = db.Column(db.Integer, nullable=False)
    ET = db.Column(db.Integer, nullable=False)
    # location_ew = db.Column(db.String, nullable=False)
    # location_ns = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    cbmid = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    orderStatus = db.Column(db.String, nullable=False)

    def __init__(self, oid, uid, order_time, ST, ET, location, cbmid, price, orderStatus):
        self.oid = oid
        self.uid = uid
        self.order_time = order_time
        self.ST = ST
        self.ET = ET
        # self.location_ew = location_ew
        # self.location_ns = location_ns
        self.location = location
        self.cbmid = cbmid
        self.price = price
        self.orderStatus = orderStatus

    def __repr__(self):
        return '<OrderRecord %r>' % self.oid
