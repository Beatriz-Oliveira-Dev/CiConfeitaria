import os
from datetime import datetime
from typing import List

from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "recipes.db")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DATABASE_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "dev-secret-key"

db = SQLAlchemy(app)


class Recipe(db.Model):
    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "ingredients": self.ingredients,
            "instructions": self.instructions,
            "image_url": self.image_url,
            "created_at": self.created_at.isoformat(),
        }


with app.app_context():
    db.create_all()


def parse_multiline_field(value: str) -> str:
    return "\n".join([line.strip() for line in value.splitlines() if line.strip()])


@app.route("/")
def index():
    recipes: List[Recipe] = Recipe.query.order_by(Recipe.created_at.desc()).all()
    return render_template("index.html", recipes=recipes)


@app.route("/cadastrar")
def form_page():
    recipe_id = request.args.get("recipe_id", type=int)
    recipe = Recipe.query.get_or_404(recipe_id) if recipe_id else None
    return render_template("create.html", recipe=recipe)


@app.route("/recipes", methods=["POST"])
def create_recipe():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    ingredients = parse_multiline_field(request.form.get("ingredients", ""))
    instructions = parse_multiline_field(request.form.get("instructions", ""))
    image_url = request.form.get("image_url", "").strip() or None

    if not all([title, description, ingredients, instructions]):
        error = "Todos os campos obrigatórios devem ser preenchidos."
        return render_template("create.html", recipe=None, error=error), 400

    recipe = Recipe(
        title=title,
        description=description,
        ingredients=ingredients,
        instructions=instructions,
        image_url=image_url,
    )
    db.session.add(recipe)
    db.session.commit()

    return redirect(url_for("index"))


@app.route("/recipes/<int:recipe_id>/update", methods=["POST"])
def update_recipe(recipe_id: int):
    recipe = Recipe.query.get_or_404(recipe_id)

    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    ingredients = parse_multiline_field(request.form.get("ingredients", ""))
    instructions = parse_multiline_field(request.form.get("instructions", ""))
    image_url = request.form.get("image_url", "").strip() or None

    if not all([title, description, ingredients, instructions]):
        error = "Todos os campos obrigatórios devem ser preenchidos."
        return render_template("create.html", recipe=recipe, error=error), 400

    recipe.title = title
    recipe.description = description
    recipe.ingredients = ingredients
    recipe.instructions = instructions
    recipe.image_url = image_url
    db.session.commit()

    return redirect(url_for("index"))


@app.route("/recipes/<int:recipe_id>/delete", methods=["POST"])
def delete_recipe(recipe_id: int):
    recipe = Recipe.query.get_or_404(recipe_id)
    db.session.delete(recipe)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/api/recipes", methods=["GET"])
def list_recipes():
    recipes = Recipe.query.order_by(Recipe.created_at.desc()).all()
    return jsonify([recipe.to_dict() for recipe in recipes])


@app.route("/api/recipes", methods=["POST"])
def api_create_recipe():
    data = request.get_json() or {}
    title = data.get("title", "").strip()
    description = data.get("description", "").strip()
    ingredients = parse_multiline_field(data.get("ingredients", ""))
    instructions = parse_multiline_field(data.get("instructions", ""))
    image_url = data.get("image_url", "").strip() or None

    if not all([title, description, ingredients, instructions]):
        return jsonify({"error": "Campos obrigatórios faltando."}), 400

    recipe = Recipe(
        title=title,
        description=description,
        ingredients=ingredients,
        instructions=instructions,
        image_url=image_url,
    )
    db.session.add(recipe)
    db.session.commit()

    return jsonify(recipe.to_dict()), 201


@app.route("/api/recipes/<int:recipe_id>", methods=["PUT", "PATCH"])
def api_update_recipe(recipe_id: int):
    recipe = Recipe.query.get_or_404(recipe_id)
    data = request.get_json() or {}

    title = data.get("title", recipe.title).strip()
    description = data.get("description", recipe.description).strip()
    ingredients = parse_multiline_field(data.get("ingredients", recipe.ingredients))
    instructions = parse_multiline_field(
        data.get("instructions", recipe.instructions)
    )
    image_url = (data.get("image_url", recipe.image_url) or "").strip() or None

    if not all([title, description, ingredients, instructions]):
        return jsonify({"error": "Campos obrigatórios faltando."}), 400

    recipe.title = title
    recipe.description = description
    recipe.ingredients = ingredients
    recipe.instructions = instructions
    recipe.image_url = image_url
    db.session.commit()

    return jsonify(recipe.to_dict())


@app.route("/api/recipes/<int:recipe_id>", methods=["DELETE"])
def api_delete_recipe(recipe_id: int):
    recipe = Recipe.query.get_or_404(recipe_id)
    db.session.delete(recipe)
    db.session.commit()
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)
