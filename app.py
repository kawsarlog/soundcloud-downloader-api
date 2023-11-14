from soundcloudDownloaderAPI import get_response
from flask import Flask, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)


def is_valid_soundcloud_url(url):
    # Regular expression for validating SoundCloud URLs
    pattern = r'^https?://soundcloud\.com/[\w-]+/[\w-]+$'
    return re.match(pattern, url)


@app.route('/getTrackInfo', methods=['GET'])
def get_track_info():
    try:
        track_link = request.args.get('url')
        if not track_link:
            return jsonify({
                'reason': 'URL parameter is missing',
                'status': False
            }), 400

        if not is_valid_soundcloud_url(track_link):
            return jsonify({
                'reason': 'Invalid SoundCloud URL format',
                'status': False

            }), 400

        output_data = get_response(track_link)
        return jsonify(output_data)
    except Exception as e:
        # return jsonify({'error': str(e)}), 500
        return jsonify({
            'status': False,
            'reason': 'Server Error'
        }), 500


# RapidAPI requires a health check endpoint
@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    app.run(debug=False)
