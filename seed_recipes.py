"""Seed sample recipes with optional image downloads."""

import base64
import os
from pathlib import Path
from typing import Dict, List, Optional

from app import app, db, Recipe

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"


MACARRONS_URL = "https://guiadacozinha.com.br/wp-content/uploads/2021/08/macaron-350x230.jpg"
CHEESECAKE_DATA_URL = os.getenv("CHEESECAKE_IMAGE_DATA")
REDVELVET_DATA_URL = os.getenv("REDVELVET_IMAGE_DATA")


def save_data_url(data_url: str, filename: str) -> str:
    """Persist a data URL under the static directory and return its relative path."""
    STATIC_DIR.mkdir(parents=True, exist_ok=True)
    _, encoded = data_url.split(",", 1)
    output_path = STATIC_DIR / filename

    if not output_path.exists():
        output_path.write_bytes(base64.b64decode(encoded))

    return f"/static/{filename}"


def recipes_payload() -> List[Dict[str, Optional[str]]]:
    images = {
        "macarrons": MACARRONS_URL,
        "cheesecake": None,
        "red velvet": None,
    }

    if CHEESECAKE_DATA_URL:
        images["cheesecake"] = save_data_url(
            CHEESECAKE_DATA_URL, "cheesecake.jpg"
        )
    if REDVELVET_DATA_URL:
        images["red velvet"] = save_data_url(
            REDVELVET_DATA_URL, "red_velvet.jpg"
        )

    base_recipes: List[Dict[str, Optional[str]]] = [
        {
            "title": "Macarrons de Framboesa",
            "description": "Macarrons delicados com ganache de framboesa.",
            "ingredients": "\n".join(
                [
                    "120 g de farinha de amêndoas",
                    "200 g de açúcar de confeiteiro",
                    "100 g de claras (cerca de 3 ovos)",
                    "80 g de açúcar refinado",
                    "Corante gel rosa",
                    "150 g de chocolate branco",
                    "80 g de creme de leite",
                    "1/2 xícara de geleia de framboesa",
                ]
            ),
            "instructions": "\n".join(
                [
                    "Peneire farinha de amêndoas e açúcar de confeiteiro e reserve.",
                    "Bata as claras em neve, adicione o açúcar refinado aos poucos até formar um merengue firme.",
                    "Incorpore os secos peneirados e o corante, mexendo até atingir a textura de fita.",
                    "Modele círculos em tapete de silicone, deixe descansar por 30 minutos e asse a 150ºC por 12-14 minutos.",
                    "Derreta o chocolate branco com o creme de leite, finalize com a geleia e recheie os discos frios.",
                ]
            ),
            "image_url": images["macarrons"],
            "price": 35.0,
            "sizes": "P\nM\nG",
            "fillings": "Ganache de chocolate\nGeleia de framboesa\nCreme de baunilha",
        },
        {
            "title": "Cheesecake de Frutas Vermelhas",
            "description": "Cheesecake cremoso com calda azedinha de frutas vermelhas.",
            "ingredients": "\n".join(
                [
                    "200 g de biscoito maisena",
                    "80 g de manteiga derretida",
                    "600 g de cream cheese",
                    "1 xícara de açúcar",
                    "3 ovos",
                    "1 colher (chá) de baunilha",
                    "Suco de 1/2 limão siciliano",
                    "1 xícara de frutas vermelhas congeladas",
                    "1/2 xícara de açúcar para a calda",
                ]
            ),
            "instructions": "\n".join(
                [
                    "Triture o biscoito, misture com a manteiga e forre o fundo de uma forma de aro removível.",
                    "Bata cream cheese, açúcar, ovos, baunilha e limão até ficar liso e despeje sobre a base.",
                    "Asse em banho-maria a 160ºC por 45-55 minutos; resfrie completamente.",
                    "Leve as frutas vermelhas com açúcar ao fogo até formar calda e cubra o cheesecake frio.",
                ]
            ),
            "image_url": images["cheesecake"],
            "price": 65.0,
            "sizes": "Pequeno\nMédio\nGrande",
            "fillings": "Calda de frutas vermelhas\nDoce de leite",
        },
        {
            "title": "Bolo Red Velvet",
            "description": "Red velvet macio com cobertura de cream cheese clássico.",
            "ingredients": "\n".join(
                [
                    "2 xícaras de farinha de trigo",
                    "1 1/2 xícara de açúcar",
                    "2 ovos",
                    "1 xícara de buttermilk",
                    "1/2 xícara de óleo",
                    "2 colheres (sopa) de cacau em pó",
                    "Corante vermelho em gel",
                    "1 colher (chá) de bicarbonato",
                    "1 colher (chá) de vinagre",
                    "300 g de cream cheese",
                    "1/4 xícara de manteiga",
                    "1 xícara de açúcar de confeiteiro",
                ]
            ),
            "instructions": "\n".join(
                [
                    "Misture os ingredientes secos; em outra tigela, una buttermilk, óleo, ovos e corante.",
                    "Combine tudo até homogêneo, adicione bicarbonato e vinagre por último e asse a 180ºC por 30-35 minutos.",
                    "Bata cream cheese, manteiga e açúcar de confeiteiro até ficar aerado e cubra o bolo frio.",
                ]
            ),
            "image_url": images["red velvet"],
            "price": 80.0,
            "sizes": "Fatia\nInteiro",
            "fillings": "Cream cheese\nGanache",
        },
    ]

    return base_recipes


def seed_recipes() -> None:
    created = 0
    updated = 0

    with app.app_context():
        db.create_all()
        for payload in recipes_payload():
            existing = Recipe.query.filter_by(title=payload["title"]).first()
            if existing:
                existing.description = payload["description"]
                existing.ingredients = payload["ingredients"]
                existing.instructions = payload["instructions"]
                existing.image_url = payload["image_url"]
                updated += 1
            else:
                recipe = Recipe(**payload)
                db.session.add(recipe)
                created += 1
        db.session.commit()

    print(f"Receitas criadas: {created}; atualizadas: {updated}")


if __name__ == "__main__":
    seed_recipes()
