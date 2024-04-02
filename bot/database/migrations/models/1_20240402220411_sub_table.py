from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "subs" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "is_bot" BOOL NOT NULL  DEFAULT False,
    "is_active" BOOL NOT NULL  DEFAULT True,
    "title" TEXT NOT NULL,
    "link" TEXT NOT NULL,
    "bot_token" TEXT NOT NULL,
    "visits" BIGINT NOT NULL  DEFAULT 0,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE "subs" IS 'Таблица с обязательными подписками ';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "subs";"""
