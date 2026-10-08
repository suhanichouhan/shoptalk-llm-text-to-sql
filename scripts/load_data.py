import sqlite3
from pathlib import Path
import pandas as pd

RAW = Path("data/raw")
DB = Path("data/olist.db")

FILES = {
    "customers": "olist_customers_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "payments": "olist_order_payments_dataset.csv",
    "reviews": "olist_order_reviews_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "category_translation": "product_category_name_translation.csv",
}

INDEXES = [
    "CREATE INDEX idx_orders_customer ON orders(customer_id)",
    "CREATE INDEX idx_items_order ON order_items(order_id)",
    "CREATE INDEX idx_items_product ON order_items(product_id)",
    "CREATE INDEX idx_items_seller ON order_items(seller_id)",
    "CREATE INDEX idx_payments_order ON payments(order_id)",
    "CREATE INDEX idx_reviews_order ON reviews(order_id)",
]

def main():
    DB.parent.mkdir(exist_ok=True)
    if DB.exists():
        DB.unlink()
    con = sqlite3.connect(DB)
    for table, fname in FILES.items():
        df = pd.read_csv(RAW / fname)
        if table == "reviews":
            df = df.drop(columns=["review_comment_title", "review_comment_message"],
                         errors="ignore")
        if table == "products":
            df = df.rename(columns={"product_name_lenght": "product_name_length",
                                    "product_description_lenght": "product_description_length"})
        df.to_sql(table, con, index=False)
        print(f"{table}: {len(df)} rows")
    for ddl in INDEXES:
        con.execute(ddl)
    con.commit()
    con.execute("VACUUM")
    con.close()
    print("Done ->", DB, f"{DB.stat().st_size / 1e6:.1f} MB")

if __name__ == "__main__":
    main()