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

from datetime import timedelta

def convert_timedelta(timedelta_obj):
    if isinstance(timedelta_obj, timedelta):
        return timedelta_obj.total_seconds()  # Convert to seconds
    return timedelta_obj  # If it's not a timedelta, return as is

# Function to convert timedelta to seconds
def convert_timedelta(timedelta_obj):
    if isinstance(timedelta_obj, timedelta):
        return timedelta_obj.total_seconds()  # Convert to seconds
    return timedelta_obj  # If it's not a timedelta, return as is

# Route to get all performance metrics (including ResponseTime) for a specific MetricID
@administrator.route('/performance-metrics/<metric_id>', methods=['GET'])
def get_performance_metrics(metric_id):
    query = '''
    SELECT MetricID, ResponseTime, UpTime, TimeStamp
    FROM PerformanceMetrics
    WHERE MetricID = %s
    ORDER BY TimeStamp DESC
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (metric_id,))
    performance_metrics = cursor.fetchall()

    # If no data is found, return an appropriate message
    if not performance_metrics:
        response = make_response(jsonify({"message": "Performance metrics not found"}))
        response.status_code = 404
        return response

    # Convert ResponseTime and UpTime (if timedelta) to seconds
    performance_metrics = [
        {
            "MetricID": row["MetricID"],
            "ResponseTime": convert_timedelta(row["ResponseTime"]),
            "UpTime": convert_timedelta(row["UpTime"]),
            "TimeStamp": row["TimeStamp"]
        } 
        for row in performance_metrics
    ]

    # Return the performance metrics data
    response = make_response(jsonify(performance_metrics))
    response.status_code = 200
    return response


@administrator.route('/roles', methods=['GET'])
def get_roles():
    query = '''
    SELECT Role, COUNT(*) as Count
    FROM Administrator
    GROUP BY Role
    ORDER BY Count DESC
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    roles = cursor.fetchall()

    response = make_response(jsonify(roles))
    response.status_code = 200
    return response