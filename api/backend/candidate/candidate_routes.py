from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

candidate = Blueprint('candidate', __name__)


# Get all the candidate from the database
@candidate.route('/candidate', methods=['GET'])
def get_candidate():
    query = '''
Select candidate.Name, candidate.Major, WorkExperience.Role, WorkExperience.Company
From candidate
JOIN WorkExperience ON candidate.candidateID = WorkExperience.candidateID
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

# get a single candidate by its id 
@candidate.route('/candidate/<id>', methods=['GET'])
def get_candidateid (id):

    query = f'''SELECT *
                FROM candidate
                WHERE candidateID = {str(id)}
    '''
    current_app.logger.info(f'GET /candidate/<id> query={query}')

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    current_app.logger.info(f'GET /candidate/<id> Result of query = {theData}')

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

# ------------------------------------------------------------
# view profiles of candidate that include their education, work history, and career journey

@candidate.route('/jobs')
def get_candidate_details():

    query = '''
Select candidate.Name, candidate.Major, candidate.GradYear, WorkExperience.Company,
       WorkExperience.Role, WorkExperience.Startdate, WorkExperience.EndDate,
       WorkExperience.IsCurrent
From candidate 
JOIN WorkExperience ON candidate.candidateID = WorkExperience.candidateID;
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
@candidate.route('/tenMostExpensive', methods=['GET'])
def get_10_most_expensive_candidate():

    query = '''
        SELECT candidate_code,
               candidate_name,
               list_price,
               reorder_level
        FROM candidate
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
# This is a POST route to add a new candidate.
# Remember, we are using POST routes to create new entries
# in the database.
@candidate.route('/candidate', methods=['POST'])
def add_new_candidate():

    # In a POST request, there is a
    # collecting data from the request object
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    name = the_data['candidate_name']
    description = the_data['candidate_description']
    price = the_data['candidate_price']
    category = the_data['candidate_category']

    query = f'''
        INSERT INTO candidate (candidate_name,
                              description,
                              category,
                              list_price)
        VALUES ('{name}', '{description}', '{category}', {str(price)})
    '''
    # TODO: Make sure the version of the query above works properly
    # Constructing the query
    # query = 'insert into candidate (candidate_name, description, category, list_price) values ("'
    # query += name + '", "'
    # query += description + '", "'
    # query += category + '", '
    # query += str(price) + ')'
    current_app.logger.info(query)

    # executing and committing the insert statement
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response("Successfully added candidate")
    response.status_code = 200
    #The return statement below returns the response to the streamlit application.
    return response

# ------------------------------------------------------------
### Get all candidate categories
@candidate.route('/categories', methods = ['GET'])
def get_all_categories():
    query = '''
        SELECT DISTINCT category AS label, category as value
        FROM candidate
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
# This is a stubbed route to update a candidate in the catalog
# The SQL query would be an UPDATE.
@candidate.route('/candidate', methods = ['PUT'])
def update_candidate():
    candidate_info = request.json
    current_app.logger.info(candidate_info)

    return "Success"



@candidate.route('/delete_candidate/<candidate_id>', methods=['DELETE'])
def delete_candidate(candidate_id):
    query = f"DELETE FROM candidate WHERE candidateID = {candidate_id}"
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    return jsonify({"message": f"candidate ID {candidate_id} deleted successfully."}), 200



@candidate.route('/candidate_with_warnings', methods=['GET'])
def get_candidate_with_warnings():
    query = '''
    SELECT A.candidateID, A.Name, A.Major, A.GradYear, 
           W.WarningID, W.Reason AS WarningReason, W.TimeStamp AS WarningTime,
           WE.Role AS WorkExperience, WE.Company
    FROM candidate A
    LEFT JOIN Warnings W ON A.candidateID = W.candidateID
    LEFT JOIN WorkExperience WE ON A.candidateID = WE.candidateID
    WHERE W.WarningID IS NOT NULL;
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response




@candidate.route('/candidate_without_warnings', methods=['GET'])
def get_candidate_without_warnings():
    query = '''
    SELECT a.candidateID, a.Name, a.Major, a.WorkExperience, a.GradYear
    FROM candidate a
    LEFT JOIN Warnings w ON a.candidateID = w.candidateID
    WHERE w.WarningID IS NULL;
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response


