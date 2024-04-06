from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "orders" (
    "order_id" SERIAL NOT NULL PRIMARY KEY,
    "count_month" INT NOT NULL,
    "user_id" BIGINT NOT NULL
);
COMMENT ON TABLE "orders" IS 'Таблица с обязательными подписками ';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "orders";"""
