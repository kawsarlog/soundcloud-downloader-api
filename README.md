# soundcloud-downloader-api
🎵 SoundCloud Scraper API is a simple Flask-based web service that enables you to extract information about SoundCloud tracks. Whether you're building a music-related application or simply exploring SoundCloud data, this API provides a convenient way to retrieve track details using SoundCloud URLs. The project emphasizes ease of use, integration, and educational purposes.

[![Selenium Version](https://img.shields.io/badge/Selenium-4.0.0-blue)](https://pypi.org/project/selenium/)
[![Flask-CORS Version](https://img.shields.io/badge/Flask--CORS-1.10.3-blue)](https://pypi.org/project/Flask-Cors/)
[![Flask Version](https://img.shields.io/badge/Flask-3.0.0-blue)](https://pypi.org/project/Flask/)

## Introduction

This Flask-based API allows you to retrieve information from SoundCloud by providing a SoundCloud track link. It is designed to be hosted on a server and can be easily integrated into other applications or services.

### Video

[![Click to watch demo video](https://img.youtube.com/vi/dyQ6Tlna2nI/0.jpg)](https://www.youtube.com/watch?v=dyQ6Tlna2nI)

## Features

- **Get Track Info:** Retrieve information about a SoundCloud track by providing its URL.

## Getting Started

### Prerequisites

- Python 3.x
- Flask
- Flask-CORS
- Selenium

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/kawsarlog/soundcloud-downloader-api.git
   ```

2. Install dependencies:

   ```bash
   cd soundcloud-downloader-api
   pip install -r requirements.txt
   ```
### Usage

1. Run the Flask app:

   ```bash
   python app.py
   ```

   The app will run on `http://127.0.0.1:5000/` by default.

2. Make a GET request to the following endpoint to retrieve track information:

   ```bash
   http://127.0.0.1:5000/getTrackInfo?url=https://soundcloud.com/user/track-link
   ```

   Replace `https://soundcloud.com/user/track-link` with the desired SoundCloud track URL.

3. You will receive a JSON response with the track information.

### API Endpoints

- **GET `/getTrackInfo`**
  - Parameters:
    - `url` (string): SoundCloud track URL (e.g., `https://soundcloud.com/user/track-link`).
  - Returns:
    - JSON object containing track information.

- **GET `/health`**
  - Returns:
    - JSON object with the status of the API.

## Configuration

- The Flask app is configured to run in production mode with debugging turned off. Adjust configurations in `app.py` if needed.

## License

This project is licensed under the [MIT License](LICENSE).

**Note:**
This project is for educational purposes only.
