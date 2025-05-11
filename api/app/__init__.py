import os
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from .config import Config
from .db import get_db_connection


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    # Register Blueprints
    from .routes import main
    app.register_blueprint(main)

    # Route to serve the main page (index.html)
    @app.route('/')
    def serve_main_page():
        return send_from_directory('frontend/main', 'index.html')

    @app.route('/frontend/main/<path:filename>')
    def serve_main_files(filename):
        return send_from_directory('frontend/main', filename)

    # Route to serve the add_asset.html page
    @app.route('/assets')
    def serve_add_asset_page():
        return send_from_directory('frontend/Asset', 'add_asset.html')

    # Route to serve static files for Asset (like styles.css and script.js)
    @app.route('/frontend/Asset/<path:filename>')
    def serve_asset_files(filename):
        return send_from_directory('frontend/Asset', filename)

    # Route to serve the add_asset_thumbnail.html page
    @app.route('/asset_thumbnail')
    def serve_add_asset_thumbnail_page():
        return send_from_directory('frontend/AssetThumbnail', 'add_asset_thumbnail.html')

    # Route to serve static files for AssetThumbnail (like styles.css and script.js)
    @app.route('/frontend/AssetThumbnail/<path:filename>')
    def serve_asset_thumbnail_files(filename):
        return send_from_directory('frontend/AssetThumbnail', filename)

    # Route to serve the add_contract.html page
    @app.route('/contract')
    def serve_add_contract_page():
        return send_from_directory('frontend/Contract', 'add_contract.html')

    # Route to serve static files for Contract (like styles.css and script.js)
    @app.route('/frontend/Contract/<path:filename>')
    def serve_contract_files(filename):
        return send_from_directory('frontend/Contract', filename)

    # Route to serve the add_room.html page
    @app.route('/room')
    def serve_add_room_page():
        return send_from_directory('frontend/Room', 'add_room.html')

    # Route to serve static files for Room (like styles.css and script.js)
    @app.route('/frontend/Room/<path:filename>')
    def serve_room_files(filename):
        return send_from_directory('frontend/Room', filename)

    # Route to serve the render_map.html page
    @app.route('/map_render')
    def serve_render_map_page():
        return send_from_directory('frontend/MapRender', 'render_map.html')

    # Route to serve static files for MapRender (like styles.css and script.js)
    @app.route('/frontend/MapRender/<path:filename>')
    def serve_map_render_files(filename):
        return send_from_directory('frontend/MapRender', filename)

    # Route to serve the add_map.html page
    @app.route('/map')
    def serve_add_map_page():
        return send_from_directory('frontend/Map', 'add_map.html')

    # Route to serve static files for Map (like styles.css and script.js)
    @app.route('/frontend/Map/<path:filename>')
    def serve_map_files(filename):
        return send_from_directory('frontend/Map', filename)

    # Test database connection route
    @app.route('/test_db')
    def test_db_connection():
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
        return jsonify(tables)

    return app

