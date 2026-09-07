from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl


class EvidenceDocument(BaseModel):
    id: str
    title: Optional[str]
    text: str
    source: Optional[HttpUrl]


class Claim(BaseModel):
    id: str
    document_id: str
    span: str
    start_char: int
    end_char: int


class Mapping(BaseModel):
    claim_id: str
    ksb_code: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    justification: Optional[str]


class Critique(BaseModel):
    mapping_claim_id: str
    issues: List[str]
    severity: Optional[str]
