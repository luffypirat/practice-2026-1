import asyncio
import aiosqlite


async def create_db():
    async with aiosqlite.connect("tasks.db") as db:
        await db.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id      INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        text    TEXT,
        done    BOOLEAN DEFAULT FALSE
    )
""")
        await db.commit()

async def add_task(user_id: int, text: str):
    async with aiosqlite.connect("tasks.db") as db:
        await db.execute("INSERT INTO tasks (user_id, text) VALUES (?, ?)", (user_id, text))
        await db.commit()

async def get_task(user_id: int):
    async with aiosqlite.connect("tasks.db") as db:
        async with db.execute("SELECT id, text, done FROM tasks WHERE user_id = ?", (user_id,)) as cursor:
            rows = await cursor.fetchall()
        return rows

async def done_task(user_id: int, id: int):
    async with aiosqlite.connect("tasks.db") as db:
        async with db.execute("UPDATE tasks SET done = 1 WHERE id = ? AND user_id = ?", (id, user_id)) as cursor:
            rows =  cursor.rowcount
        await db.commit()
        return rows

async def delete_task(user_id: int, id: int):
    async with aiosqlite.connect("tasks.db") as db:
        async with db.execute("DELETE FROM tasks WHERE id = ? AND user_id = ?", (id, user_id)) as cursor:
            rows = cursor.rowcount
        await db.commit()
        return rows

async def delete_all_done_task(user_id: int):
    async with aiosqlite.connect("tasks.db") as db:
        await db.execute("DELETE FROM tasks WHERE user_id = ? AND done = 1", (user_id,))
        await db.commit()