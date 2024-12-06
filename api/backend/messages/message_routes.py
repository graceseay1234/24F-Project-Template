from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

message = Blueprint('Message', __name__)

# Get all messages from the database
@message.route('/message', methods=['GET'])
def get_messages():
    query = '''
    SELECT MessageID, MessageContent, SenderAlumniID, ReceiverAlumniID
    FROM Messages
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
    message_id = the_data.get('MessageID', '')
    content = the_data.get('Content', '')
    sender_alumni_id = the_data.get('SenderAlumniID', '')
    receiver_alumni_id = the_data.get('ReceiverAlumniID', '')

    query = f'''
    INSERT INTO Messages (MessageID, MessageContent, SenderAlumniID, ReceiverAlumniID)
    VALUES ('{message_id}', '{content}', '{sender_alumni_id}', '{receiver_alumni_id}')
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
    query = f"DELETE FROM Messages WHERE MessageID = '{message_id}'"
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    return jsonify({"message": f"message ID {message_id} deleted successfully."}), 200

# Route to update a message's information (stubbed for now)
@message.route('/message', methods=['PUT'])
def update_message():
    message_info = request.json
    current_app.logger.info(message_info)

    # Extracting variables
    message_id = feedback_info.get('MessageID')
    content = feedback_info.get('Content')

    query = '''
        UPDATE Messages
        SET MessageContent = %s
        WHERE MessageID = %s
    '''

    # Executing the SQL query
    try:
        cursor = db.get_db().cursor()
        cursor.execute(query, (content, message_id))
        db.get_db().commit()
    except Exception as e:
        current_app.logger.error(f"Failed to update message: {e}")
        response = make_response("Failed to update message")
        response.status_code = 500
        return response

    response = make_response("Successfully updated message")
    response.status_code = 200
    return response