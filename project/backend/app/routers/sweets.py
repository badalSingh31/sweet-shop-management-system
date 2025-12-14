from fastapi import APIRouter, Depends, HTTPException, status, Query
from supabase import Client
from typing import List, Optional
from decimal import Decimal
from app.database import get_supabase_client
from app.models import (
    SweetCreate, SweetUpdate, SweetResponse,
    PurchaseRequest, RestockRequest, PurchaseResponse
)
from app.auth import get_current_user, get_current_admin_user

router = APIRouter(prefix="/api/sweets", tags=["sweets"])


@router.get("", response_model=List[SweetResponse])
async def get_all_sweets(
    current_user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase_client)
):
    try:
        response = supabase.table("sweets").select("*").order("created_at", desc=True).execute()
        return response.data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch sweets: {str(e)}"
        )


@router.get("/search", response_model=List[SweetResponse])
async def search_sweets(
    name: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    min_price: Optional[Decimal] = Query(None),
    max_price: Optional[Decimal] = Query(None),
    current_user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase_client)
):
    try:
        query = supabase.table("sweets").select("*")

        if name:
            query = query.ilike("name", f"%{name}%")

        if category:
            query = query.eq("category", category)

        if min_price is not None:
            query = query.gte("price", float(min_price))

        if max_price is not None:
            query = query.lte("price", float(max_price))

        response = query.order("created_at", desc=True).execute()
        return response.data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {str(e)}"
        )


@router.post("", response_model=SweetResponse, status_code=status.HTTP_201_CREATED)
async def create_sweet(
    sweet_data: SweetCreate,
    current_user: dict = Depends(get_current_admin_user),
    supabase: Client = Depends(get_supabase_client)
):
    try:
        sweet_dict = sweet_data.model_dump()
        sweet_dict["price"] = float(sweet_dict["price"])

        response = supabase.table("sweets").insert(sweet_dict).execute()

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create sweet"
            )

        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create sweet: {str(e)}"
        )


@router.put("/{sweet_id}", response_model=SweetResponse)
async def update_sweet(
    sweet_id: str,
    sweet_data: SweetUpdate,
    current_user: dict = Depends(get_current_admin_user),
    supabase: Client = Depends(get_supabase_client)
):
    try:
        update_dict = sweet_data.model_dump(exclude_unset=True)

        if "price" in update_dict:
            update_dict["price"] = float(update_dict["price"])

        if not update_dict:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields to update"
            )

        response = supabase.table("sweets").update(update_dict).eq("id", sweet_id).execute()

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sweet not found"
            )

        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update sweet: {str(e)}"
        )


@router.delete("/{sweet_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_sweet(
    sweet_id: str,
    current_user: dict = Depends(get_current_admin_user),
    supabase: Client = Depends(get_supabase_client)
):
    try:
        response = supabase.table("sweets").delete().eq("id", sweet_id).execute()

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sweet not found"
            )

        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete sweet: {str(e)}"
        )


@router.post("/{sweet_id}/purchase", response_model=PurchaseResponse)
async def purchase_sweet(
    sweet_id: str,
    purchase_data: PurchaseRequest,
    current_user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase_client)
):
    try:
        sweet_response = supabase.table("sweets").select("*").eq("id", sweet_id).maybeSingle().execute()

        if not sweet_response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sweet not found"
            )

        sweet = sweet_response.data

        if sweet["quantity"] < purchase_data.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Not enough stock. Available: {sweet['quantity']}"
            )

        total_price = float(sweet["price"]) * purchase_data.quantity

        new_quantity = sweet["quantity"] - purchase_data.quantity
        supabase.table("sweets").update({"quantity": new_quantity}).eq("id", sweet_id).execute()

        purchase_dict = {
            "user_id": current_user["id"],
            "sweet_id": sweet_id,
            "quantity": purchase_data.quantity,
            "total_price": total_price
        }

        purchase_response = supabase.table("purchases").insert(purchase_dict).execute()

        if not purchase_response.data:
            supabase.table("sweets").update({"quantity": sweet["quantity"]}).eq("id", sweet_id).execute()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Purchase failed"
            )

        return purchase_response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Purchase failed: {str(e)}"
        )


@router.post("/{sweet_id}/restock", response_model=SweetResponse)
async def restock_sweet(
    sweet_id: str,
    restock_data: RestockRequest,
    current_user: dict = Depends(get_current_admin_user),
    supabase: Client = Depends(get_supabase_client)
):
    try:
        sweet_response = supabase.table("sweets").select("*").eq("id", sweet_id).maybeSingle().execute()

        if not sweet_response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sweet not found"
            )

        sweet = sweet_response.data
        new_quantity = sweet["quantity"] + restock_data.quantity

        update_response = supabase.table("sweets").update({"quantity": new_quantity}).eq("id", sweet_id).execute()

        if not update_response.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Restock failed"
            )

        return update_response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Restock failed: {str(e)}"
        )
