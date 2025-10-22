# String Analyzer - FastAPI

A RESTful API service that analyzes strings and stores their computed properties.

## Features

- Analyze string properties (e.g., length, palindrome check, word count, character frequency)
- Filter strings based on computed attributes
- Store results in a MongoDB database
- RESTful API built using **FastAPI**
- JSON-based responses with clear documentation via Swagger UI (`/docs`)

## Tech Stack

- **Backend:** FastAPI (Python)
- **Database:** MongoDB

## Set Up

1. Clone the Repository

```bash
git clone https://github.com/<your-username>/string-analyzer.git
cd string-analyzer
```

2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
```

3. Install Dependencies

```bash
pip install -r requirements.txt
```

4. Configure Environment Variables

```.env
MONGO_URL
```

5. Run the Application

```bash
fastapi dev app.py
```

6. Open your browser and visit [http://127.0.0.1:8000/docs]. You should see the Swagger UI to test the api.

## Response Example

```bash
{
  "id": "7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069",
  "value": "Hello World!",
  "properties": {
    "length": 12,
    "is_palindrome": false,
    "unique_characters": 9,
    "word_count": 2,
    "sha256_hash": "7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069",
    "character_frequency_map": {
      "h": 1,
      "e": 1,
      "l": 3,
      "o": 2,
      " ": 1,
      "w": 1,
      "r": 1,
      "d": 1,
      "!": 1
    }
  },
  "created_at": "2025-10-21T21:36:05.039681Z"
}
```

## License

This project is licensed under the [MIT License](LICENSE).

You are free to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of this software, under the conditions of the MIT License.
