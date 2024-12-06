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
    SELECT w.WarningID, w.Reason, w.TimeStamp, a.Name AS Admin_name
    FROM Warnings w
    INNER JOIN Administrator a ON w.AdminID = a.AdminID
    WHERE w.AlumniID = %s
    ORDER BY w.Timestamp DESC
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
    SELECT w.WarningID, w.Reason, w.TimeStamp, 
           a.Name AS admin_name, al.Name AS AlumniName
    FROM Warnings w
    INNER JOIN Administrator a ON w.AdminID = a.AdminID
    INNER JOIN Alumni al ON w.AlumniID = al.AlumniID
    ORDER BY w.Timestamp DESC
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
    SELECT Role, COUNT(*) AS count
    FROM Administrator
    GROUP BY Role
    ORDER BY count DESC
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    roles = cursor.fetchall()
    response = make_response(jsonify(roles))
    response.status_code = 200
    return response

#Retrieve system health metrics
@administrator.route('/metrics/system', methods=['GET'])
def get_system_metrics():
    query = '''
    SELECT MetricID, Uptime, ErrorCount, DatabaseLoad, Timestamp
    FROM PerformanceMetrics
    ORDER BY Timestamp DESC
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    metrics = cursor.fetchall()
    response = make_response(jsonify(metrics))
    response.status_code = 200
    return response

#Retrieve logs of Admin actions
@administrator.route('/actions', methods=['GET'])
def get_admin_actions():
    query = '''
    SELECT ActionID, ActionType, Timestamp, AdminID
    FROM Actions
    ORDER BY Timestamp DESC
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    actions = cursor.fetchall()
    response = make_response(jsonify(actions))
    response.status_code = 200
    return response

#Log a new admin action
@administrator.route('/actions', methods=['POST'])
def log_admin_action():
    data = request.get_json()
    action_type = data.get('action_type')
    admin_id = data.get('admin_id')
    query = '''
    INSERT INTO Actions (ActionType, AdminID)
    VALUES (%s, %s)
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (action_type, admin_id))
    db.get_db().commit()
    response = make_response(jsonify({"message": "Action logged successfully"}))
    response.status_code = 201
    return response

#Update admin action records
@administrator.route('/actions/<action_id>', methods=['PUT'])
def update_action(action_id):
    data = request.get_json()
    action_type = data.get('action_type')
    query = '''
    UPDATE Actions
    SET ActionType = %s
    WHERE ActionID = %s
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (action_type, action_id))
    db.get_db().commit()
    response = make_response(jsonify({"message": "Action updated successfully"}))
    response.status_code = 200
    return response

#Delete old logs
@administrator.route('/actions/<action_id>', methods=['DELETE'])
def delete_action(action_id):
    query = '''
    DELETE FROM Actions
    WHERE ActionID = %s
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (action_id,))
    db.get_db().commit()
    response = make_response(jsonify({"message": "Action deleted successfully"}))
    response.status_code = 200
    return response

