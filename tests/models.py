"""Models for test suite."""
import datetime

from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Cloud(db.Model):
    """A group of machines connected in a cloud."""
    __tablename__ = 'cloud'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

    def __str__(self):
        return self.name

class Machine(db.Model):
    """A single machine which is part of a cloud deployment."""
    __tablename__ = 'machine'

    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String, nullable=False)
    operating_system = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    cloud_id = db.Column(db.Integer, db.ForeignKey('cloud.id'))
    cloud = db.relationship('Cloud')
    is_running = db.Column(db.Boolean, default=False, nullable=False)
    last_started_at = db.Column(db.DateTime, default=datetime.datetime.now())

    def __str__(self):
        """Return string representation."""
        return self.hostname
