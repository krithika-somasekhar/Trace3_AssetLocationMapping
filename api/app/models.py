from . import db

class AssetThumbnail(db.Model):
    __tablename__ = 'asset_thumbnail'
    asset_thumb_id = db.Column(db.Integer, primary_key=True)
    asset_thumb_name = db.Column(db.String(255), nullable=False)
    asset_thumb_url = db.Column(db.String(500), nullable=False)

class Map(db.Model):
    __tablename__ = 'map'
    map_id = db.Column(db.Integer, primary_key=True)
    map_building = db.Column(db.String(255), nullable=False)
    map_floor = db.Column(db.Integer, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)

class Room(db.Model):
    __tablename__ = 'room'
    room_id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String(255), nullable=False)
    room_floor_no = db.Column(db.Integer, nullable=False)
    room_shape = db.Column(db.Enum('rectangle', 'semicircle', 'square'), nullable=False)
    gridxx = db.Column(db.Integer, nullable=False)
    gridxy = db.Column(db.Integer, nullable=False)
    gridyx = db.Column(db.Integer, nullable=False)
    gridyy = db.Column(db.Integer, nullable=False)
    map_id = db.Column(db.Integer, db.ForeignKey('map.map_id', ondelete="SET NULL"))

class Department(db.Model):
    __tablename__ = 'department'
    department_id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(255), nullable=False)
    gridxx = db.Column(db.Integer, nullable=False)
    gridxy = db.Column(db.Integer, nullable=False)
    gridyx = db.Column(db.Integer, nullable=False)
    gridyy = db.Column(db.Integer, nullable=False)
    map_id = db.Column(db.Integer, db.ForeignKey('map.map_id', ondelete="SET NULL"))

class Asset(db.Model):
    __tablename__ = 'asset'
    asset_id = db.Column(db.Integer, primary_key=True)
    asset_name = db.Column(db.String(255), nullable=False)
    asset_type = db.Column(db.String(100), nullable=False)
    asset_thumb_id = db.Column(db.Integer, db.ForeignKey('asset_thumbnail.asset_thumb_id', ondelete="SET NULL"))
    room_id = db.Column(db.Integer, db.ForeignKey('room.room_id', ondelete="SET NULL"))
    gridx = db.Column(db.Integer, nullable=False)
    gridy = db.Column(db.Integer, nullable=False)

class Contract(db.Model):
    __tablename__ = 'contract'
    contract_id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    is_expired_flag = db.Column(db.Boolean, default=False)
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.asset_id', ondelete="CASCADE"))
