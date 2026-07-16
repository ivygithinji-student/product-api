from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session, select, SQLModel, create_engine
from typing import List, Optional
from datetime import datetime

from models.product import Product, ProductCreate, ProductUpdate, Category, CategoryCreate

# ============================================
# DATABASE SETUP - SQLite
# ============================================
DATABASE_URL = "sqlite:///./products.db"
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

# Create tables (first time only)
SQLModel.metadata.create_all(engine)

app = FastAPI(
    title="Product Catalog API",
    description="A simple product catalog API with categories",
    version="1.0.0"
)

# ============================================
# ROOT ENDPOINT
# ============================================

@app.get("/")
def root():
    return {
        "message": "Welcome to the Product Catalog API",
        "endpoints": {
            "categories": "/categories",
            "products": "/products",
            "products_stats": "/products/stats",
            "products_search": "/products/search?q=keyword"
        }
    }

# ============================================
# CATEGORY CRUD
# ============================================

@app.post("/categories", response_model=Category, status_code=201)
def create_category(category: CategoryCreate, session: Session = Depends(get_session)):
    """Create a new category"""
    # Check if category already exists
    existing = session.exec(select(Category).where(Category.name == category.name)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")
    
    db_category = Category(**category.dict())
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category

@app.get("/categories", response_model=List[Category])
def list_categories(session: Session = Depends(get_session)):
    """List all categories"""
    return session.exec(select(Category)).all()

# ============================================
# PRODUCT CRUD
# ============================================

@app.post("/products", response_model=Product, status_code=201)
def create_product(product: ProductCreate, session: Session = Depends(get_session)):
    """Create a new product"""
    # Check if product with same name already exists
    existing = session.exec(select(Product).where(Product.name == product.name)).first()
    if existing:
        raise HTTPException(status_code=400, detail="A product with this name already exists")
    
    # Check if category exists (if category_id is provided)
    if product.category_id:
        category = session.get(Category, product.category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
    
    db_product = Product(**product.dict())
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

@app.get("/products", response_model=List[Product])
def list_products(
    skip: int = 0,
    limit: int = 10,
    category_id: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    session: Session = Depends(get_session)
):
    """List all products with optional filters"""
    query = select(Product)
    
    if category_id:
        query = query.where(Product.category_id == category_id)
    if min_price:
        query = query.where(Product.price >= min_price)
    if max_price:
        query = query.where(Product.price <= max_price)
    
    return session.exec(query.offset(skip).limit(limit)).all()

@app.get("/products/stats")
def get_product_stats(session: Session = Depends(get_session)):
    """Get statistics about products"""
    products = session.exec(select(Product)).all()
    
    if not products:
        return {
            "total_products": 0,
            "average_price": 0,
            "total_stock": 0,
            "most_expensive": None,
            "cheapest": None
        }
    
    prices = [p.price for p in products]
    
    return {
        "total_products": len(products),
        "average_price": round(sum(prices) / len(prices), 2),
        "total_stock": sum(p.stock for p in products),
        "most_expensive": max(products, key=lambda p: p.price).name,
        "cheapest": min(products, key=lambda p: p.price).name
    }

@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int, session: Session = Depends(get_session)):
    """Get a specific product by ID"""
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.patch("/products/{product_id}", response_model=Product)
def update_product(
    product_id: int,
    product_update: ProductUpdate,
    session: Session = Depends(get_session)
):
    """Partially update a product"""
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Update only the fields provided
    update_data = product_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)
    
    product.updated_at = datetime.utcnow()
    session.commit()
    session.refresh(product)
    return product

@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int, session: Session = Depends(get_session)):
    """Delete a product"""
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    session.delete(product)
    session.commit()
    return None

@app.get("/products/search", response_model=List[Product])
def search_products(q: str, session: Session = Depends(get_session)):
    """Search products by name or description"""
    query = select(Product).where(
        (Product.name.contains(q)) | (Product.description.contains(q))
    )
    return session.exec(query).all()