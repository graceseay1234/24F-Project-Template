from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

message = Blueprint('Message', __name__)

# Get all messages from the database
@message.route('/messages', methods=['GET'])
def get_messages():
    query = '''
    SELECT messageID, Name, InterviewNotes, Status, Qualities
    FROM message
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

# Get a single message by its ID
@message.route('/message/<id>', methods=['GET'])
def get_message_by_id(id):
    query = f'''
    SELECT messageID, Name, InterviewNotes, Status, Qualities
    FROM message
    WHERE messageID = {str(id)}
    '''
    current_app.logger.info(f'GET /message/<id> query={query}')

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    current_app.logger.info(f'GET /message/<id> Result of query = {theData}')

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

# Route to add a new message
@message.route('/message', methods=['POST'])
def add_new_message():
    the_data = request.json
    current_app.logger.info(the_data)

    # Extracting the variables
    message_id = the_data['messageID']
    name = the_data['Name']
    interview_notes = the_data.get('InterviewNotes', '')
    status = the_data.get('Status', '')
    qualities = the_data.get('Qualities', '')

    query = f'''
    INSERT INTO message (messageID, Name, InterviewNotes, Status, Qualities)
    VALUES ('{message_id}', '{name}', '{interview_notes}', '{status}', '{qualities}')
    '''
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response("Successfully added message")
    response.status_code = 201
    return response

# Route to delete a message
@message.route('/delete_message/<message_id>', methods=['DELETE'])
def delete_message(message_id):
    query = f"DELETE FROM message WHERE messageID = '{message_id}'"
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    return jsonify({"message": f"message ID {message_id} deleted successfully."}), 200

# Route to update a message's information (stubbed for now)
@message.route('/message', methods=['PUT'])
def update_message():
    message_info = request.json
    current_app.logger.info(message_info)

    # Here you would include the logic for updating the message's information in the database.
    return jsonify({"message": "Update functionality to be implemented"}), 200