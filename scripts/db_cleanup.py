#!/usr/bin/env python3
"""
Database cleanup script for Inventory Management.
Removes old logs, expired sessions, and orphaned records.
"""

import os
from datetime import datetime, timedelta
from pymongo import MongoClient
from dotenv import load_dotenv

# Load env vars from .env or config
load_dotenv(r"../config/environment/dev.env")

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "inventory_db")


def main():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]

    # Example 1: remove old logs (>30 days)
    cutoff = datetime.utcnow() - timedelta(days=30)
    logs_deleted = db.logs.delete_many({"timestamp": {"$lt": cutoff}})
    print(f"🗑 Deleted {logs_deleted.deleted_count} old logs")

    # Example 2: clear expired sessions
    sessions_deleted = db.sessions.delete_many(
        {"expiresAt": {"$lt": datetime.utcnow()}}
    )
    print(f"🗑 Deleted {sessions_deleted.deleted_count} expired sessions")

    # Example 3: remove orphaned inventory items (no productId reference)
    orphaned_deleted = db.inventory.delete_many({"productId": {"$exists": False}})
    print(f"🗑 Deleted {orphaned_deleted.deleted_count} orphaned inventory items")

    client.close()
    print("✅ Database cleanup complete.")


if __name__ == "__main__":
    main()
