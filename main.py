import uuid
from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session, joinedload

from engenharia_zero import models, schemas, database
from security import auth

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)
) -> models.UserTable:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # 1. Decode the Token
    token_data = auth.decode_access_token(
        token
    )  # Using the function from 'security/auth.py'
    if token_data is None or "sub" not in token_data:
        raise credentials_exception

    # 2. Searches for the user by the UUID that is in the 'sub'
    try:
        user_uuid_id = uuid.UUID(token_data["sub"])
    except ValueError, AttributeError:
        raise credentials_exception

    user = (
        db.query(models.UserTable)
        .filter(models.UserTable.user_uuid_id == user_uuid_id)
        .first()
    )

    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Usuário inativo"
        )

    return user


async def admin_only(
    current_user: models.UserTable = Depends(get_current_user),
) -> models.UserTable:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a administradores",
        )
    return current_user


async def authorize_user_access(
    user_id: int, current_user: models.UserTable = Depends(get_current_user)
) -> models.UserTable:
    if not current_user.is_admin and current_user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado: permissão insuficiente",
        )
    return current_user


@app.get("/")
def read_root():
    return {"message": "Engenharia Zero API ativa e conectada ao banco"}


@app.get("/user/me", response_model=schemas.User)
def read_user_me(
    current_user: models.UserTable = Depends(get_current_user),
) -> models.UserTable:
    return current_user


@app.get("/users/", response_model=list[schemas.User])
def read_users(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(database.get_db),
    _: models.UserTable = Depends(admin_only),  # Protected Route!
) -> List[models.UserTable]:
    # The .offset(skip) option skips records (page 2, 3...)
    # The .limit(limit) option ensures that you don't crash the server with too much data
    users = db.query(models.UserTable).offset(skip).limit(limit).all()
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user_detail(
    user_id: int,
    db: Session = Depends(database.get_db),
    _: models.UserTable = Depends(authorize_user_access),
) -> models.UserTable:
    user = (
        db.query(models.UserTable).filter(models.UserTable.user_id == user_id).first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado"
        )
    return user


@app.get("/products/", response_model=list[schemas.Product])
def read_products(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(database.get_db),
    current_user: models.UserTable = Depends(get_current_user),  # Protected Route!
) -> List[models.ProductTable]:
    # The .offset(skip) option skips records (page 2, 3...)
    # The .limit(limit) option ensures that you don't crash the server with too much data
    products = db.query(models.ProductTable).offset(skip).limit(limit).all()
    return products


@app.get("/invoices/", response_model=list[schemas.Invoice])
def read_invoices(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(database.get_db),
    current_user: models.UserTable = Depends(get_current_user),  # Protected Route!
) -> List[models.InvoiceTable]:
    query = db.query(models.InvoiceTable).options(
        joinedload(models.InvoiceTable.items).joinedload(  # Load the items
            models.InvoiceItemTable.product
        )  # Load the product for each item
    )

    # Checks if the user is an administrator; if not,
    # they will only see their own invoices
    if not current_user.is_admin:
        query = query.filter(models.InvoiceTable.user_id == current_user.user_id)

    # The .offset(skip) option skips records (page 2, 3...)
    # The .limit(limit) option ensures that you don't crash the server with too much data
    invoices = query.offset(skip).limit(limit).all()
    return invoices


@app.get("/invoices/{invoice_id}", response_model=schemas.Invoice)
def read_invoice(
    invoice_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.UserTable = Depends(get_current_user),  # Protected Route!
) -> models.InvoiceTable:
    # .filter(models.InvoiceTable.id == invoice_id) is our WHERE clause where id = ?
    # .first() returns the object or None if nothing is found
    invoice = (
        db.query(models.InvoiceTable)
        .filter(models.InvoiceTable.invoice_id == invoice_id)
        .first()
    )

    if invoice is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Fatura não encontrada"
        )

    # Protection: If you're not the administrator and you're not the owner of invoice, goodbye!
    if not current_user.is_admin and invoice.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Acesso à fatura negado"
        )

    return invoice


@app.post("/auth/login", response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
) -> schemas.Token:
    # 1. Searches for the user by email (which OAuth2 calls 'username')
    user = (
        db.query(models.UserTable)
        .filter(models.UserTable.email == form_data.username)
        .first()
    )

    # 2. Valida a existência e senha
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
            headers={"WW-Authenticate": "Bearer"},
        )

    # 3. We create the token payload (we use 'user_uuid_id' as 'sub')
    # O 'sub' (subject) is a standard JWT claim to identify the subject
    access_token = auth.create_access_token(data={"sub": str(user.user_uuid_id)})

    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(database.get_db),
    _: models.UserTable = Depends(admin_only),  # Protected Route!
) -> models.UserTable:
    # Business Rule Verification: unique e-mail
    db_user = (
        db.query(models.UserTable).filter(models.UserTable.email == user.email).first()
    )
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail já cadastrado no sistema",
        )

    # Transforms the plaintext password into a secure hash
    # 'user.password' comes from the UserCreate schema
    secure_hash = auth.get_password_hash(user.password)

    # Conversion: Pydantic -> SQLAchemy
    new_user = models.UserTable(
        name=user.name,
        email=user.email,
        birth_date=user.birth_date,
        telephone=user.telephone,
        hashed_password=secure_hash,
        # is_admin will be False by default
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # Update the object with the ID generated by the data base
    return new_user


@app.post("/products/", response_model=schemas.Product)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(database.get_db),
    _: models.UserTable = Depends(admin_only),  # Protected Route!
) -> models.ProductTable:
    new_product = models.ProductTable(**product.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@app.post("/invoices/", response_model=schemas.Invoice)
def create_invoice(
    invoice_data: schemas.InvoiceCreate,
    db: Session = Depends(database.get_db),
    current_user: models.UserTable = Depends(get_current_user),  # Protected Route!
) -> models.InvoiceTable:
    try:
        # 1. Validates if the user exists before start
        user_exists = (
            db.query(models.UserTable)
            .filter(models.UserTable.user_uuid_id == invoice_data.user_uuid_id)
            .first()
        )
        if not user_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado"
            )

        # Protection: The common user cannot create invoices for others
        if not current_user.is_admin and user_exists.user_id != current_user.user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você só pode criar faturas para si mesmo",
            )

        # 2. Create the Invoice (Header)
        new_invoice = models.InvoiceTable(
            user_id=user_exists.user_id, user_uuid_id=user_exists.user_uuid_id
        )
        db.add(new_invoice)
        db.flush()  # Ensure we have the new_invoice.id

        # 3. Create the Items (Body)
        for item in invoice_data.items:
            # Validates if the product exists
            product_exists = (
                db.query(models.ProductTable)
                .filter(models.ProductTable.product_id == item.product_id)
                .first()
            )
            if not product_exists:
                db.rollback()  # Cancel EVERYTHING that was done above
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Produto {item.product_id} não existe",
                )

            db_item = models.InvoiceItemTable(
                invoice_id=new_invoice.invoice_id,
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=product_exists.price,  # Here we save the current price!
            )
            db.add(db_item)

        # 4. Final Commit (Only gets here if everything went well)
        db.commit()
        db.refresh(new_invoice)
        return new_invoice

    except Exception as e:
        db.rollback()  # Extra security for any unexpected errors
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao processar fatura",
        )
