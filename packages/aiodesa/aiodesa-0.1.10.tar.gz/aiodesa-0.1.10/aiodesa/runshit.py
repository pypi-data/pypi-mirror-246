import aiosqlite

async def create_database():
    async with aiosqlite.connect("example.sqlite3") as db:
        # Create a table
        create_table_query = f'''
            CREATE TABLE IF NOT EXISTS user_economy (
                username TEXT PRIMARY KEY,
                credits INTEGER,
                points INTEGER,
                id TEXT UNIQUE
            );
        '''
        await db.execute(create_table_query)
        await db.commit()

        # Insert a sample record
        insert_query = '''
            INSERT INTO user_economy (username, credits, points, id)
            VALUES (?, ?, ?, ?);
        '''
        sample_record_values = ("sample_user", 100, 50, "abc123")
        await db.execute(insert_query, sample_record_values)
        await db.commit()

        # Insert a sample record and attempt to duplicate id
        # sqlite3.IntegrityError: UNIQUE constraint failed
        insert_query = '''
            INSERT INTO user_economy (username, credits, points, id)
            VALUES (?, ?, ?, ?);
        '''
        sample_record_values = ("sample_user_2", 100, 50, "abc123")
        await db.execute(insert_query, sample_record_values)
        await db.commit()

        # Update a record
        update_query = '''
            UPDATE user_economy
            SET points = ?
            WHERE username = ?;
        '''
        updated_points = 75
        await db.execute(update_query, (updated_points, "sample_user"))
        await db.commit()

async def main():
    await create_database()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
