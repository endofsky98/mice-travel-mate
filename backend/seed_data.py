"""
Exporoute - Seed Data Script
Run: python seed_data.py
Inserts sample data into the database with duplicate prevention.
Seeds 100 items each for restaurants, courses, guides, and festivals.
Existing data is preserved - duplicates are skipped by name_en.
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


async def get_existing_names(session, model, name_col="name_en"):
    """Get set of existing name_en values for duplicate checking."""
    col = getattr(model, name_col)
    result = await session.execute(select(col))
    return {row[0] for row in result.fetchall()}


async def seed_restaurants(session):
    """Seed restaurants with duplicate prevention."""
    from seed.restaurants import get_restaurants
    data = get_restaurants()
    existing = await get_existing_names(session, Restaurant)
    added = 0
    for item in data:
        if item["name_en"] not in existing:
            session.add(Restaurant(**item))
            existing.add(item["name_en"])
            added += 1
    await session.commit()
    logger.info(f"  Restaurants: {added} added, {len(data) - added} skipped (duplicate)")


async def seed_courses(session):
    """Seed courses with spots and transitions, with duplicate prevention."""
    from seed.courses import get_courses
    courses, spots, transitions = get_courses()
    existing = await get_existing_names(session, Course)
    added_courses = 0
    added_course_ids = set()

    for item in courses:
        if item["name_en"] not in existing:
            session.add(Course(**item))
            existing.add(item["name_en"])
            added_course_ids.add(item["id"])
            added_courses += 1
    await session.commit()

    added_spots = 0
    for item in spots:
        if item["course_id"] in added_course_ids:
            session.add(CourseSpot(**item))
            added_spots += 1
    await session.commit()

    added_trans = 0
    for item in transitions:
        if item["course_id"] in added_course_ids:
            session.add(CourseSpotTransition(**item))
            added_trans += 1
    await session.commit()

    logger.info(f"  Courses: {added_courses} added, {len(courses) - added_courses} skipped")
    logger.info(f"  Spots: {added_spots} added, Transitions: {added_trans} added")


async def seed_products(session):
    """Seed products with duplicate prevention."""
    from seed.products import get_products
    data = get_products()
    existing = await get_existing_names(session, Product)
    added = 0
    for item in data:
        if item["name_en"] not in existing:
            session.add(Product(**item))
            existing.add(item["name_en"])
            added += 1
    await session.commit()
    logger.info(f"  Products: {added} added, {len(data) - added} skipped (duplicate)")


async def seed_guides(session):
    """Seed guides with duplicate prevention."""
    from seed.guides import get_guides
    data = get_guides()
    existing = await get_existing_names(session, Guide)
    added = 0
    for item in data:
        if item["name_en"] not in existing:
            session.add(Guide(**item))
            existing.add(item["name_en"])
            added += 1
    await session.commit()
    logger.info(f"  Guides: {added} added, {len(data) - added} skipped (duplicate)")


async def seed_banners(session):
    """Seed rolling banners with duplicate prevention."""
    from seed.supplementary import get_banners
    data = get_banners()
    existing = await get_existing_names(session, RollingBanner, "title_en")
    added = 0
    for item in data:
        if item["title_en"] not in existing:
            session.add(RollingBanner(**item))
            existing.add(item["title_en"])
            added += 1
    await session.commit()
    logger.info(f"  Banners: {added} added, {len(data) - added} skipped (duplicate)")


async def seed_events(session):
    """Seed events with duplicate prevention."""
    from seed.supplementary import get_events
    data = get_events()
    existing = await get_existing_names(session, Event)
    added = 0
    for item in data:
        if item["name_en"] not in existing:
            session.add(Event(**item))
            existing.add(item["name_en"])
            added += 1
    await session.commit()
    logger.info(f"  Events: {added} added, {len(data) - added} skipped (duplicate)")


async def seed_festivals(session):
    """Seed festivals with duplicate prevention."""
    from seed.supplementary import get_festivals
    data = get_festivals()
    existing = await get_existing_names(session, Festival)
    added = 0
    for item in data:
        if item["name_en"] not in existing:
            session.add(Festival(**item))
            existing.add(item["name_en"])
            added += 1
    await session.commit()
    logger.info(f"  Festivals: {added} added, {len(data) - added} skipped (duplicate)")


async def seed_transport(session):
    """Seed transport routes and tips with duplicate prevention."""
    from seed.supplementary import get_transport_routes, get_transport_tips
    routes = get_transport_routes()
    tips = get_transport_tips()

    existing_routes = await get_existing_names(session, TransportRoute, "from_name_en")
    added_routes = 0
    for item in routes:
        if item["from_name_en"] not in existing_routes:
            session.add(TransportRoute(**item))
            existing_routes.add(item["from_name_en"])
            added_routes += 1
    await session.commit()

    existing_tips = await get_existing_names(session, TransportTip, "title_en")
    added_tips = 0
    for item in tips:
        if item["title_en"] not in existing_tips:
            session.add(TransportTip(**item))
            existing_tips.add(item["title_en"])
            added_tips += 1
    await session.commit()
    logger.info(f"  Transport: {added_routes} routes added, {added_tips} tips added")


async def seed_themes(session):
    """Seed themes with duplicate prevention."""
    from seed.supplementary import get_themes
    data = get_themes()
    existing = await get_existing_names(session, Theme)
    added = 0
    for item in data:
        if item["name_en"] not in existing:
            session.add(Theme(**item))
            existing.add(item["name_en"])
            added += 1
    await session.commit()
    logger.info(f"  Themes: {added} added, {len(data) - added} skipped (duplicate)")


async def seed_living_guide(session):
    """Seed living guide categories and articles with duplicate prevention."""
    from seed.supplementary import get_living_guide_categories, get_living_guide_articles
    categories = get_living_guide_categories()
    existing_cats = await get_existing_names(session, LivingGuideCategory)
    added_cats = 0
    for item in categories:
        if item["name_en"] not in existing_cats:
            session.add(LivingGuideCategory(**item))
            existing_cats.add(item["name_en"])
            added_cats += 1
    await session.commit()

    articles = get_living_guide_articles()
    existing_arts = await get_existing_names(session, LivingGuideArticle, "title_en")
    added_arts = 0
    for item in articles:
        if item["title_en"] not in existing_arts:
            session.add(LivingGuideArticle(**item))
            existing_arts.add(item["title_en"])
            added_arts += 1
    await session.commit()
    logger.info(f"  Living Guide: {added_cats} categories, {added_arts} articles added")


async def print_counts(session):
    """Print current record counts for verification."""
    tables = [
        ("restaurants", "Restaurants"),
        ("courses", "Courses"),
        ("course_spots", "Course Spots"),
        ("products", "Products"),
        ("guides", "Guides"),
        ("rolling_banners", "Banners"),
        ("events", "Events"),
        ("festivals", "Festivals"),
        ("transport_routes", "Transport Routes"),
        ("transport_tips", "Transport Tips"),
        ("themes", "Themes"),
        ("living_guide_categories", "LG Categories"),
        ("living_guide_articles", "LG Articles"),
    ]
    logger.info("\n  Record counts:")
    for table, label in tables:
        try:
            result = await session.execute(text(f"SELECT COUNT(*) FROM {table}"))
            count = result.scalar()
            logger.info(f"    {label}: {count}")
        except Exception:
            pass


async def run_seed():
    """Main seed function with duplicate prevention."""
    logger.info("=" * 60)
    logger.info("Exporoute - Seeding Database (Duplicate-Safe)")
    logger.info("=" * 60)

    # Create tables if they don't exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        # No clearing - preserve existing data

        logger.info("\n[1/9] Seeding restaurants (100)...")
        await seed_restaurants(session)

        logger.info("\n[2/9] Seeding courses (100)...")
        await seed_courses(session)

        logger.info("\n[3/9] Seeding products (30)...")
        await seed_products(session)

        logger.info("\n[4/9] Seeding guides (100)...")
        await seed_guides(session)

        logger.info("\n[5/9] Seeding banners...")
        await seed_banners(session)

        logger.info("\n[6/9] Seeding events...")
        await seed_events(session)

        logger.info("\n[7/9] Seeding festivals (100)...")
        await seed_festivals(session)

        logger.info("\n[8/9] Seeding transport...")
        await seed_transport(session)

        logger.info("\n[9/9] Seeding themes & living guide...")
        await seed_themes(session)
        await seed_living_guide(session)

        # Verify counts
        logger.info("\n" + "-" * 40)
        await print_counts(session)

    logger.info("\n" + "=" * 60)
    logger.info("Seeding complete! (existing data preserved)")
    logger.info("=" * 60)


if __name__ == "__main__":
    asyncio.run(run_seed())
