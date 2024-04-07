from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "orders" ALTER COLUMN "created_at" TYPE TIMESTAMPTZ USING "created_at"::TIMESTAMPTZ;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "orders" ALTER COLUMN "created_at" TYPE TIMESTAMPTZ USING "created_at"::TIMESTAMPTZ;"""
