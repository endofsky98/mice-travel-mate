"""
Exporum Travel Mate - Seed Data Script
Run: python seed_data.py
Inserts sample data into the database (restaurants, courses, products, guides, etc.)
Now seeds 100+ items per category for restaurants, courses, guides, and festivals.
"""
import asyncio
import sys
import os
import logging

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text, select
from database import engine, Base, async_session
from models import (
    Restaurant, Course, CourseSpot, CourseSpotTransition,
    Product, Guide, RollingBanner, Event, Festival,
    TransportRoute, TransportTip,
    Theme, ThemeSpot,
    LivingGuideCategory, LivingGuideArticle,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def clear_existing_data(session):
    """Clear existing seed data to allow re-seeding."""
    tables = [
        "course_spot_transitions",
        "course_spots",
        "theme_spots",
        "living_guide_articles",
        "living_guide_categories",
        "transport_tips",
        "transport_routes",
        "themes",
        "festivals",
        "rolling_banners",
        "guides",
        "products",
        "courses",
        "restaurants",
        "events",
    ]
    for table in tables:
        try:
            await session.execute(text(f"DELETE FROM {table}"))
            logger.info(f"  Cleared table: {table}")
        except Exception as e:
            logger.warning(f"  Could not clear {table}: {e}")
    await session.commit()


async def seed_restaurants(session):
    """Seed 100 restaurants (30 base + 70 extra)."""
    from seed.restaurants import get_restaurants
    from seed.generate_extra import generate_restaurants

    base_data = get_restaurants()
    extra_data = generate_restaurants()

    for item in base_data:
        session.add(Restaurant(**item))
    await session.commit()

    for item in extra_data:
        session.add(Restaurant(**item))
    await session.commit()

    total = len(base_data) + len(extra_data)
    logger.info(f"  Seeded {total} restaurants ({len(base_data)} base + {len(extra_data)} extra)")
    return base_data


async def seed_courses(session):
    """Seed 100 courses (30 base + 70 extra) with spots and transitions."""
    from seed.courses import get_courses
    from seed.generate_extra import generate_courses

    # Base courses
    courses, spots, transitions = get_courses()
    for item in courses:
        session.add(Course(**item))
    await session.commit()
    for item in spots:
        session.add(CourseSpot(**item))
    await session.commit()
    for item in transitions:
        session.add(CourseSpotTransition(**item))
    await session.commit()

    # Extra courses
    extra_courses, extra_spots, extra_transitions = generate_courses()
    for item in extra_courses:
        session.add(Course(**item))
    await session.commit()
    for item in extra_spots:
        session.add(CourseSpot(**item))
    await session.commit()
    for item in extra_transitions:
        session.add(CourseSpotTransition(**item))
    await session.commit()

    total_courses = len(courses) + len(extra_courses)
    total_spots = len(spots) + len(extra_spots)
    logger.info(f"  Seeded {total_courses} courses, {total_spots} spots")
    return courses


async def seed_products(session):
    """Seed 30 products."""
    from seed.products import get_products
    data = get_products()
    for item in data:
        session.add(Product(**item))
    await session.commit()
    logger.info(f"  Seeded {len(data)} products")
    return data


async def seed_guides(session):
    """Seed 100 guides (30 base + 70 extra)."""
    from seed.guides import get_guides
    from seed.generate_extra import generate_guides

    base_data = get_guides()
    extra_data = generate_guides()

    for item in base_data:
        session.add(Guide(**item))
    await session.commit()

    for item in extra_data:
        session.add(Guide(**item))
    await session.commit()

    total = len(base_data) + len(extra_data)
    logger.info(f"  Seeded {total} guides ({len(base_data)} base + {len(extra_data)} extra)")
    return base_data


async def seed_banners(session):
    """Seed 5 rolling banners."""
    from seed.supplementary import get_banners
    data = get_banners()
    for item in data:
        session.add(RollingBanner(**item))
    await session.commit()
    logger.info(f"  Seeded {len(data)} banners")


async def seed_events(session):
    """Seed 3 exhibition events."""
    from seed.supplementary import get_events
    data = get_events()
    for item in data:
        session.add(Event(**item))
    await session.commit()
    logger.info(f"  Seeded {len(data)} events")


async def seed_festivals(session):
    """Seed 100 festivals (12 base + 88 extra)."""
    from seed.supplementary import get_festivals
    from seed.generate_extra import generate_festivals

    base_data = get_festivals()
    extra_data = generate_festivals()

    for item in base_data:
        session.add(Festival(**item))
    await session.commit()

    for item in extra_data:
        session.add(Festival(**item))
    await session.commit()

    total = len(base_data) + len(extra_data)
    logger.info(f"  Seeded {total} festivals ({len(base_data)} base + {len(extra_data)} extra)")


async def seed_transport(session):
    """Seed transport routes and tips."""
    from seed.supplementary import get_transport_routes, get_transport_tips
    routes = get_transport_routes()
    tips = get_transport_tips()
    for item in routes:
        session.add(TransportRoute(**item))
    await session.commit()
    for item in tips:
        session.add(TransportTip(**item))
    await session.commit()
    logger.info(f"  Seeded {len(routes)} transport routes, {len(tips)} transport tips")


async def seed_themes(session):
    """Seed 7 themes."""
    from seed.supplementary import get_themes
    data = get_themes()
    for item in data:
        session.add(Theme(**item))
    await session.commit()
    logger.info(f"  Seeded {len(data)} themes")


async def seed_living_guide(session):
    """Seed living guide categories and articles."""
    from seed.supplementary import get_living_guide_categories, get_living_guide_articles
    categories = get_living_guide_categories()
    for item in categories:
        session.add(LivingGuideCategory(**item))
    await session.commit()

    articles = get_living_guide_articles()
    for item in articles:
        session.add(LivingGuideArticle(**item))
    await session.commit()
    logger.info(f"  Seeded {len(categories)} categories, {len(articles)} articles")


async def run_seed():
    """Main seed function."""
    logger.info("=" * 60)
    logger.info("Exporum Travel Mate - Seeding Database")
    logger.info("=" * 60)

    # Create tables if they don't exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        # Clear existing data
        logger.info("\n[1/10] Clearing existing data...")
        await clear_existing_data(session)

        # Seed in order
        logger.info("\n[2/10] Seeding restaurants (100)...")
        await seed_restaurants(session)

        logger.info("\n[3/10] Seeding courses (100)...")
        await seed_courses(session)

        logger.info("\n[4/10] Seeding products...")
        await seed_products(session)

        logger.info("\n[5/10] Seeding guides (100)...")
        await seed_guides(session)

        logger.info("\n[6/10] Seeding banners...")
        await seed_banners(session)

        logger.info("\n[7/10] Seeding events...")
        await seed_events(session)

        logger.info("\n[8/10] Seeding festivals (100)...")
        await seed_festivals(session)

        logger.info("\n[9/10] Seeding transport...")
        await seed_transport(session)

        logger.info("\n[10/10] Seeding themes & living guide...")
        await seed_themes(session)
        await seed_living_guide(session)

    logger.info("\n" + "=" * 60)
    logger.info("Seeding complete! Total: 100 restaurants, 100 courses, 30 products, 100 guides, 100 festivals")
    logger.info("=" * 60)


if __name__ == "__main__":
    asyncio.run(run_seed())
