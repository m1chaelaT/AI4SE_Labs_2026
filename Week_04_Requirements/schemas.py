"""Shared data structures for the requirements-refinement network.

Models whose name starts with "LLM" are the exact schemas the language models
must fill (structured output); all their fields are required so that OpenAI's
strict JSON-schema mode accepts them. Identifiers and tracing fields are added
afterwards in code, so the LLM can never invent a wrong source ID (OS4).
"""
from typing import Literal

from pydantic import BaseModel, Field


# --------------------------------------------------------------------------
# Loader
# --------------------------------------------------------------------------
class SourceDocument(BaseModel):
    """One input file from the corpus, identified by a stable ID (used for tracing, OS4)."""
    doc_id: str = Field(description="Stable document ID, e.g. 'D01'")
    path: str = Field(description="Path relative to the input directory")
    doc_type: str = Field(description="Coarse kind of document: email, meeting, interview, survey, specification, reference, other")
    title: str = Field(description="Subject line or first heading of the document")
    date: str | None = Field(default=None, description="Date found in the document header, if any")
    char_count: int
    text: str


class DocumentChunk(BaseModel):
    """A piece of a document small enough for one LLM extraction call."""
    chunk_id: str = Field(description="e.g. 'D03#2' (document D03, chunk 2)")
    doc_id: str
    index: int
    total: int
    text: str


# --------------------------------------------------------------------------
# Extractor
# --------------------------------------------------------------------------
RequirementType = Literal["functional", "non-functional", "constraint"]
RequirementStatus = Literal["proposed", "agreed", "disputed", "rejected"]


class LLMExtractedRequirement(BaseModel):
    """A candidate requirement as returned by the extractor LLM."""
    name: str = Field(description="Short descriptive name, 3-8 words, e.g. 'Inactive patrons report'")
    statement: str = Field(description="One sentence in the form 'The system shall ...'")
    details: str = Field(description="Supporting detail from the text: parameters, fields, examples, rationale. Empty string if none.")
    req_type: RequirementType = Field(description="functional = a capability; non-functional = a quality (performance, usability, security, accessibility...); constraint = a fixed technical or organisational limit")
    category: str = Field(description="Functional area, e.g. 'Circulation reports', 'Patron reports', 'Query tool', 'Security', 'Performance'")
    stakeholders: list[str] = Field(description="People or roles who asked for or supported it, as named in the text")
    priority_signals: list[str] = Field(description="Verbatim wording indicating importance, e.g. 'CRITICAL', 'must', 'nice to have', '78% of respondents'. Empty list if none.")
    status: RequirementStatus = Field(description="proposed = raised; agreed = explicitly accepted or decided; disputed = someone objected or there is disagreement; rejected = explicitly turned down")
    status_note: str = Field(description="Who objected/decided and why, if status is not 'proposed'. Empty string otherwise.")
    quote: str = Field(description="Short verbatim excerpt (max ~300 characters) from the text that supports this requirement")


class LLMIgnoredStatement(BaseModel):
    """Something that looks like a request but is not a requirement for the system."""
    text: str = Field(description="Short verbatim excerpt of the ignored statement")
    reason: Literal["off-topic", "existing-functionality", "not-a-requirement", "unclear"] = Field(
        description="off-topic = personal chatter unrelated to the system; existing-functionality = describes what the current system already does; not-a-requirement = question, opinion or fact without a need; unclear = too vague to use")
    explanation: str = Field(description="One sentence explaining why it was ignored")


class LLMExtractionResult(BaseModel):
    """Full extractor output for one chunk."""
    requirements: list[LLMExtractedRequirement]
    ignored: list[LLMIgnoredStatement]


class CandidateRequirement(LLMExtractedRequirement):
    """An extracted requirement enriched with IDs and tracing by deterministic code."""
    candidate_id: str = Field(description="e.g. 'C001'")
    doc_id: str
    chunk_id: str
    quote_verified: bool = Field(description="True if the quote was found in the source chunk (guards against hallucination)")


class IgnoredStatement(LLMIgnoredStatement):
    """An ignored statement with its source, kept for the blacklist section (OS9)."""
    doc_id: str
    chunk_id: str


class ExtractionError(BaseModel):
    """A chunk whose extraction failed even after retrying (reported, never silently dropped - OS8)."""
    chunk_id: str
    error: str


# --------------------------------------------------------------------------
# Merger
# --------------------------------------------------------------------------
class LLMArea(BaseModel):
    name: str = Field(description="Canonical functional area name, e.g. 'Circulation reports'")
    description: str = Field(description="One sentence describing what belongs to this area")


class LLMCategoryMapping(BaseModel):
    raw_category: str = Field(description="A category string exactly as given in the input")
    area: str = Field(description="The canonical area name it belongs to (must be one of 'areas')")


class LLMGlossaryTerm(BaseModel):
    term: str = Field(description="Preferred term to use in all requirements, e.g. 'staff user'")
    definition: str = Field(description="Short definition")
    avoid: list[str] = Field(description="Synonyms that should be replaced by the preferred term")


class LLMTaxonomy(BaseModel):
    areas: list[LLMArea]
    mapping: list[LLMCategoryMapping]
    glossary: list[LLMGlossaryTerm]


class LLMMergedRequirement(BaseModel):
    name: str = Field(description="Short descriptive name, 3-8 words")
    statement: str = Field(description="One sentence: 'The system shall ...'")
    description: str = Field(description="One paragraph (3-6 sentences): what is needed, who needs it and why, key parameters and details combined from all sources")
    req_type: RequirementType
    source_candidate_ids: list[str] = Field(description="IDs of ALL candidates merged into this requirement, e.g. ['C012', 'C140']")
    priority_signals: list[str] = Field(description="Union of the verbatim priority signals of the merged candidates")
    conflict_note: str = Field(description="If this requirement seems to contradict another candidate, describe it; otherwise empty string")


class LLMDiscardedCandidate(BaseModel):
    candidate_id: str
    reason: Literal["not-a-requirement", "nonsensical", "off-topic", "too-vague"]
    explanation: str = Field(description="One sentence explaining why it is discarded")


class LLMAreaMergeResult(BaseModel):
    requirements: list[LLMMergedRequirement]
    discarded: list[LLMDiscardedCandidate]


class LLMDuplicateGroup(BaseModel):
    ids: list[str] = Field(description="IDs (e.g. 'M004', 'M087') of 2 or more requirements that describe the same need")
    name: str
    statement: str
    description: str = Field(description="One merged paragraph combining the details of all requirements in the group")
    req_type: RequirementType


class LLMDedupResult(BaseModel):
    groups: list[LLMDuplicateGroup]


class Evidence(BaseModel):
    candidate_id: str
    doc_id: str
    quote: str
    quote_verified: bool


class MergedRequirement(BaseModel):
    """A deduplicated requirement. Tracing fields are computed in code from its candidates (OS4)."""
    merge_id: str = Field(description="Temporary ID, e.g. 'M001'; final IDs are assigned by the validator")
    area: str
    name: str
    statement: str
    description: str
    req_type: RequirementType
    source_candidate_ids: list[str]
    source_doc_ids: list[str]
    stakeholders: list[str]
    priority_signals: list[str]
    candidate_statuses: list[str] = Field(description="Status of each merged candidate, e.g. 'C012: agreed - decided at the July meeting'")
    conflict_notes: list[str]
    evidence: list[Evidence]
    resolution_notes: list[str] = Field(default_factory=list, description="How a conflict involving this requirement was resolved")
    priority: str | None = Field(default=None, description="MoSCoW priority: Must, Should, Could or Won't")
    priority_rationale: str = Field(default="", description="Why this priority was assigned")
    req_id: str = Field(default="", description="Final unique ID, e.g. 'REQ-001', assigned by the validator (OS2)")


class DiscardedCandidate(BaseModel):
    """A candidate removed during merging, kept for the blacklist section (OS9)."""
    candidate_id: str
    doc_id: str
    name: str
    statement: str
    reason: str
    explanation: str


class GlossaryTerm(LLMGlossaryTerm):
    pass


# --------------------------------------------------------------------------
# Conflict checker
# --------------------------------------------------------------------------
class LLMConflict(BaseModel):
    requirement_ids: list[str] = Field(description="IDs of the 2 or more requirements involved, e.g. ['M076', 'M229']")
    conflict_type: Literal["contradiction", "inconsistent-parameter", "incompatible-alternatives"] = Field(
        description="contradiction = one requires what another forbids; inconsistent-parameter = different values for the same thing; incompatible-alternatives = mutually exclusive solutions to the same need")
    description: str = Field(description="One or two sentences describing the conflict")
    keep_id: str = Field(description="ID of the requirement that is kept (possibly revised)")
    discard_ids: list[str] = Field(description="IDs of requirements removed because of this conflict; empty if the conflict is reconciled by revising the kept one")
    revised_statement: str = Field(description="New 'The system shall ...' statement for the kept requirement if it must change to resolve the conflict; empty string if unchanged")
    revised_description: str = Field(description="New one-paragraph description for the kept requirement if it changes; empty string if unchanged")
    rationale: str = Field(description="Why this resolution was chosen, referring to the sources (e.g. later decision, agreed status, technical constraint)")


class LLMInvalidRequirement(BaseModel):
    requirement_id: str
    reason: Literal["nonsensical", "out-of-scope", "not-a-system-requirement"] = Field(
        description="nonsensical = makes no sense or is internally contradictory; out-of-scope = not about the system being specified; not-a-system-requirement = a project task, process step or remark rather than something the system must do")
    explanation: str = Field(description="One sentence explaining why it is removed")


class LLMConflictResult(BaseModel):
    conflicts: list[LLMConflict]
    invalid: list[LLMInvalidRequirement]


class BlacklistEntry(BaseModel):
    """A requirement or candidate excluded from the final document, with the reason (OS9)."""
    source_id: str = Field(description="Merge ID (M###) or candidate ID (C###) of the excluded item")
    name: str
    statement: str
    source_doc_ids: list[str]
    category: str = Field(description="e.g. 'conflict', 'nonsensical', 'out-of-scope', 'too-vague', 'off-topic'")
    explanation: str
    conflicts_with: list[str] = Field(default_factory=list, description="Name of the kept requirement it conflicted with")
    source_candidate_ids: list[str] = Field(default_factory=list, description="Candidates behind the excluded item (keeps the coverage check exact)")


class ConflictRecord(BaseModel):
    """Log entry of a resolved conflict, for the report and the document."""
    requirement_ids: list[str]
    conflict_type: str
    description: str
    kept: str
    discarded: list[str]
    revised: bool
    rationale: str


# --------------------------------------------------------------------------
# Prioritiser
# --------------------------------------------------------------------------
Priority = Literal["Must", "Should", "Could", "Won't"]


class LLMPriorityAssignment(BaseModel):
    requirement_id: str
    priority: Priority
    justification: str = Field(description="One sentence referring to the evidence (signals, number of sources, decisions)")


class LLMPriorityResult(BaseModel):
    assignments: list[LLMPriorityAssignment]


# --------------------------------------------------------------------------
# Validator
# --------------------------------------------------------------------------
Responsible = Literal["extractor", "merger", "conflict_checker", "prioritizer", "none"]


class ValidationIssue(BaseModel):
    severity: Literal["error", "warning", "info"]
    check: str = Field(description="Short name of the check, e.g. 'missing-priority'")
    target: str = Field(description="Requirement ID, document ID or 'document'")
    message: str
    responsible: Responsible = Field(description="Node that should fix it (used by the reviewer to route feedback)")


class ValidationReport(BaseModel):
    passed: bool = Field(description="True if there are no errors (warnings are allowed)")
    issues: list[ValidationIssue]
    stats: dict[str, int]


# --------------------------------------------------------------------------
# Reviewer and reviser (feedback loop)
# --------------------------------------------------------------------------
class LLMReviewAction(BaseModel):
    action: Literal["merge", "rewrite", "change_priority", "remove"] = Field(
        description="merge = combine duplicates; rewrite = improve name/statement/description; change_priority = set new_priority; remove = move to the blacklist")
    requirement_ids: list[str] = Field(description="Final IDs, e.g. ['REQ-042', 'REQ-136']; merge needs 2 or more")
    new_priority: Literal["Must", "Should", "Could", "Won't", "none"] = Field(description="Only for change_priority; otherwise 'none'")
    instruction: str = Field(description="Precise instruction for the reviser, or the reason for a priority change or removal")


class LLMDismissal(BaseModel):
    issue_id: str = Field(description="ID of a validator warning, e.g. 'I7'")
    reason: str = Field(description="Why this warning is acceptable and needs no change")


class LLMReview(BaseModel):
    summary: str = Field(description="Two or three sentences on the overall quality of the specification")
    actions: list[LLMReviewAction]
    dismissed: list[LLMDismissal]


class LLMRevision(BaseModel):
    name: str = Field(description="Short descriptive name, 3-8 words")
    statement: str = Field(description="One sentence: 'The system shall ...'")
    description: str = Field(description="One paragraph of 3-6 sentences")
    req_type: RequirementType


class ReviewRound(BaseModel):
    """Log of one iteration of the feedback loop (for the report and the document)."""
    round: int
    errors: int
    warnings: int
    summary: str
    actions: list[str]
    dismissed: int
