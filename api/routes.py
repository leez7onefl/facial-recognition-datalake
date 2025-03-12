from flask import Flask, request, jsonify, send_file
from utils import get_raw_data, get_staging_data, get_curated_data, check_health, get_stats
import io

app = Flask(__name__)

def setup_routes(app):

    @app.route('/raw')
    def raw():
        uuids = request.args.getlist('uuid')
        data = get_raw_data(uuids)
        if len(data) == 1:
            image = list(data.values())[0]
            if isinstance(image, str) and image.startswith('Error:'):
                return image, 400 
            img_io = io.BytesIO()
            image.save(img_io, 'JPEG')
            img_io.seek(0)
            return send_file(img_io, mimetype='image/jpeg')
        return jsonify({"error": "Multiple images not supported in raw endpoint"}), 400

    @app.route('/staging')
    def staging():
        uuids = request.args.getlist('uuid')
        data = get_staging_data(uuids)
        if len(data) == 1:
            image = list(data.values())[0]
            if isinstance(image, str) and image.startswith('Error:'):
                return image, 400
            img_io = io.BytesIO()
            image.save(img_io, 'JPEG')
            img_io.seek(0)
            return send_file(img_io, mimetype='image/jpeg')
        return jsonify({"error": "Multiple images not supported in staging endpoint"}), 400

    @app.route('/curated')
    def curated():
        uuids = request.args.getlist('uuid')
        data = get_curated_data(uuids)
        return data


    @app.route('/health')
    def health():
        status = check_health()
        return jsonify(status)

    @app.route('/stats')
    def stats():
        metrics = get_stats()
        return jsonify(metrics)

if __name__ == '__main__':
    setup_routes(app)
    app.run()