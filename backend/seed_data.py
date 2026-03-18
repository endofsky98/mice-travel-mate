"""
MICE Travel Mate - Seed Data Script
Run: python seed_data.py
Inserts sample data into the database (restaurants, courses, products, guides, etc.)
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
    """Seed 30 restaurants."""
    from seed.restaurants import get_restaurants
    data = get_restaurants()
    for item in data:
        r = Restaurant(**item)
        session.add(r)
    await session.commit()
    logger.info(f"  Seeded {len(data)} restaurants")
    return data


async def seed_courses(session):
    """Seed 30 courses with spots and transitions."""
    from seed.courses import get_courses
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

    logger.info(f"  Seeded {len(courses)} courses, {len(spots)} spots, {len(transitions)} transitions")
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
    """Seed 30 guides."""
    from seed.guides import get_guides
    data = get_guides()
    for item in data:
        session.add(Guide(**item))
    await session.commit()
    logger.info(f"  Seeded {len(data)} guides")
    return data


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
    """Seed 12 festivals."""
    from seed.supplementary import get_festivals
    data = get_festivals()
    for item in data:
        session.add(Festival(**item))
    await session.commit()
    logger.info(f"  Seeded {len(data)} festivals")


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
    logger.info("MICE Travel Mate - Seeding Database")
    logger.info("=" * 60)

    # Create tables if they don't exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        # Clear existing data
        logger.info("\n[1/10] Clearing existing data...")
        await clear_existing_data(session)

        # Seed in order
        logger.info("\n[2/10] Seeding restaurants...")
        await seed_restaurants(session)

        logger.info("\n[3/10] Seeding courses...")
        await seed_courses(session)

        logger.info("\n[4/10] Seeding products...")
        await seed_products(session)

        logger.info("\n[5/10] Seeding guides...")
        await seed_guides(session)

        logger.info("\n[6/10] Seeding banners...")
        await seed_banners(session)

        logger.info("\n[7/10] Seeding events...")
        await seed_events(session)

        logger.info("\n[8/10] Seeding festivals...")
        await seed_festivals(session)

        logger.info("\n[9/10] Seeding transport...")
        await seed_transport(session)

        logger.info("\n[10/10] Seeding themes & living guide...")
        await seed_themes(session)
        await seed_living_guide(session)

    logger.info("\n" + "=" * 60)
    logger.info("Seeding complete!")
    logger.info("=" * 60)


if __name__ == "__main__":
    asyncio.run(run_seed())
