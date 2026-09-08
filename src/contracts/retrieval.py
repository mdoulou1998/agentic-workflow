from typing import Optional, List, Literal
from pydantic import BaseModel, Field


class RetrievalInput(BaseModel):
    """Input for a retrieval request.

    Either `document_id` or `query_text` drives retrieval. `standard_id` can
    be supplied to scope the lookup to a known standard.
    """

    document_id: Optional[str] = None
    query_text: Optional[str] = None
    standard_id: Optional[str] = None
    max_results: int = 10


class KSB(BaseModel):
    """Representation of a single KSB (Knowledge / Skill / Behaviour).

    Includes a `source_locator` (file, URL, or standard section), an
    optional `confidence` score (0.0-1.0) and a ranking to allow stable
    downstream selection.
    """

    ksb_code: str
    category: Literal["knowledge", "skills", "behaviours"]
    description: str
    source_locator: Optional[str] = None
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0)
    rank: Optional[int] = None


class RetrievalOutput(BaseModel):
    """Output from a retrieval operation.

    Contains the selected standard metadata, the returned KSBs, and
    retrieval strategy metadata so runs are reproducible and auditable.
    """

    standard_id: Optional[str] = None
    standard_title: Optional[str] = None
    retrieved_ksbs: List[KSB] = Field(default_factory=list)
    retrieval_strategy: Optional[str] = None
    model_id: Optional[str] = None
    prompt_version: Optional[str] = None