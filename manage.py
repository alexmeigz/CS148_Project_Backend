from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from myapp import app
from models import models


manager = Manager(app)
migrate = Migrate(app, models.db)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()