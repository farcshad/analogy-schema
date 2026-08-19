from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class Sentence(BaseModel):
    sentence_id: int
    text: str
    char_start: int
    char_end: int


class StoryInput(BaseModel):
    """Anonymous LLM-facing story representation with zero metadata or benchmark labels."""
    story_id: str
    text: str
    sentences: List[Sentence] = Field(default_factory=list)


class Story(BaseModel):
    story_id: str
    title: Optional[str] = None
    text: str
    sentences: List[Sentence] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def from_text(cls, story_id: str, text: str, title: Optional[str] = None, metadata: Optional[dict] = None) -> "Story":
        import re
        text_clean = text.strip()
        raw_sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text_clean) if s.strip()]
        sentences = []
        curr_idx = 0
        for i, s in enumerate(raw_sentences, start=1):
            char_start = text_clean.find(s, curr_idx)
            if char_start == -1:
                char_start = curr_idx
            char_end = char_start + len(s)
            curr_idx = char_end
            sentences.append(Sentence(sentence_id=i, text=s, char_start=char_start, char_end=char_end))
        
        return cls(
            story_id=story_id,
            title=title,
            text=text_clean,
            sentences=sentences,
            metadata=metadata or {}
        )

    def to_llm_input(self, anonymous_id: Optional[str] = None) -> StoryInput:
        """Strips all titles, filenames, and metadata to eliminate ground-truth leakage."""
        return StoryInput(
            story_id=anonymous_id or self.story_id,
            text=self.text,
            sentences=self.sentences
        )
