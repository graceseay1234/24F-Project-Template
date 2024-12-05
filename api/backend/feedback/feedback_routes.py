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
                FROM Feedback
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
    cursor.execute("SELECT IFNULL(MAX(CAST(FeedbackID AS UNSIGNED)), -1) FROM Feedback")
    row = cursor.fetchone()

    new_feedback_id = row.get('IFNULL(MAX(CAST(FeedbackID AS UNSIGNED)), -1)', 0)

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
# This is a stubbed route to update a feedback in the catalog
# The SQL query would be an UPDATE.
@feedback.route('/feedback', methods = ['PUT'])
def update_feedback():
    feedback_info = request.json
    current_app.logger.info(feedback_info)

    # Extracting variables
    feedback_id = feedback_info.get('FeedbackID')
    content = feedback_info.get('Content')

    query = '''
        UPDATE Feedback
        SET Content = %s
        WHERE FeedbackID = %s
    '''

    # Executing the SQL query
    try:
        cursor = db.get_db().cursor()
        cursor.execute(query, (content, feedback_id))
        db.get_db().commit()
    except Exception as e:
        current_app.logger.error(f"Failed to update feedback: {e}")
        response = make_response("Failed to update feedback")
        response.status_code = 500
        return response

    response = make_response("Successfully updated feedback")
    response.status_code = 200
    return response



@feedback.route('/delete_feedback/<feedback_id>', methods=['DELETE'])
def delete_feedback(feedback_id):
    query = f"DELETE FROM Feedback WHERE feedbackID = {feedback_id}"
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    return jsonify({"message": f"feedback ID {feedback_id} deleted successfully."}), 200