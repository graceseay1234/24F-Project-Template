from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

candidate = Blueprint('Candidate', __name__)

# Get all candidates from the database
@candidate.route('/candidate', methods=['GET'])
def get_candidates():
    query = '''
    SELECT CandidateID, Name, InterviewNotes, Status, Qualities
    FROM Candidate
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

# Get a single candidate by its ID
@candidate.route('/candidate/<id>', methods=['GET'])
def get_candidate_by_id(id):
    query = f'''
    SELECT CandidateID, Name, InterviewNotes, Status, Qualities
    FROM Candidate
    WHERE CandidateID = {str(id)}
    '''
    current_app.logger.info(f'GET /candidate/<id> query={query}')

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    current_app.logger.info(f'GET /candidate/<id> Result of query = {theData}')

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

# Route to add a new candidate
@candidate.route('/candidate', methods=['POST'])
def add_new_candidate():
    the_data = request.json
    current_app.logger.info(the_data)

    # Extracting the variables
    candidate_id = the_data['CandidateID']
    name = the_data['Name']
    interview_notes = the_data.get('InterviewNotes', '')
    status = the_data.get('Status', '')
    qualities = the_data.get('Qualities', '')

    query = f'''
    INSERT INTO Candidate (CandidateID, Name, InterviewNotes, Status, Qualities)
    VALUES ('{candidate_id}', '{name}', '{interview_notes}', '{status}', '{qualities}')
    '''
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response("Successfully added candidate")
    response.status_code = 201
    return response

# Route to delete a candidate
@candidate.route('/delete_candidate/<candidate_id>', methods=['DELETE'])
def delete_candidate(candidate_id):
    query = f"DELETE FROM Candidate WHERE CandidateID = '{candidate_id}'"
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    return jsonify({"message": f"Candidate ID {candidate_id} deleted successfully."}), 200

# Route to update a candidate's information (stubbed for now)
@candidate.route('/candidate', methods=['PUT'])
def update_candidate():
    candidate_info = request.json
    current_app.logger.info(candidate_info)

    # Here you would include the logic for updating the candidate's information in the database.
    return jsonify({"message": "Update functionality to be implemented"}), 200

# Get candidates with warnings
@candidate.route('/candidate_with_warnings', methods=['GET'])
def get_candidate_with_warnings():
    query = '''
    SELECT A.CandidateID, A.Name, A.Status, A.Qualities, 
           W.WarningID, W.Reason AS WarningReason, W.TimeStamp AS WarningTime
    FROM Candidate A
    LEFT JOIN Warnings W ON A.CandidateID = W.CandidateID
    WHERE W.WarningID IS NOT NULL;
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

# Get candidates without warnings
@candidate.route('/candidate_without_warnings', methods=['GET'])
def get_candidate_without_warnings():
    query = '''
    SELECT A.CandidateID, A.Name, A.Status, A.Qualities
    FROM Candidate A
    LEFT JOIN Warnings W ON A.CandidateID = W.CandidateID
    WHERE W.WarningID IS NULL;
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

@candidate.route('/delete_candidate_by_name/<candidate_name>', methods=['DELETE'])
def delete_candidate_by_name(candidate_name):
    query = f"DELETE FROM Candidate WHERE Name = '{candidate_name}'"
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    return jsonify({"message": f"Candidate {candidate_name} deleted successfully."}), 200


@candidate.route('/job', methods=['GET'])
def get_jobs():
    query = '''
    SELECT JobID, Title, Description, Status
    FROM Job
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response