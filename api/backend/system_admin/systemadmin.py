from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

administrator = Blueprint('administrator', __name__)
# Route to get all warnings for a specific alumni
@administrator.route('/warnings/<alumni_id>', methods=['GET'])
def get_warnings(alumni_id):
    query = '''
    SELECT Warnings.WarningID, Warnings.Reason, Warnings.TimeStamp, Administrator.Name AS AdminName
    FROM Warnings
    JOIN Administrator ON Warnings.AdminID = Administrator.AdminID
    WHERE Warnings.AlumniID = %s
    ORDER BY Warnings.TimeStamp DESC
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (alumni_id,))
    warnings = cursor.fetchall()

    response = make_response(jsonify(warnings))
    response.status_code = 200
    return response



@administrator.route('/warnings', methods=['GET'])
def get_all_warnings():
    query = '''
    SELECT Warnings.WarningID, Warnings.Reason, Warnings.TimeStamp, 
           Administrator.Name AS AdminName, Alumni.Name AS AlumniName
    FROM Warnings
    JOIN Administrator ON Warnings.AdminID = Administrator.AdminID
    JOIN Alumni ON Warnings.AlumniID = Alumni.AlumniID
    ORDER BY Warnings.TimeStamp DESC
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    warnings = cursor.fetchall()

    response = make_response(jsonify(warnings))
    response.status_code = 200
    return response