from sqlalchemy import select

from app.db import SessionLocal
from app.models import Species
from app.services.moisture import default_range

# (common name, scientific name, watering category, sunlight)
PLANTS = [
    ("Tomato", "Solanum lycopersicum", "frequent", ["full sun"]),
    ("Basil", "Ocimum basilicum", "average", ["full sun"]),
    ("Mint", "Mentha spicata", "frequent", ["full sun", "part shade"]),
    ("Lavender", "Lavandula angustifolia", "minimum", ["full sun"]),
    ("Rosemary", "Salvia rosmarinus", "minimum", ["full sun"]),
    ("Thyme", "Thymus vulgaris", "minimum", ["full sun"]),
    ("Parsley", "Petroselinum crispum", "average", ["full sun", "part shade"]),
    ("Pepper", "Capsicum annuum", "average", ["full sun"]),
    ("Cucumber", "Cucumis sativus", "frequent", ["full sun"]),
    ("Strawberry", "Fragaria x ananassa", "frequent", ["full sun"]),
    ("Aloe vera", "Aloe vera", "minimum", ["full sun", "part shade"]),
    ("Snake plant", "Dracaena trifasciata", "minimum", ["part shade"]),
    ("Peace lily", "Spathiphyllum wallisii", "frequent", ["part shade"]),
    ("Boston fern", "Nephrolepis exaltata", "frequent", ["part shade"]),
    ("Geranium", "Pelargonium x hortorum", "average", ["full sun"]),
    ("Rose", "Rosa", "average", ["full sun"]),
    ("Jasmine", "Jasminum officinale", "average", ["full sun", "part shade"]),
    ("Olive tree", "Olea europaea", "minimum", ["full sun"]),
    ("Lemon tree", "Citrus limon", "average", ["full sun"]),
    ("Fig tree", "Ficus carica", "average", ["full sun"]),
]


def run() -> None:
    added = 0
    with SessionLocal() as db:
        for common, scientific, category, sunlight in PLANTS:
            exists = db.scalar(select(Species).where(Species.common_name == common))
            if exists:
                continue
            low, high = default_range(category)
            db.add(
                Species(
                    common_name=common,
                    scientific_name=scientific,
                    watering_category=category,
                    sunlight=sunlight,
                    moisture_min_pct=low,
                    moisture_max_pct=high,
                    moisture_source="default_mapping",
                )
            )
            added += 1
        db.commit()
    print(f"Added {added} species")


if __name__ == "__main__":
    run()