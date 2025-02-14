from app import create_app
from app.services.availability_processor import add_huts_and_availability_to_database
from app.routes.hut_routes import hut_routes

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        add_huts_and_availability_to_database()
    app.run(debug=True)
