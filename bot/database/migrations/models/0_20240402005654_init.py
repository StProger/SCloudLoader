from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "user_id" BIGSERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(64),
    "created_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "first_name" TEXT,
    "last_name" TEXT,
    "full_name" TEXT,
    "language_code" VARCHAR(5),
    "subscription_to" TIMESTAMPTZ
);
COMMENT ON TABLE "users" IS 'Таблица с пользователями ';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
