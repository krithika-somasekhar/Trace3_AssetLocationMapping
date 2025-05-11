import cv2
from flask import Blueprint, request, jsonify, current_app, url_for, send_from_directory, g
from werkzeug.utils import secure_filename
import os
import uuid
from .utils import process_floor_plan_image
from .db import get_db_connection, close_db_connection

main = Blueprint('main', __name__)

@main.teardown_app_request
def teardown_db(exception):
    close_db_connection(exception)


@main.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

def save_map_data(connection, map_building, map_floor, map_url):
    with connection.cursor() as cursor:
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS map (
            map_id INT AUTO_INCREMENT PRIMARY KEY,
            map_building VARCHAR(255) NOT NULL,
            map_floor INT NOT NULL,
            map_url VARCHAR(500) NOT NULL
        )
        """
        cursor.execute(create_table_sql)

        insert_sql = """
        INSERT INTO map (map_building, map_floor, map_url)
        VALUES (%s, %s, %s)
        """
        cursor.execute(insert_sql, (map_building, map_floor, map_url))

@main.route('/add_assets', methods=['POST'])
def add_or_update_asset():
    asset_id = request.form.get('asset_id', type=int)
    asset_name = request.form.get('asset_name')
    asset_type = request.form.get('asset_type')
    asset_thumb_id = request.form.get('asset_thumb_id', type=int)
    room_id = request.form.get('room_id', type=int)
    gridx = request.form.get('gridx', type=int)
    gridy = request.form.get('gridy', type=int)

    if not asset_name:
        return jsonify({'error': 'Field "asset_name" is mandatory'}), 400
    if not asset_type:
        return jsonify({'error': 'Field "asset_type" is mandatory'}), 400

    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            if asset_id:
                update_sql = """
                UPDATE Asset
                SET asset_name = %s, asset_type = %s, asset_thumb_id = %s, room_id = %s, gridx = %s, gridy = %s
                WHERE asset_id = %s
                """
                cursor.execute(update_sql, (asset_name, asset_type, asset_thumb_id, room_id, gridx, gridy, asset_id))
                message = 'Asset updated successfully'
            else:
                insert_sql = """
                INSERT INTO Asset (asset_name, asset_type, asset_thumb_id, room_id, gridx, gridy)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_sql, (asset_name, asset_type, asset_thumb_id, room_id, gridx, gridy))
                message = 'Asset added successfully'

        connection.commit()
        return jsonify({'message': message}), 200
    except Exception as e:
        current_app.logger.error(f"An error occurred: {str(e)}")
        return jsonify({'error': 'An error occurred while adding/updating the asset'}), 500
    finally:
        if connection:
            connection.close()


@main.route('/add_room', methods=['POST'])
def add_or_update_room():
    room_id = request.form.get('room_id', type=int)
    room_name = request.form.get('room_name')
    room_floor_no = request.form.get('room_floor_no', type=int)
    room_shape = request.form.get('room_shape')
    gridxx = request.form.get('gridxx')
    gridxy = request.form.get('gridxy')
    gridyx = request.form.get('gridyx')
    gridyy = request.form.get('gridyy')
    map_id = request.form.get('map_id', type=int)

    # Basic validation for required fields
    if not room_name:
        return jsonify({'error': 'Field "room_name" is mandatory'}), 400
    if room_floor_no is None:
        return jsonify({'error': 'Field "room_floor_no" is mandatory'}), 400
    if not room_shape:
        return jsonify({'error': 'Field "room_shape" is mandatory'}), 400
    if not gridxx or not gridxy or not gridyx or not gridyy:
        return jsonify({'error': 'Grid coordinates (gridxx, gridxy, gridyx, gridyy) are mandatory'}), 400

    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            if room_id:
                # Update existing room
                update_sql = """
                UPDATE Room
                SET room_name = %s, room_floor_no = %s, room_shape = %s, 
                    gridxx = %s, gridxy = %s, gridyx = %s, gridyy = %s, map_id = %s
                WHERE room_id = %s
                """
                cursor.execute(update_sql, (room_name, room_floor_no, room_shape, 
                                            gridxx, gridxy, gridyx, gridyy, map_id, room_id))
                message = 'Room updated successfully'
            else:
                # Insert new room
                insert_sql = """
                INSERT INTO Room (room_name, room_floor_no, room_shape, 
                                  gridxx, gridxy, gridyx, gridyy, map_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_sql, (room_name, room_floor_no, room_shape, 
                                            gridxx, gridxy, gridyx, gridyy, map_id))
                message = 'Room added successfully'

        connection.commit()
        return jsonify({
            'message': message,
            'room_name': room_name,
            'room_floor_no': room_floor_no,
            'room_shape': room_shape,
            'gridxx': gridxx,
            'gridxy': gridxy,
            'gridyx': gridyx,
            'gridyy': gridyy,
            'map_id': map_id
        }), 200

    except Exception as e:
        current_app.logger.error(f"An error occurred: {str(e)}")
        return jsonify({'error': 'An error occurred while adding/updating the room'}), 500

    finally:
        if connection is not None:
            connection.close()


@main.route('/add_contract', methods=['POST'])
def add_or_update_contract():
    contract_id = request.form.get('contract_id', type=int)
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    is_expired_flag = request.form.get('is_expired_flag', '').lower() in ['true', '1', 'yes']
    asset_id = request.form.get('asset_id', type=int)

    if not start_date:
        return jsonify({'error': 'Field "start_date" is mandatory'}), 400
    if not end_date:
        return jsonify({'error': 'Field "end_date" is mandatory'}), 400
    if not asset_id:
        return jsonify({'error': 'Field "asset_id" is mandatory'}), 400

    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            if contract_id:
                update_sql = """
                UPDATE Contract
                SET start_date = %s, end_date = %s, is_expired_flag = %s, asset_id = %s
                WHERE contract_id = %s
                """
                cursor.execute(update_sql, (start_date, end_date, is_expired_flag, asset_id, contract_id))
                message = 'Contract updated successfully'
            else:
                insert_sql = """
                INSERT INTO Contract (start_date, end_date, is_expired_flag, asset_id)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(insert_sql, (start_date, end_date, is_expired_flag, asset_id))
                message = 'Contract added successfully'

        connection.commit()
        return jsonify({
            'message': message,
            'start_date': start_date,
            'end_date': end_date,
            'is_expired_flag': is_expired_flag,
            'asset_id': asset_id
        }), 200

    except Exception as e:
        current_app.logger.error(f"An error occurred: {str(e)}")
        return jsonify({'error': 'An error occurred while adding/updating the contract'}), 500

    finally:
        if connection is not None:
            connection.close()

@main.route('/add_asset_thumbnail', methods=['POST'])
def add_or_update_asset_thumbnail():
    asset_thumb_id = request.form.get('asset_thumb_id', type=int)
    asset_thumb_name = request.form.get('asset_thumb_name')
    
    if not asset_thumb_name:
        return jsonify({'error': 'Field "asset_thumb_name" is mandatory'}), 400
    if 'file' not in request.files:
        return jsonify({'error': 'Field "file" is mandatory'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    filename = secure_filename(file.filename)
    if '.' not in filename:
        return jsonify({'error': 'Invalid file name'}), 400
    file_ext = filename.rsplit('.', 1)[1].lower()
    if file_ext not in current_app.config['ALLOWED_EXTENSIONS']:
        return jsonify({'error': 'Unsupported file type'}), 400

    unique_filename = f"{uuid.uuid4()}.{file_ext}"
    asset_thumb_filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)

    connection = None
    try:
        file.save(asset_thumb_filepath)
        asset_thumb_url = url_for('main.uploaded_file', filename=unique_filename, _external=True)

        connection = get_db_connection()
        with connection.cursor() as cursor:
            if asset_thumb_id:
                update_sql = """
                UPDATE AssetThumbnail
                SET asset_thumb_name = %s, asset_thumb_url = %s
                WHERE asset_thumb_id = %s
                """
                cursor.execute(update_sql, (asset_thumb_name, asset_thumb_url, asset_thumb_id))
                message = 'Asset thumbnail updated successfully'
            else:
                insert_sql = """
                INSERT INTO AssetThumbnail (asset_thumb_name, asset_thumb_url)
                VALUES (%s, %s)
                """
                cursor.execute(insert_sql, (asset_thumb_name, asset_thumb_url))
                message = 'Asset thumbnail added successfully'

        connection.commit()
        return jsonify({
            'message': message,
            'asset_thumb_name': asset_thumb_name,
            'asset_thumb_url': asset_thumb_url
        }), 200

    except Exception as e:
        current_app.logger.error(f"An error occurred: {str(e)}")
        return jsonify({'error': 'An error occurred while adding/updating the asset thumbnail'}), 500

    finally:
        if connection is not None:
            connection.close()

@main.route('/fetch_map', methods=['GET'])
def fetch_map():
    map_building = request.args.get('map_building')
    map_floor = request.args.get('map_floor', type=int)
    grid_size = request.args.get('grid_size', type=float, default=0.1)  # Default grid size in cm

    if not map_building or map_floor is None:
        return jsonify({'error': 'map_building and map_floor are required'}), 400

    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = """
                SELECT map_url FROM map
                WHERE map_building = %s AND map_floor = %s
            """
            cursor.execute(query, (map_building, map_floor))
            result = cursor.fetchone()
            if result:
                return jsonify({
                    'map_url': result['map_url'],
                    'grid_size': grid_size
                }), 200
            else:
                return jsonify({'error': 'Map not found'}), 404
    except Exception as e:
        current_app.logger.error(f"An error occurred: {str(e)}")
        return jsonify({'error': 'An error occurred while fetching the map'}), 500
    finally:
        if connection:
            connection.close()


@main.route('/fetch_assets', methods=['GET'])
def fetch_assets():
    map_building = request.args.get('map_building')
    map_floor = request.args.get('map_floor', type=int)
    asset_name = request.args.get('asset_name', '')
    asset_type = request.args.get('asset_type', '')

    query_filters = []
    params = []

    if asset_name:
        query_filters.append("a.asset_name = %s")
        params.append(asset_name)
    if asset_type:
        query_filters.append("a.asset_type = %s")
        params.append(asset_type)

    query_filter_string = " AND ".join(query_filters)
    if query_filter_string:
        query_filter_string = f" AND {query_filter_string}"

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = f"""
                SELECT 
                    a.asset_id,
                    CONCAT(LPAD(a.gridx, 2, '0'), LPAD(a.gridy, 2, '0')) AS grid_id,
                    a.gridx, 
                    a.gridy, 
                    at.asset_thumb_url, 
                    a.asset_name, 
                    a.asset_type, 
                    d.department_name, 
                    c.is_expired_flag
                FROM Asset a
                LEFT JOIN Room r ON a.room_id = r.room_id
                LEFT JOIN Map m ON r.map_id = m.map_id
                LEFT JOIN Department d ON d.department_id = a.department_id
                LEFT JOIN Contract c ON a.asset_id = c.asset_id
                LEFT JOIN AssetThumbnail at ON a.asset_thumb_id = at.asset_thumb_id
                WHERE m.map_building = %s AND m.map_floor = %s
                {query_filter_string}
            """
            params = [map_building, map_floor] + params
            cursor.execute(query, params)
            assets = cursor.fetchall()
            return jsonify({'assets': assets}), 200
    except Exception as e:
        current_app.logger.error(f"Error: {e}")
        return jsonify({'error': 'Failed to fetch assets'}), 500


@main.route('/fetch_deal_summary', methods=['GET'])
def fetch_deal_summary():
    map_building = request.args.get('map_building')
    map_floor = request.args.get('map_floor', type=int)
    asset_name = request.args.get('asset_name', '')
    asset_type = request.args.get('asset_type', '')

    query_filters = []
    params = []

    if asset_name:
        query_filters.append("a.asset_name = %s")
        params.append(asset_name)
    if asset_type:
        query_filters.append("a.asset_type = %s")
        params.append(asset_type)

    query_filter_string = " AND ".join(query_filters)
    if query_filter_string:
        query_filter_string = f" AND {query_filter_string}"

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = f"""
                SELECT a.asset_name, a.asset_type, at.asset_thumb_url, d.department_name, c.is_expired_flag
                FROM Asset a
                JOIN Room r ON a.room_id = r.room_id
                JOIN Map m ON r.map_id = m.map_id
                JOIN AssetThumbnail at ON a.asset_thumb_id = at.asset_thumb_id
                LEFT JOIN Department d ON d.department_id = a.department_id
                LEFT JOIN Contract c ON c.asset_id = a.asset_id
                WHERE m.map_building = %s AND m.map_floor = %s
                {query_filter_string}
            """
            params = [map_building, map_floor] + params

            # Print query and parameters for debugging
            #print(f"Executing Query: {query}")
            #print(f"Query Parameters: {params}")

            cursor.execute(query, params)

            # Fetch all results and print them
            assets = cursor.fetchall()
            print(f"Query Results: {assets}")

            return jsonify({'assets': assets}), 200
    except Exception as e:
        # Print error for debugging
        print(f"Error occurred: {e}")
        return jsonify({'error': 'Failed to fetch summary'}), 500


@main.route('/add_map', methods=['POST'])
def add_or_update_map():
    map_id = request.form.get('map_id', type=int)
    map_building = request.form.get('map_building')
    map_floor = request.form.get('map_floor', type=int)
    if 'file' not in request.files or not request.files['file']:
        return jsonify({'error': 'Field "file" is mandatory'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    filename = secure_filename(file.filename)
    if '.' not in filename:
        return jsonify({'error': 'Invalid file name'}), 400
    file_ext = filename.rsplit('.', 1)[1].lower()
    if file_ext not in current_app.config['ALLOWED_EXTENSIONS']:
        return jsonify({'error': 'Unsupported file type'}), 400

    unique_filename = f"{uuid.uuid4()}.{file_ext}"
    map_filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(map_filepath)

    map_url = url_for('main.uploaded_file', filename=unique_filename, _external=True)

    if not map_building or map_floor is None:
        return jsonify({'error': 'map_building and map_floor are required'}), 400

    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            if map_id:
                update_sql = """
                UPDATE map
                SET map_building = %s, map_floor = %s, map_url = %s
                WHERE map_id = %s
                """
                cursor.execute(update_sql, (map_building, map_floor, map_url, map_id))
                message = 'Map updated successfully'
            else:
                insert_sql = """
                INSERT INTO map (map_building, map_floor, map_url)
                VALUES (%s, %s, %s)
                """
                cursor.execute(insert_sql, (map_building, map_floor, map_url))
                message = 'Map added successfully'

        connection.commit()
        return jsonify({'message': message, 'map_url': map_url}), 200

    except Exception as e:
        current_app.logger.error(f"An error occurred: {str(e)}")
        return jsonify({'error': 'An error occurred while adding/updating the map'}), 500
    finally:
        if connection:
            connection.close()

@main.route('/fetch_departments', methods=['GET'])
def fetch_departments():
    map_building = request.args.get('map_building')
    map_floor = request.args.get('map_floor', type=int)

    if not map_building or map_floor is None:
        return jsonify({'error': 'map_building and map_floor are required'}), 400

    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = """
                SELECT d.department_name, d.gridxx, d.gridxy, d.gridyx, d.gridyy
                FROM Department d
                JOIN Map m ON d.map_id = m.map_id
                WHERE m.map_building = %s AND m.map_floor = %s
            """
            cursor.execute(query, (map_building, map_floor))
            departments = cursor.fetchall()
            return jsonify({'departments': departments}), 200
    except Exception as e:
        current_app.logger.error(f"An error occurred: {str(e)}")
        return jsonify({'error': 'An error occurred while fetching departments'}), 500
    finally:
        if connection:
            connection.close()

@main.route('/fetch_asset_info', methods=['GET'])
def fetch_asset_info():
    asset_id = request.args.get('asset_id', type=int)
    if not asset_id:
        return jsonify({'error': 'Asset ID is required'}), 400

    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = """
                SELECT 
                    a.asset_name, 
                    a.asset_type, 
                    d.department_name, 
                    c.is_expired_flag
                FROM Asset a
                LEFT JOIN Room r ON a.room_id = r.room_id
                LEFT JOIN Department d ON r.map_id = d.map_id
                LEFT JOIN Contract c ON a.asset_id = c.asset_id
                WHERE a.asset_id = %s
            """
            cursor.execute(query, (asset_id,))
            asset_info = cursor.fetchone()
            if asset_info:
                return jsonify(asset_info), 200
            else:
                return jsonify({'error': 'Asset not found'}), 404
    except Exception as e:
        current_app.logger.error(f"Error fetching asset info: {str(e)}")
        return jsonify({'error': 'An error occurred while fetching asset info'}), 500
    finally:
        if connection:
            connection.close()


@main.route('/fetch_asset_filters', methods=['GET'])
def fetch_asset_filters():
    map_building = request.args.get('map_building')
    map_floor = request.args.get('map_floor', type=int)

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query_names = """
                SELECT DISTINCT a.asset_name
                FROM Asset a
                JOIN Room r ON a.room_id = r.room_id
                JOIN Map m ON r.map_id = m.map_id
                WHERE m.map_building = %s AND m.map_floor = %s
            """
            cursor.execute(query_names, (map_building, map_floor))
            asset_names = [row['asset_name'] for row in cursor.fetchall()]

            query_types = """
                SELECT DISTINCT a.asset_type
                FROM Asset a
                JOIN Room r ON a.room_id = r.room_id
                JOIN Map m ON r.map_id = m.map_id
                WHERE m.map_building = %s AND m.map_floor = %s
            """
            cursor.execute(query_types, (map_building, map_floor))
            asset_types = [row['asset_type'] for row in cursor.fetchall()]

            return jsonify({'assetNames': asset_names, 'assetTypes': asset_types}), 200
    except Exception as e:
        current_app.logger.error(f"Error: {e}")
        return jsonify({'error': 'Failed to fetch filters'}), 500