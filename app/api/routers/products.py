from fastapi import APIRouter, Depends, HTTPException, Query, Path, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database.session import get_db
from app.models.product import Product
from app.schemas.product_schema import ProductCreate, ProductUpdate, ProductResponse
from app.core.exceptions import ProductNotFoundException

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=List[ProductResponse])
def get_products(
    skip: int = Query(0, ge=0, description="Skip elements for pagination"),
    limit: int = Query(10, le=100, description="Limit result size"),
    db: Session = Depends(get_db)
):
    """
    WHY: Fetch list of products.
    HOW: Uses Query parameters for pagination and Sync DB retrieval.
    """
    return db.query(Product).offset(skip).limit(limit).all()

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int = Path(..., title="The ID of the product to get", ge=1),
    db: Session = Depends(get_db)
):
    """
    WHY: Fetch a single product by ID.
    HOW: Demonstrates Path parameters validation. Raises Custom Exception.
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise ProductNotFoundException(product_id=product_id)
    return product

@router.post("/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """
    WHY: Create a new product.
    HOW: Uses POST and Pydantic validation via ProductCreate.
    """
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.put("/{product_id}", response_model=ProductResponse)
def update_product_totally(product_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    """
    WHY: Completely replace a product.
    HOW: Uses PUT method.
    """
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise ProductNotFoundException(product_id=product_id)
    for key, value in product.model_dump().items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.patch("/{product_id}", response_model=ProductResponse)
def patch_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    """
    WHY: Partially update a product.
    HOW: Uses PATCH method and conditional field updates.
    """
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise ProductNotFoundException(product_id=product_id)
    
    update_data = product.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product

@router.post("/{product_id}/image")
async def upload_product_image(product_id: int, file: UploadFile = File(...)):
    """
    WHY: Allow merchants to upload product images.
    HOW: Demonstrates File Upload feature. Reads file async.
    """
    contents = await file.read()
    # In reality, save file to S3 or local storage
    return {"filename": file.filename, "file_size": len(contents), "status": "Uploaded successfully"}
