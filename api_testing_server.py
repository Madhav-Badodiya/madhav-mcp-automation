from mcp.server.fastmcp import FastMCP
import httpx

mcp = FastMCP("Madhav API testing server")

BASE_URL = "https://rahulshettyacademy.com"

auth_token: str | None = None

@mcp.tool()
async def api_login(email: str, password: str) -> str:
    """Call the login API and store the auth token for subsequent requests"""
    global auth_token

    payload = {
        "userEmail": email,
        "userPassword": password
    }
    try: 
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{BASE_URL}/api/ecom/auth/login", json=payload)
            response.raise_for_status()
            data = response.json()
            if response.status_code != 200:
                return f"Assertion Failed! Expected status 200 but got {response.status_code}"

            if data.get("message") != "Login Successfully":
                return f"Assertion Failed! Expected 'Login Successfully' but got {data.get('message')}"
            
            auth_token = data.get("token")
            user_id = data.get("userId")
            success_message = data.get("message")
            return f"Login successful! User ID: {user_id}, token: {auth_token[:30]}... , Message: {success_message}"
    except Exception as e:
            return f"Error in api_login: {str(e)}"
    
@mcp.tool()
async def api_get_products() -> str:
    """Call the get products API using the stored auth token"""
    if not auth_token:
        return "Error: Not authenticated. Please login first."

    payload = {
        "productName": "",
        "minPrice": None,
        "maxPrice": None,
        "productCategory": [],
        "productSubCategory": []
    }

    headers = { "Authorization": auth_token}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{BASE_URL}/api/ecom/product/get-all-products", json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            if response.status_code != 200:
                return f"Assertion Failed! Expected status 200 but got {response.status_code}"
            
            if data.get("message") != "All Products fetched Successfully":
                return f"Assertion Failed! Expected 'All Products fetched Successfully' but got {data.get('message')}"
            
            products = data.get("data", [])
            result = f"Total products retrieved: {len(products)}\n"
            for product in products:  # Show details of first 5 products
                result += f"Name: {product.get('productName')}, ID: {product.get('_id')}, Price: {product.get('productPrice')}, Category: {product.get('productCategory')}\n"
            return result
    except Exception as e:
        return f"Error in api_get_products: {str(e)}"

@mcp.tool()
async def api_create_order(country: str, productOrderedId: str) -> str:
    """Call the create order API using the stored auth token"""
    if not auth_token:
        return "Error: Not authenticated. Please login first."

    payload = {
        "orders": [
            {
                "country": country,
                "productOrderedId": productOrderedId
            }
        ]
    }
    headers = { "Authorization": auth_token}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{BASE_URL}/api/ecom/order/create-order", json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            if response.status_code != 201:
                return f"Assertion Failed! Expected status 201 but got {response.status_code}"
            
            if data.get("message") != "Order Placed Successfully":
                return f"Assertion Failed! Expected 'Order Placed Successfully' but got {data.get('message')}"
            
            return f" Order ID: {data.get('orders', [])[0]} Product ID: {data.get('productOrderId', []) [0] } created successfully! Message: {data.get('message')}"   
    except Exception as e:
        return f"Error in api_create_order: {str(e)}"
    
@mcp.tool()
async def api_get_orders(order_id: str) -> str:
    """Call the get orders API using the stored auth token"""
    if not auth_token:
        return "Error: Not authenticated. Please login first."

    headers = { "Authorization": auth_token}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/api/ecom/order/get-orders-details",headers=headers,params={"id": order_id})
            response.raise_for_status()
            data = response.json()
            if response.status_code != 200:
                return f"Assertion Failed! Expected status 200 but got {response.status_code}"
            if data.get("message") != "Orders fetched for customer Successfully":
                return f"Assertion Failed! Expected 'Orders fetched for customer Successfully' but got {data.get('message')}"
            order = data.get("data", {})
            return f"Order ID: {order.get('_id')}, Product Name: {order.get('productName')}, Country: {order.get('country')}, Price: {order.get('orderPrice')}, Message: {data.get('message')}"
    except Exception as e:
        return f"Error in api_get_orders: {str(e)}"     
    
@mcp.tool()
async def api_get_all_orders(user_id: str) -> str:
    """Call the get all orders API using the stored auth token"""
    if not auth_token:
        return "Error: Not authenticated. Please login first."

    headers = { "Authorization": auth_token}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/api/ecom/order/get-orders-for-customer/{user_id}",headers=headers)
            response.raise_for_status()
            data = response.json()
            if response.status_code != 200:
                return f"Assertion Failed! Expected status 200 but got {response.status_code}"
            if data.get("message") != "Orders fetched for customer Successfully":
                return f"Assertion Failed! Expected 'Orders fetched for customer Successfully' but got {data.get('message')}"
            orders = data.get("data", [])
            result = f"Total orders retrieved: {len(orders)}\n"
            for order in orders:
                result += f"Order ID: {order.get('_id')}, Product Name: {order.get('productName')}, Country: {order.get('country')}, Price: {order.get('orderPrice')}\n"
            return f"Order details retrieved successfully! {result}"
    except Exception as e:
        return f"Error in api_get_all_orders: {str(e)}"
    
@mcp.tool()
async def api_delete_product(productId: str) -> str:
    """Call the delete product API using the stored auth token"""
    if not auth_token:
        return "Error: Not authenticated. Please login first."

    headers = { "Authorization": auth_token}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(f"{BASE_URL}/api/ecom/product/delete-product/{productId}",headers=headers)
            response.raise_for_status()
            data = response.json()
            if response.status_code != 200:
                return f"Assertion Failed! Expected status 200 but got {response.status_code}"  
            if data.get("message") != "Product Deleted Successfully":
                return f"Assertion Failed! Expected 'Product Deleted Successfully' but got {data.get('message')}"
            return f"Product ID: {productId} deleted successfully! Message: {data.get('message')}"
    except Exception as e:
        return f"Error in api_delete_product: {str(e)}"    

if __name__ == "__main__":
    mcp.run(transport="stdio")