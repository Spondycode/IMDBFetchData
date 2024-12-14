import os
import requests
from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        imdb_id = request.form.get('imdb_id')
        return get_movie_data(imdb_id)
    return render_template('index.html')

def get_movie_data(imdb_id):
    # Get the API key from the environment variable
    api_key = os.getenv('OMDB_API_KEY')
    url = f'http://www.omdbapi.com/?i={imdb_id}&apikey={api_key}'
    
    response = requests.get(url)
    data = response.json()

    if data['Response'] == 'True':
        # Format the response in Markdown
        markdown_response = f"""
# {data.get("Title", "N/A")}
![Poster]({data.get("Poster", "N/A")})

**IMDb ID**: {data.get("imdbID", "N/A")}  
**Length**: {data.get("Runtime", "N/A")}  
**Genre**: {data.get("Genre", "N/A")}  
**Year**: {data.get("Year", "N/A")}  
**Cast**: {data.get("Actors", "N/A")}  
**Director**: {data.get("Director", "N/A")}  
**Plot**: {data.get("Plot", "N/A")}
        """
        return markdown_response, 200, {'Content-Type': 'text/markdown'}
    else:
        return jsonify({"error": data.get("Error", "Movie not found")}), 404

if __name__ == '__main__':
    app.run(debug=True)