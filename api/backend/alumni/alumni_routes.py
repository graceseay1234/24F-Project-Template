from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

alumni = Blueprint('alumni', __name__)


# Get all the alumni from the database
@alumni.route('/alumni', methods=['GET'])
def get_alumni():
    query = '''
Select Alumni.Name, Alumni.Major, WorkExperience.Role, WorkExperience.Company
From Alumni
LEFT OUTER JOIN WorkExperience ON Alumni.AlumniID = WorkExperience.AlumniID
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

# get a single alumni by its id 
@alumni.route('/alumni/<id>', methods=['GET'])
def get_alumniid (id):

    query = f'''SELECT *
                FROM Alumni
                WHERE AlumniID = {str(id)}
    '''
    current_app.logger.info(f'GET /alumni/<id> query={query}')

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    current_app.logger.info(f'GET /alumni/<id> Result of query = {theData}')

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

# ------------------------------------------------------------
# view profiles of alumni that include their education, work history, and career journey

@alumni.route('/jobs')
def get_alumni_details():

    query = '''
Select Alumni.Name, Alumni.Major, Alumni.GradYear, WorkExperience.Company,
       WorkExperience.Role, WorkExperience.Startdate, WorkExperience.EndDate,
       WorkExperience.IsCurrent
From Alumni 
JOIN WorkExperience ON Alumni.AlumniID = WorkExperience.AlumniID;
    '''
    # Same process as handler above
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

# ------------------------------------------------------------
# Route to get the 10 most expensive items from the
# database.
@alumni.route('/tenMostExpensive', methods=['GET'])
def get_10_most_expensive_alumni():

    query = '''
        SELECT alumni_code,
               alumni_name,
               list_price,
               reorder_level
        FROM alumni
        ORDER BY list_price DESC
        LIMIT 10
    '''

    # Same process as above
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response


# ------------------------------------------------------------
# This is a POST route to add a new alumni.
# Remember, we are using POST routes to create new entries
# in the database.
@alumni.route('/alumni', methods=['POST'])
def add_new_alumni():

    # In a POST request, there is a
    # collecting data from the request object
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    name = the_data['Name']
    major = the_data['Major']
    grad_year = the_data['GradYear']
    work_experience = the_data['WorkExperience']
    company = the_data['Company']
    #warning_reason = the_data["WarningReason"]


    query1 = f'''
        INSERT INTO Alumni (Name,
                              Major,
                              GradYear,
                              WorkExperience
                              )
        VALUES ('{name}', '{major}', '{grad_year}', '{work_experience}')
    '''
    query2 = '''
        SET @last_id = LAST_INSERT_ID()
    '''
    query3 = f'''
        INSERT INTO WorkExperience (Company, AlumniID)
        VALUES ('{company}', @last_id)
    '''
    current_app.logger.info(query1)
    current_app.logger.info(query2)
    current_app.logger.info(query3)

    # executing and committing the insert statement
    cursor = db.get_db().cursor()
    cursor.execute(query1)
    cursor.execute(query2)
    cursor.execute(query3)
    db.get_db().commit()

    response = make_response("Successfully added alumni")
    response.status_code = 200
    #The return statement below returns the response to the streamlit application.
    return response

# ------------------------------------------------------------
### Get all alumni categories
@alumni.route('/categories', methods = ['GET'])
def get_all_categories():
    query = '''
        SELECT DISTINCT category AS label, category as value
        FROM alumni
        WHERE category IS NOT NULL
        ORDER BY category
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

# ------------------------------------------------------------
# This is a stubbed route to update a alumni in the catalog
# The SQL query would be an UPDATE.
@alumni.route('/alumni', methods = ['PUT'])
def update_alumni():
    alumni_info = request.json
    current_app.logger.info(alumni_info)

    return "Success"



@alumni.route('/delete_alumni/<alumni_id>', methods=['DELETE'])
def delete_alumni(alumni_id):
    query = f"DELETE FROM Alumni WHERE AlumniID = {alumni_id}"
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    return jsonify({"message": f"Alumni ID {alumni_id} deleted successfully."}), 200



@alumni.route('/alumni_with_warnings', methods=['GET'])
def get_alumni_with_warnings():
    query = '''
    SELECT A.AlumniID, A.Name, A.Major, A.GradYear, 
           W.WarningID, W.Reason AS WarningReason, W.TimeStamp AS WarningTime,
           WE.Role AS WorkExperience, WE.Company
    FROM Alumni A
    LEFT JOIN Warnings W ON A.AlumniID = W.AlumniID
    LEFT JOIN WorkExperience WE ON A.AlumniID = WE.AlumniID
    WHERE W.WarningID IS NOT NULL;
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response




@alumni.route('/alumni_without_warnings', methods=['GET'])
def get_alumni_without_warnings():
    query = '''
    SELECT a.AlumniID, a.Name, a.Major, a.WorkExperience, a.GradYear
    FROM Alumni a
    LEFT JOIN Warnings w ON a.AlumniID = w.AlumniID
    WHERE w.WarningID IS NULL;
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response


@alumni.route('/majors', methods=['GET'])
def get_all_majors():
    query = '''
        SELECT DISTINCT Major
        FROM Alumni
        WHERE Major IS NOT NULL
        ORDER BY Major
    '''
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    majors = cursor.fetchall()

    response = make_response(jsonify(majors))
    response.status_code = 200
    return response