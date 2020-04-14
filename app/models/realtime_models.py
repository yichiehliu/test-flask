from app.extensions import db  # 不用套用實例?

class RealtimeCarDetails(db.Model): # 8 columns
    __tablename__ = 'RealtimeCarDetails'
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
        return '<RealtimeCarDetails %r>' % self.item_id

class RealtimeCarOrderRecord(db.Model):  # 即時
    __tablename__ = 'RealtimeCarOrderRecord'
    item_id = db.Column(db.String, nullable=False)
    oid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    st = db.Column(db.Integer, nullable=False)
    et = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False) # Abort/Finished/Ongoing
    
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