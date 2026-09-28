-- ==============================================================================
-- PROJECT 2: E-COMMERCE ANALYTICS DATABASE QUERIES
-- Data Mastery All-In-One (2026 Edition)
-- ==============================================================================

-- 1. DDL: Tạo các bảng cơ sở dữ liệu
CREATE TABLE IF NOT EXISTS customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    city VARCHAR(50),
    signup_date DATE
);

CREATE TABLE IF NOT EXISTS orders (
    order_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50),
    order_purchase_timestamp TIMESTAMP,
    order_status VARCHAR(50),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE IF NOT EXISTS order_items (
    order_id VARCHAR(50),
    item_id VARCHAR(50),
    category VARCHAR(50),
    price NUMERIC(10, 2),
    quantity INT,
    PRIMARY KEY (order_id, item_id),
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

CREATE TABLE IF NOT EXISTS payments (
    order_id VARCHAR(50),
    payment_method VARCHAR(50),
    payment_value NUMERIC(10, 2),
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

-- ==============================================================================
-- 2. TRUY VẤN CƠ BẢN: SELECT, WHERE, GROUP BY, HAVING
-- ==============================================================================

-- Truy vấn 1: Top 5 thành phố có nhiều khách hàng nhất
SELECT 
    city,
    COUNT(customer_id) AS total_customers
FROM customers
GROUP BY city
ORDER BY total_customers DESC
LIMIT 5;

-- Truy vấn 2: Thống kê số lượng đơn hàng theo trạng thái
SELECT 
    order_status,
    COUNT(order_id) AS order_count,
    ROUND(COUNT(order_id) * 100.0 / (SELECT COUNT(*) FROM orders), 2) AS percentage
FROM orders
GROUP BY order_status
ORDER BY order_count DESC;

-- Truy vấn 3: Các danh mục sản phẩm có tổng doanh thu vượt trên $10,000
SELECT 
    category,
    SUM(quantity) AS total_units_sold,
    ROUND(SUM(price * quantity), 2) AS total_revenue
FROM order_items
GROUP BY category
HAVING SUM(price * quantity) > 10000
ORDER BY total_revenue DESC;

-- ==============================================================================
-- 3. TRUY VẤN NÂNG CAO: JOIN, CTE & WINDOW FUNCTIONS
-- ==============================================================================

-- Truy vấn 4: Doanh thu theo phương thức thanh toán và tỷ lệ phần trăm
SELECT 
    p.payment_method,
    COUNT(DISTINCT p.order_id) AS total_orders,
    ROUND(SUM(p.payment_value), 2) AS total_revenue,
    ROUND(SUM(p.payment_value) * 100.0 / SUM(SUM(p.payment_value)) OVER(), 2) AS pct_of_total
FROM payments p
INNER JOIN orders o ON p.order_id = o.order_id
WHERE o.order_status = 'COMPLETED'
GROUP BY p.payment_method
ORDER BY total_revenue DESC;

-- Truy vấn 5: Phân tích Khách hàng VIP qua CTE (Top 10 Khách chi tiêu cao nhất)
WITH customer_spending AS (
    SELECT 
        c.customer_id,
        c.customer_name,
        c.city,
        COUNT(DISTINCT o.order_id) AS order_count,
        ROUND(SUM(oi.price * oi.quantity), 2) AS total_spend
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.order_status = 'COMPLETED'
    GROUP BY c.customer_id, c.customer_name, c.city
)
SELECT 
    customer_id,
    customer_name,
    city,
    order_count,
    total_spend,
    DENSE_RANK() OVER (ORDER BY total_spend DESC) AS spending_rank
FROM customer_spending
ORDER BY spending_rank
LIMIT 10;

-- Truy vấn 6: Running Total Doanh Thu Hàng Tháng & Tăng Trưởng MoM
WITH monthly_revenue AS (
    SELECT 
        strftime('%Y-%m', o.order_purchase_timestamp) AS order_month,
        ROUND(SUM(oi.price * oi.quantity), 2) AS monthly_rev
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.order_status = 'COMPLETED'
    GROUP BY strftime('%Y-%m', o.order_purchase_timestamp)
)
SELECT 
    order_month,
    monthly_rev,
    LAG(monthly_rev, 1) OVER (ORDER BY order_month) AS prev_month_rev,
    ROUND(
        (monthly_rev - LAG(monthly_rev, 1) OVER (ORDER BY order_month)) * 100.0 /
        LAG(monthly_rev, 1) OVER (ORDER BY order_month), 2
    ) AS mom_growth_pct,
    SUM(monthly_rev) OVER (ORDER BY order_month ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cumulative_revenue
FROM monthly_revenue
ORDER BY order_month;

-- Truy vấn 7: Top 1 sản phẩm bán chạy nhất trong từng danh mục (Window Function)
WITH ranked_products AS (
    SELECT 
        category,
        item_id,
        SUM(quantity) AS units_sold,
        ROUND(SUM(price * quantity), 2) AS revenue,
        ROW_NUMBER() OVER (PARTITION BY category ORDER BY SUM(quantity) DESC) AS rank_in_cat
    FROM order_items
    GROUP BY category, item_id
)
SELECT 
    category,
    item_id,
    units_sold,
    revenue
FROM ranked_products
WHERE rank_in_cat = 1
ORDER BY units_sold DESC;
