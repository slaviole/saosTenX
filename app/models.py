from . import db

class Node(db.Model):
    __tablename__ = 'nodes'
    id = db.Column(db.Integer, primary_key=True)
    nodeName = db.Column(db.String(64), unique=True)
    nodeIP = db.Column(db.String(64), unique=True)
    userID = db.Column(db.String(64), unique=False)
    password = db.Column(db.String(64), unique=False)

    def __repr__(self):
        return '<Node %r>' % self.nodeName
#        return str(self.nodeName)

# Flasky has not __str__ function
    def __str__(self):
        return self.nodeName
