from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from utils import make_response
from db_operations import add_transaction, get_account_data, get_all_transactions
from models import Transaction, db
from routes import transaction_bp
from flasgger import Swagger


def create_app(config=None):
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:password@db/tymebank'

    if config:
        app.config.update(config)

    db.init_app(app)
    migrate = Migrate(app, db)
    app.config['SWAGGER'] = {
        'title': 'Bank transaction API',
        'uiversion': 3
    }
    swagger = Swagger(app)
    app.register_blueprint(transaction_bp, url_prefix='/transactions')
    return app


app = create_app()


@app.route('/')
def index():
    account_data = get_account_data()
    return render_template('index.html', data=account_data)


@app.route('/account')
def get_account_detail():
    account_data = get_account_data()
    return make_response(status=200, message=None, success=True, data=account_data)


if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0')
