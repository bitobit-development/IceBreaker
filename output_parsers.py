from typing import List, Dict, Any

from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field


class Summary(BaseModel):
    """Pydantic model for person summary with interesting facts."""
    summary: str = Field(description="summary")
    facts: List[str] = Field(description="interesting facts about them")

    def to_dict(self) -> Dict[str, Any]:
        """Convert the Summary object to a dictionary.

        Returns:
            Dict[str, Any]: Dictionary with 'summary' and 'facts' keys.
        """
        return {"summary": self.summary, "facts": self.facts}


class IceBreaker(BaseModel):
    """Pydantic model for conversation ice breakers."""
    ice_breakers: List[str] = Field(description="ice breaker list")

    def to_dict(self) -> Dict[str, Any]:
        """Convert the IceBreaker object to a dictionary.

        Returns:
            Dict[str, Any]: Dictionary with 'ice_breakers' key.
        """
        return {"ice_breakers": self.ice_breakers}


class TopicOfInterest(BaseModel):
    """Pydantic model for topics that might interest a person."""
    topics_of_interest: List[str] = Field(
        description="topic that might interest the person"
    )

    def to_dict(self) -> Dict[str, Any]:
        """Convert the TopicOfInterest object to a dictionary.

        Returns:
            Dict[str, Any]: Dictionary with 'topics_of_interest' key.
        """
        return {"topics_of_interest": self.topics_of_interest}


summary_parser = PydanticOutputParser(pydantic_object=Summary)
ice_breaker_parser = PydanticOutputParser(pydantic_object=IceBreaker)
topics_of_interest_parser = PydanticOutputParser(pydantic_object=TopicOfInterest)
