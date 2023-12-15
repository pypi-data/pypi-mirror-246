from fastapi import (
    APIRouter,
    Query,
    status, HTTPException
)
from starlette.requests import Request
from starlette.responses import JSONResponse

from .database_cows_functions import get_cows_by_field_from_db, get_cow_by_id_from_db, delete_cow_by_id_from_db, \
    is_unique_cow_in_db, create_cow_in_db, \
    update_cow_in_db
from .models import CowResponse, CowUpdate, CowCreate
from fastapi.encoders import jsonable_encoder

# initiate APIrouter for cow_api
router = APIRouter()


@router.get("/cows", response_model=list[CowResponse])
async def get_cows(
        request: Request,
        name: str = Query(None, description="Cow's name"),
        sex: str = Query(None, description="Cow's sex"),
        condition: str = Query(None, description="Cow's condition")
) -> list[CowResponse]:
    """Retrieve desired cows by name, sex or condition"""

    # initialize a dictionary that contains the fields to filter the cows by.
    filter_dict = {k: v for k, v in zip(["name", "sex", "condition"], [name, sex, condition]) 
                   if v is not None}
    if len(filter_dict) < 1:
        request.app.logger.info("retrieving cows...")
    else:
        request.app.logger.info("filtering and retrieving cows...")

    cows = await get_cows_by_field_from_db(request, filter_dict)

    request.app.logger.info(f"found {len(cows)} cows.")

    return cows


@router.post("/cows", response_model=CowResponse, status_code=status.HTTP_201_CREATED)
async def cows_post(request: Request, cow: CowCreate):
    """Add cow to farm."""
    cow = CowResponse(**cow.dict())
    cow = jsonable_encoder(cow)
    cow_dict = {"name": cow["name"], "sex": cow["sex"], "birthdate": cow["birthdate"]}

    request.app.logger.info("checking if cow exists in db...")    
    if await is_unique_cow_in_db(request, cow_dict):
        request.app.logger.info("creating cow...")
        new_cow = await create_cow_in_db(request, cow)
    else:
        request.app.logger.error("cow already exists in db.")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Cow already exists")
    
    created_cow = await get_cow_by_id_from_db(request, new_cow.inserted_id)
    request.app.logger.info(f"cow {created_cow['name']}  created in db successfully.")

    return created_cow


@router.get("/cows/{id}", response_model=CowResponse)
async def get_cow(request: Request, id: str) -> CowResponse:
    """Get Cow by id."""

    request.app.logger.info(f"Get Cow by id = {id}")
    cow = await get_cow_by_id_from_db(request, id)
    if cow is not None:
        request.app.logger.info(f"found cow {id}")
        return cow
    request.app.logger.error(f"cow {id} not found")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"cow {id} not found")


@router.put("/cows/{id}", status_code=status.HTTP_200_OK, response_model=CowResponse)
async def cows_put(request: Request, id: str, cow_model: CowUpdate) -> CowResponse:
    """Updates cow's details."""

    request.app.logger.info(f"updating cow {id}")
    # exclude unset values from cow_model in order to update only the fields that are supposed to be updated.
    update_fields_dict = cow_model.dict(exclude_unset=True)
    # if the dictionary is of length over 0 then user provided fields to update the cow.
    if len(update_fields_dict) > 0:
        update_result = await update_cow_in_db(request, id, update_fields_dict)

        # if there is a cow of the provided id then the value of modified_count should be 1.
        if update_result.modified_count == 1:
            if (updated_cow := await get_cow_by_id_from_db(request, id)) is not None:
                request.app.logger.info(f"updated cow {id} successfully.")
                return updated_cow
    elif (existing_cow := await get_cow_by_id_from_db(request, id)) is not None:
        return existing_cow
    request.app.logger.error(f"Cow {id} not found.")
    raise HTTPException(status_code=404, detail=f"Cow {id} not found.")


@router.delete("/cows/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def cows_id_delete(request: Request, id: str):
    """Delete cow from farm."""
    request.app.logger.info(f"Deleting cow {id}")
    delete_result = await delete_cow_by_id_from_db(request, id)

    if delete_result.deleted_count == 1:
        request.app.logger.info(f"Deleted cow {id} successfully.")
        return JSONResponse(content=f"Cow {id} Deleted!", status_code=status.HTTP_204_NO_CONTENT)
    request.app.logger.error(f"Cow {id} not found.")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Cow {id} not found!")
