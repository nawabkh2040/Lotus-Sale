"""
SQLite persistence layer for Lotus Electronics chatbot.

Replaces Redis for durable data since Redis is optional/often down here. Stores:
  - sessions   : one row per chat session (id, timestamps, message count)
  - chat_logs  : every user/assistant message (powers the admin transcript view)
  - orders     : dummy orders (seeded + created via the chat "place order" flow)

Uses a fresh short-lived connection per call so it is safe under Flask's threaded
dev server. All functions are defensive: a DB error is logged and swallowed so
persistence never breaks the chat.
"""

import os
import json
import random
import sqlite3
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lotus_app.db")


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create tables if they don't exist. Safe to call repeatedly."""
    try:
        with _connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id    TEXT PRIMARY KEY,
                    created_at    TEXT NOT NULL,
                    last_active   TEXT NOT NULL,
                    message_count INTEGER NOT NULL DEFAULT 0
                );

                CREATE TABLE IF NOT EXISTS chat_logs (
                    id         INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    role       TEXT NOT NULL,
                    message    TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_chat_logs_session
                    ON chat_logs(session_id);

                CREATE TABLE IF NOT EXISTS orders (
                    order_id          TEXT PRIMARY KEY,
                    session_id        TEXT,
                    product_id        TEXT,
                    product_name      TEXT,
                    amount            TEXT,
                    status            TEXT,
                    order_date        TEXT,
                    expected_delivery TEXT,
                    timeline_json     TEXT
                );

                CREATE TABLE IF NOT EXISTS tickets (
                    ticket_id   TEXT PRIMARY KEY,
                    session_id  TEXT,
                    name        TEXT,
                    phone       TEXT,
                    issue       TEXT,
                    status      TEXT,
                    created_at  TEXT
                );
                """
            )
    except Exception as e:  # pragma: no cover - defensive
        print(f"❌ store.init_db failed: {type(e).__name__}: {e}")


# --------------------------------------------------------------------------- #
# Chat logging / sessions
# --------------------------------------------------------------------------- #
def log_message(session_id: str, role: str, message: str) -> None:
    """Record one message and upsert its session row."""
    if not session_id or not message:
        return
    now = datetime.utcnow().isoformat()
    try:
        with _connect() as conn:
            conn.execute(
                "INSERT INTO chat_logs (session_id, role, message, created_at) "
                "VALUES (?, ?, ?, ?)",
                (session_id, role, message, now),
            )
            conn.execute(
                """
                INSERT INTO sessions (session_id, created_at, last_active, message_count)
                VALUES (?, ?, ?, 1)
                ON CONFLICT(session_id) DO UPDATE SET
                    last_active = excluded.last_active,
                    message_count = message_count + 1
                """,
                (session_id, now, now),
            )
    except Exception as e:  # pragma: no cover - defensive
        print(f"❌ store.log_message failed: {type(e).__name__}: {e}")


def get_sessions() -> List[Dict[str, Any]]:
    try:
        with _connect() as conn:
            rows = conn.execute(
                "SELECT session_id, created_at, last_active, message_count "
                "FROM sessions ORDER BY last_active DESC"
            ).fetchall()
            return [dict(r) for r in rows]
    except Exception as e:  # pragma: no cover - defensive
        print(f"❌ store.get_sessions failed: {type(e).__name__}: {e}")
        return []


def get_chat_logs(session_id: str) -> List[Dict[str, Any]]:
    try:
        with _connect() as conn:
            rows = conn.execute(
                "SELECT role, message, created_at FROM chat_logs "
                "WHERE session_id = ? ORDER BY id ASC",
                (session_id,),
            ).fetchall()
            return [dict(r) for r in rows]
    except Exception as e:  # pragma: no cover - defensive
        print(f"❌ store.get_chat_logs failed: {type(e).__name__}: {e}")
        return []


def get_stats() -> Dict[str, int]:
    try:
        with _connect() as conn:
            sessions = conn.execute("SELECT COUNT(*) FROM sessions").fetchone()[0]
            messages = conn.execute("SELECT COUNT(*) FROM chat_logs").fetchone()[0]
            orders = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
            tickets = conn.execute("SELECT COUNT(*) FROM tickets").fetchone()[0]
            return {"sessions": sessions, "messages": messages, "orders": orders, "tickets": tickets}
    except Exception as e:  # pragma: no cover - defensive
        print(f"❌ store.get_stats failed: {type(e).__name__}: {e}")
        return {"sessions": 0, "messages": 0, "orders": 0, "tickets": 0}


# --------------------------------------------------------------------------- #
# Orders
# --------------------------------------------------------------------------- #
_STATUS_FLOW = ["Order Placed", "Processing", "Shipped", "Out for Delivery", "Delivered"]


def _build_timeline(current_status: str, order_dt: datetime) -> List[Dict[str, str]]:
    """Return a timeline marking each stage done/current/pending."""
    try:
        idx = _STATUS_FLOW.index(current_status)
    except ValueError:
        idx = 0
    timeline = []
    for i, stage in enumerate(_STATUS_FLOW):
        if i < idx:
            state = "done"
        elif i == idx:
            state = "current"
        else:
            state = "pending"
        stage_dt = order_dt + timedelta(days=i)
        timeline.append({"stage": stage, "state": state, "date": stage_dt.strftime("%d %b %Y")})
    return timeline


def _row_to_order(row: sqlite3.Row) -> Dict[str, Any]:
    d = dict(row)
    try:
        d["timeline"] = json.loads(d.pop("timeline_json") or "[]")
    except Exception:
        d["timeline"] = []
    return d


def create_order(session_id: Optional[str], product: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new order for a product dict (from catalog._public_view)."""
    order_id = "LOTUS" + str(random.randint(10000, 99999))
    order_dt = datetime.utcnow()
    status = "Processing"
    expected = (order_dt + timedelta(days=4)).strftime("%d %b %Y")
    timeline = _build_timeline(status, order_dt)
    record = {
        "order_id": order_id,
        "session_id": session_id,
        "product_id": str(product.get("product_id", "")),
        "product_name": product.get("product_name", "Product"),
        "amount": product.get("product_mrp", ""),
        "status": status,
        "order_date": order_dt.strftime("%d %b %Y"),
        "expected_delivery": expected,
        "timeline_json": json.dumps(timeline),
    }
    try:
        with _connect() as conn:
            conn.execute(
                "INSERT INTO orders (order_id, session_id, product_id, product_name, "
                "amount, status, order_date, expected_delivery, timeline_json) "
                "VALUES (:order_id, :session_id, :product_id, :product_name, :amount, "
                ":status, :order_date, :expected_delivery, :timeline_json)",
                record,
            )
    except Exception as e:  # pragma: no cover - defensive
        print(f"❌ store.create_order failed: {type(e).__name__}: {e}")
    out = dict(record)
    out["timeline"] = timeline
    out.pop("timeline_json", None)
    return out


def get_order(order_id: str) -> Optional[Dict[str, Any]]:
    if not order_id:
        return None
    oid = order_id.strip().upper()
    if not oid.startswith("LOTUS"):
        oid = "LOTUS" + oid.lstrip("#").strip()
    try:
        with _connect() as conn:
            row = conn.execute("SELECT * FROM orders WHERE order_id = ?", (oid,)).fetchone()
            return _row_to_order(row) if row else None
    except Exception as e:  # pragma: no cover - defensive
        print(f"❌ store.get_order failed: {type(e).__name__}: {e}")
        return None


def get_orders() -> List[Dict[str, Any]]:
    try:
        with _connect() as conn:
            rows = conn.execute("SELECT * FROM orders ORDER BY rowid DESC").fetchall()
            return [_row_to_order(r) for r in rows]
    except Exception as e:  # pragma: no cover - defensive
        print(f"❌ store.get_orders failed: {type(e).__name__}: {e}")
        return []


def seed_orders() -> None:
    """Insert a few dummy orders once, so tracking works out of the box."""
    try:
        with _connect() as conn:
            existing = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
            if existing:
                return
    except Exception as e:  # pragma: no cover - defensive
        print(f"❌ store.seed_orders check failed: {type(e).__name__}: {e}")
        return

    samples = [
        ("LOTUS1001", "40089", "Samsung Galaxy A26 5G (6GB/128GB) White", "₹21,557", "Delivered", 9),
        ("LOTUS1002", "41002", "Samsung 43 inch 4K Ultra HD Smart LED TV", "₹32,990", "Out for Delivery", 3),
        ("LOTUS1003", "42010", "HP Pavilion 15 (i5, 16GB, 512GB SSD)", "₹61,990", "Shipped", 2),
        ("LOTUS1004", "43001", "LG 1.5 Ton 5 Star Dual Inverter Split AC", "₹42,990", "Processing", 1),
    ]
    for order_id, pid, name, amount, status, days_ago in samples:
        order_dt = datetime.utcnow() - timedelta(days=days_ago)
        expected = (order_dt + timedelta(days=4)).strftime("%d %b %Y")
        timeline = _build_timeline(status, order_dt)
        record = {
            "order_id": order_id,
            "session_id": "seed",
            "product_id": pid,
            "product_name": name,
            "amount": amount,
            "status": status,
            "order_date": order_dt.strftime("%d %b %Y"),
            "expected_delivery": expected,
            "timeline_json": json.dumps(timeline),
        }
        try:
            with _connect() as conn:
                conn.execute(
                    "INSERT OR IGNORE INTO orders (order_id, session_id, product_id, "
                    "product_name, amount, status, order_date, expected_delivery, "
                    "timeline_json) VALUES (:order_id, :session_id, :product_id, "
                    ":product_name, :amount, :status, :order_date, :expected_delivery, "
                    ":timeline_json)",
                    record,
                )
        except Exception as e:  # pragma: no cover - defensive
            print(f"❌ store.seed_orders insert failed: {type(e).__name__}: {e}")


# --------------------------------------------------------------------------- #
# Support tickets
# --------------------------------------------------------------------------- #
def create_ticket(session_id: Optional[str], name: str, phone: str, issue: str) -> Dict[str, Any]:
    """Create a support ticket and return it."""
    ticket_id = "TCKT" + str(random.randint(10000, 99999))
    created = datetime.utcnow()
    record = {
        "ticket_id": ticket_id,
        "session_id": session_id,
        "name": (name or "").strip(),
        "phone": (phone or "").strip(),
        "issue": (issue or "").strip(),
        "status": "Open",
        "created_at": created.isoformat(),
    }
    try:
        with _connect() as conn:
            conn.execute(
                "INSERT INTO tickets (ticket_id, session_id, name, phone, issue, "
                "status, created_at) VALUES (:ticket_id, :session_id, :name, :phone, "
                ":issue, :status, :created_at)",
                record,
            )
    except Exception as e:  # pragma: no cover - defensive
        print(f"❌ store.create_ticket failed: {type(e).__name__}: {e}")
    out = dict(record)
    out["created_date"] = created.strftime("%d %b %Y, %I:%M %p")
    return out


def get_tickets() -> List[Dict[str, Any]]:
    try:
        with _connect() as conn:
            rows = conn.execute("SELECT * FROM tickets ORDER BY rowid DESC").fetchall()
            return [dict(r) for r in rows]
    except Exception as e:  # pragma: no cover - defensive
        print(f"❌ store.get_tickets failed: {type(e).__name__}: {e}")
        return []
