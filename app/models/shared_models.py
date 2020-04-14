from app.extensions import db 



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

# 真正有租賃紀錄的record
class OrderRecord(db.Model):
    __tablename__ = 'OrderRecord'
    oid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String, nullable=False)
    order_time = db.Column(db.Integer, nullable=False)
    ST = db.Column(db.Integer, nullable=False)
    ET = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String, nullable=False)
    itemid = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    orderStatus = db.Column(db.String, nullable=False)

    def __init__(self, oid, uid, order_time, ST, ET, location, itemid, price, orderStatus):
        self.oid = oid
        self.uid = uid
        self.order_time = order_time
        self.ST = ST
        self.ET = ET
        # self.location_ew = location_ew
        # self.location_ns = location_ns
        self.location = location
        self.itemid = itemid
        self.price = price
        self.orderStatus = orderStatus

    def __repr__(self):
        return '<OrderRecord %r>' % self.oid