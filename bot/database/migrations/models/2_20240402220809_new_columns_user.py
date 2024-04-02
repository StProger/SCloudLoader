from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" ADD "subbed" BOOL NOT NULL  DEFAULT False;
        ALTER TABLE "users" ADD "subbed_before" BOOL NOT NULL  DEFAULT False;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" DROP COLUMN "subbed";
        ALTER TABLE "users" DROP COLUMN "subbed_before";"""
