# -*- coding: utf-8 -*-
import aiopg
from urllib.parse import urlparse
from typing import Optional, Tuple, List, Any
import sys, asyncio


class DataBase:
    def __init__(self, max_conections: int) -> None:
        self.max_conections = max_conections
        self.pool: Optional[aiopg.Pool] = None
        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    async def connect(self, url: str) -> None:
        # also run on windows
        p = urlparse(url)
        dsn = f"dbname={p.path[1:]} user={p.username} password={p.password} host={p.hostname}"
        self.pool = await aiopg.create_pool(dsn=dsn, maxsize=self.max_conections)

    def close(self) -> None:
        print(f"- Fechando conexões do pool.")
        self.pool.terminate()
        print(f"- {self.pool.size} conexões terminadas.")

    async def set(self, querry: str, *valores: Any) -> None:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(querry, valores)

    async def get(self, querry: str, *valores: Any) -> List[Tuple]:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(querry, valores)
                return await cur.fetchall()

    async def set_count(self, querry: str, *valores: Any) -> int:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(querry, valores)
                return cur.rowcount