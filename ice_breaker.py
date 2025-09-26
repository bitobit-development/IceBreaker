from typing import Tuple
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from agents.twitter_lookup_agent import lookup as twitter_lookup_agent
from chains.custom_chains import (
    get_summary_chain,
    get_interests_chain,
    get_ice_breaker_chain,
)
from third_parties.linkedin import scrape_linkedin_profile
from third_parties.twitter import scrape_user_tweets, scrape_user_tweets_mock
from output_parsers import (
    Summary,
    IceBreaker,
    TopicOfInterest,
)


def ice_break_with(
    name: str,
) -> Tuple[Summary, TopicOfInterest, IceBreaker, str]:
    """Generate ice breaker content for a person based on their social media profiles.

    This function orchestrates the entire pipeline:
    1. Looks up LinkedIn and Twitter profiles for the given name
    2. Scrapes data from both platforms
    3. Generates a summary with facts
    4. Identifies topics of interest
    5. Creates personalized ice breakers

    Args:
        name (str): Full name of the person to research.

    Returns:
        Tuple[Summary, TopicOfInterest, IceBreaker, str]: A tuple containing:
            - Summary object with profile summary and interesting facts
            - TopicOfInterest object with topics that might interest the person
            - IceBreaker object with conversation starters
            - Profile picture URL string from LinkedIn
    """
    linkedin_url = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_url)

    twitter_username = twitter_lookup_agent(name=name)
    tweets = scrape_user_tweets_mock(username=twitter_username)

    summary_chain = get_summary_chain()
    summary_and_facts: Summary = summary_chain.invoke(
        input={"information": linkedin_data, "twitter_posts": tweets},
    )

    interests_chain = get_interests_chain()
    interests: TopicOfInterest = interests_chain.invoke(
        input={"information": linkedin_data, "twitter_posts": tweets}
    )

    ice_breaker_chain = get_ice_breaker_chain()
    ice_breakers: IceBreaker = ice_breaker_chain.invoke(
        input={"information": linkedin_data, "twitter_posts": tweets}
    )

    return (
        summary_and_facts,
        interests,
        ice_breakers,
        linkedin_data.get("photoUrl"),
    )


if __name__ == "__main__":
    pass
