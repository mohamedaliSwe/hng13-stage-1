"""Contain the String Model"""
from pydantic import BaseModel
from typing import Dict


class TextBaseModel(BaseModel):
    id: str | None = None
    value: str


class TextAnalysisModel(BaseModel):
    length: int
    is_palindrome: bool
    unique_characters: int
    word_count: int
    sha256_hash: str
    character_frequency_map: Dict[str, int]


class TextResponseModel(TextBaseModel):
    properties: TextAnalysisModel
    created_at: str
