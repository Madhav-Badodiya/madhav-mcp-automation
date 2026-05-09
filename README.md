# Madhav MCP Automation

AI-powered browser automation using MCP (Model Context Protocol) + Playwright + Python + Claude Desktop.

## What This Project Does

Natural language instruction → Claude AI → MCP Server → Playwright/httpx → Real browser + API automation

## Tech Stack

- Python 3.14
- Playwright (async)
- FastMCP (MCP SDK)
- Claude Desktop
- SQL Server Express
- pyodbc
- httpx

-------------------------------------------------------------------

## Project Structure

madhav-mcp-automation/
├── server.py               # UI + DB tools (Phases 1-5, 7)
├── api_testing_server.py   # API testing tools (Phase 6)
├── db/
│   └── schema.sql          # Database schema and seed data
├── bug_Report.txt          # Bugs found during automation
└── README.md

-------------------------------------------------------------------

## UI Automation Tools (server.py)

| Tool | What It Does |
|------|-------------|
| hello() | Test tool — verifies MCP connection |
| login() | Opens browser and logs into website |
| find_and_add_to_cart() | Finds product by name and adds to cart |
| view_cart() | Reads all cart items and total |
| checkout() | Selects country and places order |
| get_order_history() | Retrieves all past orders |
| take_screenshot() | Saves screenshot at any step |
| get_test_user() | Fetches credentials from SQL Server |
| get_test_product() | Fetches product name from SQL Server |

## API Testing Tools (api_testing_server.py)

| Tool | What It Does |
|------|-------------|
| api_login() | Calls login API and stores auth token |
| api_get_products() | Fetches all products from API |
| api_create_order() | Creates an order via API |
| api_get_orders() | Fetches single order details |
| api_get_all_orders() | Fetches full order history for a user |
| api_delete_product() | Deletes a product via API |

## Full Hybrid Flow

One instruction drives the entire stack:

DB credentials → API login → API products → Browser login →
Add to cart (UI) → Create order (API) → Verify in order history (API)

Zero hardcoded values. Everything driven from SQL Server.

## Project Status

- Phase 1 — Environment Setup ✅
- Phase 2 — Claude Desktop Connection ✅
- Phase 3 — Login Tool ✅
- Phase 4 — Core Automation Tools ✅
- Phase 5 — SQL Server Integration ✅
- Phase 6 — API Testing Tools ✅
- Phase 7 — Error Handling + Auto-screenshot + Full Demo ✅

## Bugs Found

See `bug_Report.txt` for full details.

- BUG-001 — Search bar non-functional (High)
- BUG-002 — Angular typeahead dropdown not triggered by programmatic input (Medium)
- BUG-003 — Country dropdown returns ambiguous results (Medium)
- BUG-004 — Orders silently deleted without user consent (High)

## Author

Madhav Badodiya — QA Automation Engineer  
[linkedin.com/in/madhavbadodiya](https://linkedin.com/in/madhavbadodiya)  
[github.com/Madhav-Badodiya](https://github.com/Madhav-Badodiya)
