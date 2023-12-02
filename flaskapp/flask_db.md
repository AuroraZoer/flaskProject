flask shell
from flaskapp import db
db.create_all()

from flaskapp.models import User
u1 = User(full_name='student1', email='student1@example.com')
u2 = User(full_name='student2', email='student2@example.com')
db.session.add(u1)
db.session.add(u2)
db.session.commit()
users=User.query.all()
for u in users:
    print(u.full_name, u.email)

for u in users:
    db.session.delete(u)

db.session.commit()

