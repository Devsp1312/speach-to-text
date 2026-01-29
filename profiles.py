"""
User Profiling System

Generates anonymous user profiles from interest scores.
Profiles reset daily and include social style, activity preferences, and personalized suggestions.
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class UserProfile:
    """Represents an anonymous user profile."""
    core_interests: List[str]  # Top 3 interests
    secondary_interests: List[str]  # Next tier of interests
    social_style: str  # introverted, balanced, extroverted
    activity_preference: str  # solo, small group, large group
    reasoning: str  # Explanation of profile derivation
    suggestions: List[str]  # 3 personalized suggestions


# Mapping of interest categories to social characteristics
SOCIAL_INDICATORS = {
    "Tech/Engineering": {"social": -1, "activity": 0},  # More solo-oriented
    "Academics/School": {"social": 0, "activity": -0.5},  # Neutral, somewhat solo
    "Career/Jobs": {"social": 1, "activity": 0},  # Networking-oriented
    "Sports/Fitness": {"social": 0, "activity": 0},  # Balanced
    "Food": {"social": 1, "activity": 0.5},  # Social, group-oriented
    "Social/People": {"social": 2, "activity": 1},  # Highly social, group-oriented
    "Entertainment/Gaming": {"social": 0, "activity": -0.5},  # Mixed, can be solo
}

# Suggestion templates for each interest category
SUGGESTION_TEMPLATES = {
    "Tech/Engineering": [
        "Attend a coding meetup or hackathon this week",
        "Start a small side project using a language you've wanted to learn",
        "Join an online tech community or Discord server for your interests",
    ],
    "Academics/School": [
        "Form a study group for an upcoming exam",
        "Attend office hours to discuss challenging concepts",
        "Work on a project with a classmate for collaborative learning",
    ],
    "Career/Jobs": [
        "Update your LinkedIn profile and reach out to 2-3 professionals in your field",
        "Attend a career fair or industry networking event",
        "Schedule coffee chats with people in roles you aspire to",
    ],
    "Sports/Fitness": [
        "Try a new fitness class at your gym or campus",
        "Invite a friend for a workout or sports activity",
        "Join an intramural team or casual sports group",
    ],
    "Food": [
        "Try a new restaurant with friends this week",
        "Cook a meal with roommates or classmates",
        "Attend a food-focused event or tasting on campus",
    ],
    "Social/People": [
        "Plan a hangout with friends you haven't seen recently",
        "Attend a social event or party happening on campus",
        "Start a group chat for a shared interest or hobby",
    ],
    "Entertainment/Gaming": [
        "Join a gaming session with friends online or in-person",
        "Attend a gaming event or tournament",
        "Watch the latest movie/show with a small group",
    ],
}


def determine_social_style(scores: Dict[str, float]) -> Tuple[str, float]:
    """
    Determine social style based on interest scores.
    
    Args:
        scores: Dictionary of interest categories and their percentage scores
    
    Returns:
        Tuple of (social_style, confidence_score)
    """
    social_score = 0.0
    total_weight = 0.0
    
    for category, score in scores.items():
        if category in SOCIAL_INDICATORS:
            weight = score / 100  # Normalize by percentage
            social_indicator = SOCIAL_INDICATORS[category]["social"]
            social_score += social_indicator * weight
            total_weight += weight
    
    # Normalize the social score
    if total_weight > 0:
        social_score = social_score / total_weight
    
    # Classify into social style
    if social_score < -0.5:
        style = "Introverted"
    elif social_score > 0.5:
        style = "Extroverted"
    else:
        style = "Balanced"
    
    confidence = min(abs(social_score), 1.0)  # Confidence between 0-1
    return style, confidence


def determine_activity_preference(scores: Dict[str, float]) -> Tuple[str, float]:
    """
    Determine activity preference (solo, small group, large group).
    
    Args:
        scores: Dictionary of interest categories and their percentage scores
    
    Returns:
        Tuple of (activity_preference, confidence_score)
    """
    activity_score = 0.0
    total_weight = 0.0
    
    for category, score in scores.items():
        if category in SOCIAL_INDICATORS:
            weight = score / 100
            activity_indicator = SOCIAL_INDICATORS[category]["activity"]
            activity_score += activity_indicator * weight
            total_weight += weight
    
    # Normalize the activity score
    if total_weight > 0:
        activity_score = activity_score / total_weight
    
    # Classify into activity preference
    if activity_score < -0.3:
        preference = "Solo activities"
    elif activity_score > 0.3:
        preference = "Large group activities"
    else:
        preference = "Small group activities"
    
    confidence = min(abs(activity_score), 1.0)
    return preference, confidence


def generate_suggestions(
    interests: List[str],
    scores: Dict[str, float],
    social_style: str,
    num_suggestions: int = 3
) -> List[str]:
    """
    Generate personalized suggestions based on interests and profile.
    
    Args:
        interests: List of top interest categories
        scores: Dictionary of interest scores
        social_style: The determined social style
        num_suggestions: Number of suggestions to generate (default 3)
    
    Returns:
        List of actionable suggestions
    """
    suggestions = []
    
    # Collect suggestions from top interests
    for interest in interests[:num_suggestions]:
        if interest in SUGGESTION_TEMPLATES:
            templates = SUGGESTION_TEMPLATES[interest]
            # Select template based on social style
            if social_style == "Introverted":
                # Prefer less social suggestions
                suggestion = templates[0] if len(templates) > 0 else templates[0]
            elif social_style == "Extroverted":
                # Prefer more social suggestions
                suggestion = templates[-1] if len(templates) > 1 else templates[0]
            else:
                # Balanced: pick middle suggestion
                suggestion = templates[len(templates) // 2]
            
            suggestions.append(suggestion)
    
    # Ensure we have enough suggestions
    while len(suggestions) < num_suggestions:
        suggestions.append("Explore a new activity that combines your interests")
    
    return suggestions[:num_suggestions]


def build_reasoning(
    core_interests: List[str],
    social_style: str,
    activity_preference: str,
    scores: Dict[str, float]
) -> str:
    """
    Build a reasoning explanation for the profile.
    
    Args:
        core_interests: Top 3 interest categories
        social_style: Determined social style
        activity_preference: Determined activity preference
        scores: Interest scores for context
    
    Returns:
        Explanation string
    """
    core_str = ", ".join(core_interests)
    top_score = max(scores.values()) if scores else 0
    
    reasoning = (
        f"Based on your transcribed content, your profile centers on {core_str}. "
        f"With '{core_interests[0]}' as your strongest interest ({top_score:.1f}%), "
        f"your social style suggests a preference for {social_style.lower()} engagement. "
        f"You appear to thrive with {activity_preference.lower()}, allowing for both "
        f"focused individual pursuits and meaningful interactions when you choose them."
    )
    
    return reasoning


def create_profile(
    scores: Dict[str, float],
    energy_level: Optional[str] = None,
    social_level: Optional[str] = None,
    time_of_day: Optional[str] = None,
) -> UserProfile:
    """
    Generate an anonymous user profile from interest scores.
    
    Args:
        scores: Dictionary of interest categories with percentage scores
        energy_level: Optional metadata (not used in current version)
        social_level: Optional metadata (not used in current version)
        time_of_day: Optional metadata (not used in current version)
    
    Returns:
        UserProfile object containing complete profile information
    """
    # Get top interests
    sorted_interests = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    core_interests = [cat for cat, _ in sorted_interests[:3]]
    secondary_interests = [cat for cat, _ in sorted_interests[3:6]]
    
    # Determine social and activity characteristics
    social_style, _ = determine_social_style(scores)
    activity_preference, _ = determine_activity_preference(scores)
    
    # Build reasoning
    reasoning = build_reasoning(core_interests, social_style, activity_preference, scores)
    
    # Generate suggestions
    suggestions = generate_suggestions(core_interests, scores, social_style)
    
    return UserProfile(
        core_interests=core_interests,
        secondary_interests=secondary_interests,
        social_style=social_style,
        activity_preference=activity_preference,
        reasoning=reasoning,
        suggestions=suggestions,
    )


def format_profile_for_display(profile: UserProfile) -> Dict:
    """
    Format profile for Streamlit display.
    
    Args:
        profile: UserProfile object
    
    Returns:
        Dictionary with formatted profile data
    """
    return {
        "Core Interests": ", ".join(profile.core_interests),
        "Secondary Interests": ", ".join(profile.secondary_interests) if profile.secondary_interests else "None",
        "Social Style": profile.social_style,
        "Activity Preference": profile.activity_preference,
        "Reasoning": profile.reasoning,
        "Suggestions": profile.suggestions,
    }


# Example usage
if __name__ == "__main__":
    # Test with sample scores
    test_scores = {
        "Tech/Engineering": 35.5,
        "Career/Jobs": 25.2,
        "Social/People": 15.3,
        "Sports/Fitness": 12.1,
        "Food": 8.9,
        "Academics/School": 2.0,
        "Entertainment/Gaming": 1.0,
    }
    
    profile = create_profile(test_scores)
    
    print("=" * 60)
    print("ANONYMOUS USER PROFILE")
    print("=" * 60)
    print(f"\nCore Interests: {', '.join(profile.core_interests)}")
    print(f"Secondary Interests: {', '.join(profile.secondary_interests)}")
    print(f"\nSocial Style: {profile.social_style}")
    print(f"Activity Preference: {profile.activity_preference}")
    print(f"\nReasoning:\n{profile.reasoning}")
    print(f"\nPersonalized Suggestions:")
    for i, suggestion in enumerate(profile.suggestions, 1):
        print(f"  {i}. {suggestion}")
