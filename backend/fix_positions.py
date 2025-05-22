"""
Script to fix aircraft position data by extracting coordinates from raw_data
"""
import asyncio
import json
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app.core.config import settings

async def fix_aircraft_positions():
    """Extract coordinates from raw_data and populate position column"""
    
    # Create async engine
    engine = create_async_engine(
        f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
    )
    
    async with AsyncSession(engine) as session:
        try:
            # Get all aircraft with null positions but with raw_data
            result = await session.execute(text("""
                SELECT id, raw_data 
                FROM aircraft 
                WHERE position IS NULL 
                AND raw_data IS NOT NULL
                LIMIT 1000
            """))
            
            aircraft_rows = result.fetchall()
            updated_count = 0
            
            print(f"Found {len(aircraft_rows)} aircraft with null positions")
            
            for row in aircraft_rows:
                aircraft_id, raw_data = row
                
                if not raw_data:
                    continue
                    
                lat = None
                lon = None
                
                # Try to extract coordinates from various places in raw_data
                if isinstance(raw_data, dict):
                    # Check direct lat/lon
                    if raw_data.get('latitude') and raw_data.get('longitude'):
                        lat = raw_data['latitude']
                        lon = raw_data['longitude']
                    # Check lastPosition
                    elif raw_data.get('lastPosition'):
                        last_pos = raw_data['lastPosition']
                        if last_pos.get('lat') and last_pos.get('lon'):
                            lat = last_pos['lat']
                            lon = last_pos['lon']
                    # Check raw_data.raw_data (nested)
                    elif raw_data.get('raw_data'):
                        nested = raw_data['raw_data']
                        if nested.get('lastPosition'):
                            last_pos = nested['lastPosition']
                            if last_pos.get('lat') and last_pos.get('lon'):
                                lat = last_pos['lat']
                                lon = last_pos['lon']
                
                if lat is not None and lon is not None:
                    try:
                        # Update the position using PostGIS function
                        await session.execute(text("""
                            UPDATE aircraft 
                            SET position = ST_GeomFromText(:wkt, 4326)
                            WHERE id = :aircraft_id
                        """), {
                            'wkt': f'POINT({lon} {lat})',
                            'aircraft_id': aircraft_id
                        })
                        updated_count += 1
                        
                        if updated_count % 100 == 0:
                            print(f"Updated {updated_count} aircraft positions...")
                            
                    except Exception as e:
                        print(f"Error updating aircraft {aircraft_id}: {e}")
            
            await session.commit()
            print(f"Successfully updated {updated_count} aircraft positions")
            
        except Exception as e:
            print(f"Error: {e}")
            await session.rollback()
        finally:
            await engine.dispose()

if __name__ == "__main__":
    asyncio.run(fix_aircraft_positions())