from flask import Blueprint, jsonify
from app.models.hut import Hut  # Import your Hut model

hut_routes = Blueprint('hut_routes', __name__)

@hut_routes.route('/api/get-all-huts', methods=['GET'])
def get_huts():
    try:
        huts = Hut.query.all()  # SQLAlchemy query to get all huts
        huts_list = [{"id": hut.id, "name": hut.name} for hut in huts]  # Create a list of huts with id and name
        print(f"Retrieved huts: {huts_list}")  # Print the retrieved huts to the terminal
        return jsonify(huts_list), 200  # Return the list as JSON with a 200 status code
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Return an error message with a 500 status code
