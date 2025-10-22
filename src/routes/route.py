from datetime import datetime
from typing import Optional
from fastapi import APIRouter, HTTPException, Query, status
from src.services.string_analysis import analyze_string, sha256_hash
from src.services.nlp_filter import filter_nlp
from src.models.string_models import TextResponseModel, TextBaseModel
from src.models.db import string_collection


router = APIRouter(prefix='/strings', tags=['Strings'])


@router.post('', response_model=TextResponseModel, status_code=status.HTTP_201_CREATED)
def string_analysis(input: TextBaseModel):

    # Check if the value is provided in input
    if not input.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid request body or missing "value" field'
        )

    # Check if the value provided is a string
    if not isinstance(input.value, str):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Invalid data type for "value" (must be string)'
        )

    # Analyze the text and check if the hash already exists
    analysis_result = analyze_string(input.value)
    hash_id = analysis_result.sha256_hash
    existing_text = string_collection.find_one({'id': hash_id})

    if existing_text:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='String already exists in the system'
        )

    # Insert the analysis result into the database
    response = TextResponseModel(
        id=analysis_result.sha256_hash,
        value=input.value,
        properties=analysis_result,
        created_at=datetime.utcnow().isoformat()+"Z"
    )
    string_collection.insert_one(response.model_dump())

    return response


@router.get('', status_code=status.HTTP_200_OK)
def get_all_strings_filtered(
    is_palindrome: Optional[bool] = Query(None),
    min_length: Optional[int] = Query(None),
    max_length: Optional[int] = Query(None),
    word_count: Optional[int] = Query(None),
    contains_character: Optional[str] = Query(None)
):
    # Format the database query
    try:
        query = {}

        if is_palindrome is not None:
            query["properties.is_palindrome"] = is_palindrome
        if min_length is not None:
            query["properties.length"] = {"$gte": min_length}
        if max_length is not None:
            query.setdefault("properties.length", {}).update(
                {"$lte": max_length})
        if word_count is not None:
            query["properties.word_count"] = word_count
        if contains_character:
            query["value"] = {"$regex": contains_character, "$options": "i"}

        # Perform the query
        results = list(string_collection.find(query, {"_id": 0}))
        return {
            "data": results,
            "count": len(results),
            "filters_applied": {
                "is_palindrome": is_palindrome,
                "min_length": min_length,
                "max_length": max_length,
                "word_count": word_count,
                "contains_character": contains_character
            }
        }

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid query parameter values or types'
        )


@router.get('/filter-by-natural-language', status_code=status.HTTP_200_OK)
def filter_by_natural_language(query: str = Query(...)):

    try:
        # try to perform NLP processing
        filters = filter_nlp(query)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(e)
        )

    # Format the database query
    mongo_query = {}
    if "is_palindrome" in filters:
        mongo_query["properties.is_palindrome"] = filters["is_palindrome"]
    if "word_count" in filters:
        mongo_query["properties.word_count"] = filters["word_count"]
    if "min_length" in filters:
        mongo_query["properties.length"] = {"$gte": filters["min_length"]}
    if "contains_character" in filters:
        mongo_query["value"] = {
            "$regex": filters["contains_character"], "$options": "i"}

    # Perform the query
    results = list(string_collection.find(mongo_query, {"_id": 0}))

    return {
        "data": results,
        "count": len(results),
        "interpreted_query": {
            "original": query,
            "parsed_filters": filters,
        }
    }


@router.get('/{string_value}', response_model=TextResponseModel, status_code=status.HTTP_200_OK)
def get_specific_string(string_value: str):
    # Hash the input and check if it exists
    text_hash = sha256_hash(string_value)
    existing_text = string_collection.find_one({'id': text_hash})

    # raise and error if response not found
    if not existing_text:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='String does not exist in the system'
        )
    return existing_text


@router.delete('/{string_value}', status_code=status.HTTP_204_NO_CONTENT)
def delete_string(string_value: str):
    # Hash the text and check if it exists
    text_hash = sha256_hash(string_value)
    existing_text = string_collection.find_one({'id': text_hash})

    if not existing_text:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='String does not exist in the system'
        )

    # delete the string
    string_collection.delete_one(existing_text)
