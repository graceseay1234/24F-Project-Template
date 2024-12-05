from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

feedback = Blueprint('feedback', __name__)


# Get all the feedback from the database
@feedback.route('/feedback', methods=['GET'])
def get_feedback():
    query = '''
Select Feedback.Content, Feedback.TimeStamp
From Feedback
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

# get a single feedback by its id 
@feedback.route('/feedback/<id>', methods=['GET'])
def get_feedbackid (id):

    query = f'''SELECT *
                FROM feedback
                WHERE feedbackID = {str(id)}
    '''
    current_app.logger.info(f'GET /feedback/<id> query={query}')

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    current_app.logger.info(f'GET /feedback/<id> Result of query = {theData}')

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

# ------------------------------------------------------------
# view profiles of feedback that include their education, work history, and career journey

@feedback.route('/jobs')
def get_feedback_details():

    query = '''
Select feedback.Name, feedback.Major, feedback.GradYear, WorkExperience.Company,
       WorkExperience.Role, WorkExperience.Startdate, WorkExperience.EndDate,
       WorkExperience.IsCurrent
From feedback 
JOIN WorkExperience ON feedback.feedbackID = WorkExperience.feedbackID;
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
@feedback.route('/tenMostExpensive', methods=['GET'])
def get_10_most_expensive_feedback():

    query = '''
        SELECT feedback_code,
               feedback_name,
               list_price,
               reorder_level
        FROM feedback
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
# This is a POST route to add a new feedback.
# Remember, we are using POST routes to create new entries
# in the database.
@feedback.route('/feedback', methods=['POST'])
def add_new_feedback():

    # In a POST request, there is a
    # collecting data from the request object
    the_data = request.json
    current_app.logger.info(the_data)

    # Generating a new FeedbackID
    cursor = db.get_db().cursor()
    cursor.execute("SELECT COUNT(FeedbackID) FROM Feedback")
    row = cursor.fetchone()

    new_feedback_id = row.get('COUNT(FeedbackID)', 0)

    content = the_data.get('content', '')

    query = f'''
        INSERT INTO Feedback (FeedbackID, Content)
        VALUES ('{new_feedback_id + 1}', '{content}')
    '''

    current_app.logger.info(query)

    # executing and committing the insert statement
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response("Successfully added feedback")
    response.status_code = 200
    #The return statement below returns the response to the streamlit application.
    return response

# ------------------------------------------------------------
### Get all feedback categories
@feedback.route('/categories', methods = ['GET'])
def get_all_categories():
    query = '''
        SELECT DISTINCT category AS label, category as value
        FROM feedback
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
# This is a stubbed route to update a feedback in the catalog
# The SQL query would be an UPDATE.
@feedback.route('/feedback', methods = ['PUT'])
def update_feedback():
    feedback_info = request.json
    current_app.logger.info(feedback_info)

    return "Success"



@feedback.route('/delete_feedback/<feedback_id>', methods=['DELETE'])
def delete_feedback(feedback_id):
    query = f"DELETE FROM feedback WHERE feedbackID = {feedback_id}"
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    return jsonify({"message": f"feedback ID {feedback_id} deleted successfully."}), 200



@feedback.route('/feedback_with_warnings', methods=['GET'])
def get_feedback_with_warnings():
    query = '''
    SELECT A.feedbackID, A.Name, A.Major, A.GradYear, 
           W.WarningID, W.Reason AS WarningReason, W.TimeStamp AS WarningTime,
           WE.Role AS WorkExperience, WE.Company
    FROM feedback A
    LEFT JOIN Warnings W ON A.feedbackID = W.feedbackID
    LEFT JOIN WorkExperience WE ON A.feedbackID = WE.feedbackID
    WHERE W.WarningID IS NOT NULL;
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response




@feedback.route('/feedback_without_warnings', methods=['GET'])
def get_feedback_without_warnings():
    query = '''
    SELECT a.feedbackID, a.Name, a.Major, a.WorkExperience, a.GradYear
    FROM feedback a
    LEFT JOIN Warnings w ON a.feedbackID = w.feedbackID
    WHERE w.WarningID IS NULL;
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response


