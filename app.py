from flask import Flask, request, jsonify, render_template_string
import uuid

app = Flask(__name__)

# In-memory storage for embeds (warning: resets on server restart)
embeds = {}

# HTML template for Open Graph metadata embeds
EMBED_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta property="og:title" content="{{ title }}" />
    <meta property="og:description" content="{{ description }}" />
    {% if image %}
    <meta property="og:image" content="{{ image }}" />
    {% endif %}
    <meta name="theme-color" content="{{ color }}" />
    <meta property="og:type" content="website" />
</head>
<body>
    <h1>{{ title }}</h1>
    <p>{{ description }}</p>
    {% if image %}
    <img src="{{ image }}" alt="Embed image">
    {% endif %}
</body>
</html>
"""

@app.route("/create_embed", methods=["POST"])
def create_embed():
    data = request.json
    embed_id = str(uuid.uuid4())[:8]
    embeds[embed_id] = data
    return jsonify({"embed_url": f"{request.host_url}embed/{embed_id}"}), 200

@app.route("/embed/<embed_id>")
def embed(embed_id):
    data = embeds.get(embed_id)
    if not data:
        return "Embed not found", 404

    return render_template_string(
        EMBED_TEMPLATE,
        title=data["title"],
        description=data["description"],
        image=data.get("image"),
        color=data.get("color", "#ffffff")
    )

@app.route("/")
def home():
    return "Public Discord Embed API is running 🚀"
