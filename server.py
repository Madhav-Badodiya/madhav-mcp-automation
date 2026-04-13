from mcp.server.fastmcp import FastMCP
from playwright.async_api import async_playwright, expect
import pyodbc

# Create the MCP server with a name
mcp = FastMCP("Madhav Automation Server")

# Global browser state - keeps browser open between tool calls
playwright_instance = None
browser = None
page = None

# ─────────────────────────────────────────
# TOOL 1: Hello (test tool)
# ─────────────────────────────────────────
@mcp.tool()
async def hello(name: str) -> str:
    """Say hello to someone"""
    return f"Hello {name}! Your MCP server is working!"

# ─────────────────────────────────────────
# TOOL 2: Login
# ─────────────────────────────────────────
@mcp.tool()
async def login(email: str, password: str) -> str:
    """Open browser and log into Rahul Shetty Academy website"""
    global playwright_instance, browser, page

    try:
        # Start Playwright engine
        playwright_instance = await async_playwright().start()

        # Launch visible Chromium browser
        browser = await playwright_instance.chromium.launch(headless=False)

        # Open a new tab
        page = await browser.new_page()

        # Go to login page
        await page.goto("https://rahulshettyacademy.com/client/#/auth/login")

        # Fill email using ID locator
        await page.fill("#userEmail", email)

        # Fill password using ID locator
        await page.fill("#userPassword", password)

        # Click login button using ID locator
        await page.click("#login")

        # Wait for dashboard URL to confirm login worked
        await page.wait_for_url("**/dashboard/**", timeout=15000)
        return f"Login successful! Logged in as {email}"

    except Exception as e:
        return f"Login failed: {str(e)}"

# ─────────────────────────────────────────``
# TOOL 3: Find Product and Add to Cart
# ─────────────────────────────────────────

@mcp.tool()
async def find_and_add_to_cart(product_name: str) -> str:
    """Find a product by name on dashboard and add it to cart"""
    global page

    if page is None:
        return "Error: Browser not open. Please run Login first."

    try:
        all_cards = page.locator(".card")
        card_count = await all_cards.count()

        for i in range(card_count):
            card = all_cards.nth(i)
            name_element = card.locator("h5 b")
            product_text = await name_element.inner_text()

            if product_name.upper() in product_text.upper():
                add_to_cart_btn = card.locator("button:has-text('Add To Cart')")
                await add_to_cart_btn.click()

                toast = page.locator(".toast-message")
                await toast.wait_for(timeout=5000)
                toast_text = await toast.inner_text()

                #await page.locator("button.btn-custom").click()
                await page.locator('button[routerlink="/dashboard/cart"]').click()
                await page.wait_for_url("**/cart**", timeout=5000)    

                return f"Success! Found '{product_text}' → clicked Add To Cart → Toast says: '{toast_text.strip()}'"

        return f"Product '{product_name}' not found on dashboard."

    except Exception as e:
        return f"Error in find_and_add_to_cart: {str(e)}"

@mcp.tool()
async def view_cart() -> str:
    """View all items currently in the cart"""
    global page

    #Gaurd Clause to ensure we have a browser page to work with
    if page is None:
        return "Error: Browser not open. Please run Login first."

    try:
        await page.locator("li.items").first.wait_for(timeout=5000)

        all_items = page.locator("li.items")
        item_count = await all_items.count()

        result = f"Total items in cart: {item_count}\n"

        if item_count == 0:
            return "Your cart is empty."

        for i in range(item_count):
            item = all_items.nth(i)
            item_name = await item.locator("h3").inner_text()
            item_price = await item.locator("p:has-text('MRP')").inner_text()
            result += f"{i+1}. {item_name} - {item_price.strip()}\n"

        #return f"Items in your cart: {', '.join(items_list)}"
        total = await page.locator(".value").last.inner_text()
        result += f"\nOrder Total: {total.strip()}"

        await page.get_by_role("button", name="Checkout").click()
        await page.wait_for_url("**/order**", timeout=5000)
        result += "\n\nNavigated to Checkout page successfully."
        
        return result

    except Exception as e:
        return f"Error in view_cart: {str(e)}"

# ─────────────────────────────────────────
# TOOL 5: Checkout
# ─────────────────────────────────────────

@mcp.tool()
async def checkout(country: str) -> str:
    """Complete the checkout process by selecting country and placing order"""
    global page

    if page is None:
        return "Error: Browser not open. Please run Login first."

    try:
        # Wait for page to fully render
        await page.wait_for_load_state("networkidle", timeout=10000)

        # Wait for country input
        country_input = page.locator("[placeholder='Select Country']")
        await country_input.wait_for(timeout=5000)

        # Click to focus then type character by character
        await country_input.click()
        await country_input.type(country, delay=100)

        # Wait for dropdown to populate
        await page.locator(".ta-item").first.wait_for(timeout=8000)

        # ── BUG-004 FIX ────────────────────────────────
        # Loop through all options, match exact text
        # Prevents partial match catching wrong country
        all_options = page.locator(".ta-item")
        option_count = await all_options.count()
        country_clicked = False

        for i in range(option_count):
            option = all_options.nth(i)
            option_text = await option.inner_text()
            if option_text.strip() == country.strip():
                await option.click()
                country_clicked = True
                break

        # If no exact match found, report clearly
        if not country_clicked:
            return f"Country '{country}' not found in dropdown. Check spelling."
        # ───────────────────────────────────────────────

        # Wait for selection to register
        await page.wait_for_load_state("networkidle", timeout=5000)

        # Click Place Order
        await page.locator("a.btnn.action__submit").click()

        # Confirm via toast
        await page.locator(".toast-title").wait_for(timeout=8000)
        toast_text = await page.locator(".toast-title").inner_text()

        thank_you = page.locator("h1.hero-primary")
        await thank_you.wait_for(timeout=8000)
        heading_text = await thank_you.inner_text()

        await page.locator("button[routerlink='/dashboard/myorders']").click()
        await page.wait_for_url("**/myorders**", timeout=5000)

        return (
            f"✅ Order placed! Country: {country}\n"
            f"✅ Toast: '{toast_text.strip()}'\n"
            f"✅ Page confirmed: '{heading_text.strip()}'\n"
            f"✅ Navigated to Orders History page"
        )

    except Exception as e:
        return f"Error in checkout: {str(e)}"

# ─────────────────────────────────────────
# TOOL 6: Get Order History
# ─────────────────────────────────────────

@mcp.tool()
async def get_order_history() -> str:
    """Retrieve and return a list of past orders from the Orders History page"""
    global page

    if page is None:
        return "Error: Browser not open. Please run Login first."

    try:
        await page.locator("tbody tr").first.wait_for(timeout=8000)

        all_orders = page.locator("tbody tr")
        order_count = await all_orders.count()

        if order_count == 0:
            return "No past orders found in your order history."

        result = f"Total past orders: {order_count}\n\n"
        result += "─" * 40 + "\n"

        for i in range(order_count):
            order = all_orders.nth(i)
            order_id = await order.locator("th[scope='row']").inner_text()
            product = await order.locator("td:nth-child(3)").inner_text()
            price = await order.locator("td:nth-child(4)").inner_text()
            date = await order.locator("td:nth-child(5)").inner_text()

            result += f"Order {i+1}:\n"
            result += f"  ID: {order_id.strip()}\n"
            result += f"  Product: {product.strip()}\n"
            result += f"  Price: {price.strip()}\n"
            result += f"  Date: {date.strip()}\n"
            result += "─" * 40 + "\n"

        return result

    except Exception as e:
        return f"Error in get_order_history: {str(e)}"
    
# ─────────────────────────────────────────
# TOOL 7:  Get Screenshot
# ─────────────────────────────────────────

@mcp.tool()
async def take_screenshot(filename: str) -> str:
    """Take a screenshot of the current browser state and save it"""
    global page

    if page is None:
        return "Error: Browser not open. Please run Login first."

    try:
        # Build the full file path
        # screenshots folder inside your project directory
        filepath = f"D:\\madhav-mcp\\screenshots\\{filename}.png"

        # One line — Playwright saves the screenshot
        # full_page=False means only visible area, not entire scrollable page
        await page.screenshot(path=filepath, full_page=False)

        return f"Screenshot saved: {filepath}"

    except Exception as e:
        return f"Error in take_screenshot: {str(e)}"
    

# ─────────────────────────────────────────
# DB CONNECTION HELPER
# ─────────────────────────────────────────
def get_db_connection():
    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost\\SQLEXPRESS;"
        "DATABASE=madhav_test_data;"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )
    return pyodbc.connect(conn_str)

# ─────────────────────────────────────────
# TOOL 8: Get Test User from Database
# ─────────────────────────────────────────

@mcp.tool()
async def get_test_user(role: str) -> str:
    """Fetch login credentials from SQL server based on user role (e.g., 'admin', 'user')"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT email, password FROM test_users WHERE role = ?", role)
        
        row = cursor.fetchone()
        conn.close()

        if row is None:
            return f"No user found with role '{role}'."

        email, password = row
        return f"Credentials for role '{role}': Email: {email}, Password: {password}"

    except Exception as e:
        return f"DB Error in fetching get_test_user from database: {str(e)}"

# ─────────────────────────────────────────
# TOOL 9: Get Test Product from Database
# ─────────────────────────────────────────

@mcp.tool()
async def get_test_product(category: str) -> str:  
    """Fetch a product name from SQL server by category"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM test_products WHERE category = ?", category)

        row = cursor.fetchone()
        conn.close()

        if row is None:
            return f"No product found in category '{category}'."
        
        product_name = row[0]
        return f"Test product in category '{category}': {product_name}"
    
    except Exception as e:
        return f"DB Error in fetching get_test_product from database: {str(e)}"


# ─────────────────────────────────────────
# Run the server
# ─────────────────────────────────────────
if __name__ == "__main__":
    mcp.run(transport="stdio")