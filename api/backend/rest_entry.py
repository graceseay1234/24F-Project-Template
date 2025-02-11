from flask import Flask

from backend.db_connection import db
from backend.alumni.alumni_routes import alumni
from backend.system_admin.systemadmin_routes import administrator
from backend.feedback.feedback_routes import feedback
from backend.candidate.candidate_routes import candidate
from backend.messages.message_routes import message
import os
from dotenv import load_dotenv

from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort



def create_app():
    app = Flask(__name__)


    # Load environment variables
    # This function reads all the values from inside
    # the .env file (in the parent folder) so they
    # are available in this file.  See the MySQL setup 
    # commands below to see how they're being used.
    load_dotenv()

    # secret key that will be used for securely signing the session 
    # cookie and can be used for any other security related needs by 
    # extensions or your application
    # app.config['SECRET_KEY'] = 'someCrazyS3cR3T!Key.!'
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # # these are for the DB object to be able to connect to MySQL. 
    # app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_USER'] = os.getenv('DB_USER').strip()
    app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_ROOT_PASSWORD').strip()
    app.config['MYSQL_DATABASE_HOST'] = os.getenv('DB_HOST').strip()
    app.config['MYSQL_DATABASE_PORT'] = int(os.getenv('DB_PORT').strip())
    app.config['MYSQL_DATABASE_DB'] = os.getenv('DB_NAME').strip()  # Change this to your DB name

    # Initialize the database object with the settings above. 
    app.logger.info('current_app(): starting the database connection')
    db.init_app(app)


    # Register the routes from each Blueprint with the app object
    # and give a url prefix to each
    app.logger.info('current_app(): registering blueprints with Flask app object.')   
 #   app.register_blueprint(simple_routes) #Flask, this collection of routes, please respond to them.
  #  app.register_blueprint(customers,   url_prefix='/c')
    #app.register_blueprint(products,    url_prefix='/p') 
    app.register_blueprint(alumni)
    app.register_blueprint(administrator, url_prefix='/administrators')
    app.register_blueprint(feedback)
    app.register_blueprint(candidate)
    app.register_blueprint(message)
    # Register the Blueprint

    # Don't forget to return the app object
    return app

