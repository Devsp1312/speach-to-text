import re
from collections import Counter, defaultdict
from typing import Dict, Tuple, Set, List, Optional


# Enhanced interest taxonomy with weighted keywords
WEIGHTED_KEYWORDS = {
    "Tech/Engineering": {
        # Programming - high weight
        "programming": 2.0, "coding": 2.0, "code": 1.5, "developer": 2.0, "software": 1.5,
        # Languages
        "python": 1.5, "java": 1.5, "javascript": 1.5, "c++": 1.5, "react": 1.5, 
        "css": 1.0, "html": 1.0, "typescript": 1.5, "rust": 1.5, "go": 1.5,
        # Hardware/Electronics
        "arduino": 1.5, "esp32": 1.5, "circuit": 1.5, "pcb": 1.5, "signal": 1.0,
        "semiconductor": 1.5, "mosfet": 1.5, "fpga": 1.5, "embedded": 1.5,
        # AI/ML
        "ai": 1.5, "ml": 1.5, "machine learning": 2.0, "deep learning": 2.0,
        "model": 1.0, "dataset": 1.5, "neural": 1.5, "gpu": 1.0, "tensorflow": 1.5,
        # Tools/Platforms
        "git": 1.0, "github": 1.0, "docker": 1.5, "kubernetes": 1.5, "aws": 1.5,
        "cloud": 1.0, "api": 1.5, "database": 1.5, "sql": 1.5, "linux": 1.5,
        # Concepts
        "algorithm": 1.5, "debug": 1.0, "compile": 1.0, "deploy": 1.0,
        "backend": 1.5, "frontend": 1.5, "fullstack": 1.5, "devops": 1.5,
    },
    "Academics/School": {
        # Core academic terms
        "class": 1.0, "lecture": 1.5, "homework": 1.5, "assignment": 1.5,
        "exam": 2.0, "test": 1.5, "quiz": 1.5, "project": 1.0, "essay": 1.5,
        # People
        "professor": 1.5, "ta": 1.5, "teacher": 1.5, "instructor": 1.5,
        # Outcomes
        "grade": 1.5, "gpa": 2.0, "study": 1.5, "studying": 1.5,
        "midterm": 2.0, "final": 1.5, "finals": 1.5,
        # Activities
        "research": 1.5, "lab": 1.0, "thesis": 2.0, "dissertation": 2.0,
        "semester": 1.0, "course": 1.0, "syllabus": 1.5, "textbook": 1.0,
        "library": 1.0, "campus": 1.0, "university": 1.0, "college": 1.0,
    },
    "Career/Jobs": {
        # Job search
        "internship": 2.0, "interview": 2.0, "resume": 2.0, "cv": 2.0,
        "recruiter": 2.0, "linkedin": 1.5, "offer": 1.5, "application": 1.5,
        "job": 1.5, "career": 1.5, "hiring": 1.5, "recruitment": 1.5,
        # Compensation
        "salary": 2.0, "compensation": 2.0, "benefits": 1.5, "401k": 1.5,
        "stock options": 2.0, "bonus": 1.5, "raise": 1.5, "promotion": 1.5,
        # Work terms
        "workplace": 1.0, "office": 0.5, "remote": 1.0, "wfh": 1.5,
        "manager": 1.0, "boss": 1.0, "colleague": 1.0, "coworker": 1.0,
        "meeting": 0.5, "deadline": 1.0, "project management": 1.5,
    },
    "Sports/Fitness": {
        # Gym/Training
        "gym": 2.0, "workout": 2.0, "exercise": 2.0, "lift": 2.0, "lifting": 2.0,
        "training": 1.5, "cardio": 1.5, "running": 1.5, "jogging": 1.5,
        # Nutrition
        "protein": 1.5, "calories": 1.5, "diet": 1.0, "nutrition": 1.5,
        "supplements": 1.5, "gains": 1.5, "bulk": 1.5, "cut": 1.0,
        # Sports
        "basketball": 2.0, "soccer": 2.0, "football": 2.0, "tennis": 2.0,
        "baseball": 2.0, "volleyball": 2.0, "swimming": 2.0, "cycling": 2.0,
        # General
        "athlete": 1.5, "coach": 1.5, "team": 1.0, "practice": 1.0,
        "game": 0.5, "match": 1.0, "competition": 1.5, "tournament": 1.5,
    },
    "Food": {
        # Meals
        "eat": 1.0, "eating": 1.0, "dinner": 1.5, "lunch": 1.5, "breakfast": 1.5,
        "brunch": 1.5, "meal": 1.5, "snack": 1.0, "hungry": 1.0,
        # Cooking
        "cook": 1.5, "cooking": 1.5, "recipe": 2.0, "bake": 1.5, "baking": 1.5,
        "kitchen": 1.0, "chef": 1.5, "ingredients": 1.5,
        # Places/Types
        "restaurant": 1.5, "cafe": 1.5, "coffee": 1.0, "pizza": 1.0,
        "sushi": 1.0, "burger": 1.0, "taco": 1.0, "ramen": 1.0,
        # Actions
        "order": 0.5, "delivery": 1.0, "takeout": 1.5, "reservation": 1.5,
        "menu": 1.0, "food": 1.0, "taste": 1.0, "delicious": 1.0,
    },
    "Social/People": {
        # Events
        "party": 2.0, "hangout": 2.0, "hang out": 2.0, "meet": 1.0, "meeting": 0.5,
        "club": 1.5, "event": 1.0, "gathering": 1.5, "get together": 2.0,
        # Relationships
        "friends": 1.5, "friend": 1.0, "dating": 2.0, "date": 1.5, "relationship": 1.5,
        "girlfriend": 1.5, "boyfriend": 1.5, "crush": 2.0,
        # Communication
        "conversation": 1.0, "talking": 1.0, "chat": 1.0, "texting": 1.0,
        "call": 0.5, "social": 1.5, "networking": 1.0,
        # Activities
        "bar": 1.5, "drinks": 1.5, "dance": 1.5, "dancing": 1.5,
        "karaoke": 2.0, "trivia": 1.5, "board game": 1.5,
    },
    "Entertainment/Gaming": {
        # Gaming
        "game": 1.0, "gaming": 2.0, "gamer": 2.0, "gameplay": 2.0,
        "valorant": 2.0, "league": 1.5, "lol": 1.0, "minecraft": 2.0,
        "fortnite": 2.0, "apex": 2.0, "cod": 2.0, "cs2": 2.0, "csgo": 2.0,
        "playstation": 1.5, "xbox": 1.5, "nintendo": 1.5, "switch": 1.0,
        "pc gaming": 2.0, "console": 1.5, "steam": 1.5,
        # Media
        "movie": 1.5, "film": 1.5, "cinema": 1.5, "netflix": 2.0,
        "hulu": 2.0, "disney plus": 2.0, "streaming": 1.5, "binge": 1.5,
        # Music
        "music": 1.5, "song": 1.0, "album": 1.5, "concert": 2.0,
        "festival": 1.5, "spotify": 1.5, "playlist": 1.5,
        # Content
        "youtube": 1.5, "twitch": 2.0, "podcast": 1.5, "streamer": 2.0,
        "stream": 1.0, "video": 1.0, "watch": 0.5, "watching": 0.5,
    },
}

# Negation words that flip meaning
NEGATIONS = {
    "not", "no", "never", "don't", "dont", "doesn't", "doesnt", "won't", "wont",
    "can't", "cant", "couldn't", "couldnt", "wouldn't", "wouldnt", "shouldn't",
    "shouldnt", "isn't", "isnt", "aren't", "arent", "wasn't", "wasnt", "weren't",
    "werent", "hardly", "barely", "neither", "nor", "none", "nobody", "nothing",
}

# Context words that boost certain categories
CONTEXT_BOOSTERS = {
    "Tech/Engineering": {
        "learn", "build", "develop", "create", "design", "implement", "debug", "fix"
    },
    "Academics/School": {
        "due", "submit", "prepare", "review", "cram", "pass", "fail"
    },
    "Career/Jobs": {
        "apply", "search", "looking", "negotiate", "accept", "decline"
    },
}

# Text cleaning regex
CLEAN_RE = re.compile(r"[^a-z0-9\s'+#]")

# Configuration
MIN_SCORE_THRESHOLD = 3.0  # Minimum percentage to include in results
NEGATION_WINDOW = 3  # Words before keyword to check for negation
CONTEXT_WINDOW = 5  # Words around keyword to check for context
CONTEXT_BOOST = 1.3  # Multiplier when context words found


def clean_text(text: str) -> str:
    """Clean and normalize text to lowercase and remove special characters."""
    text = text.lower()
    text = CLEAN_RE.sub(" ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def build_keyword_index() -> Tuple[Dict[str, Dict[str, float]], Dict[str, List]]:
    """Build indexed keyword structure for fast matching."""
    token_keywords = {}
    phrase_patterns = {}
    
    for cat, kw_weights in WEIGHTED_KEYWORDS.items():
        tokens = {}
        patterns = []
        
        for kw, weight in kw_weights.items():
            normalized = clean_text(kw)
            if not normalized:
                continue
            
            # Multi-word keywords become regex patterns
            if " " in normalized:
                patterns.append((re.compile(rf"\b{re.escape(normalized)}\b"), weight))
            else:
                tokens[normalized] = weight
        
        token_keywords[cat] = tokens
        phrase_patterns[cat] = patterns
    
    return token_keywords, phrase_patterns


# Pre-build indices
TOKEN_KEYWORDS, PHRASE_PATTERNS = build_keyword_index()


def check_negation(tokens: List[str], index: int, window: int = NEGATION_WINDOW) -> bool:
    """Check if keyword at index is negated by nearby negation words."""
    start = max(0, index - window)
    return any(tokens[i] in NEGATIONS for i in range(start, index))


def check_context_boost(tokens: List[str], index: int, category: str, 
                        window: int = CONTEXT_WINDOW) -> bool:
    """Check if keyword has supporting context words nearby."""
    context_words = CONTEXT_BOOSTERS.get(category, set())
    if not context_words:
        return False
    
    start = max(0, index - window)
    end = min(len(tokens), index + window + 1)
    
    nearby_words = set(tokens[start:index] + tokens[index+1:end])
    return bool(nearby_words & context_words)


def score_interests(text: str, include_details: bool = False) -> Dict[str, any]:
    """
    Score text against interest categories and return normalized percentages.
    
    Args:
        text: Input text to analyze
        include_details: If True, return matched keywords and confidence levels
    
    Returns:
        Dictionary with scores (and optionally details)
    """
    cleaned = clean_text(text)
    tokens = cleaned.split()
    token_counts = Counter(tokens)

    scores = {}
    matched_keywords = defaultdict(list) if include_details else None
    
    for cat in WEIGHTED_KEYWORDS:
        score = 0.0
        
        # Score single-token keywords
        for kw, weight in TOKEN_KEYWORDS.get(cat, {}).items():
            if kw in token_counts:
                # Find all positions of this keyword
                indices = [i for i, t in enumerate(tokens) if t == kw]
                
                for idx in indices:
                    # Check for negation
                    if check_negation(tokens, idx):
                        continue
                    
                    # Apply base weight
                    kw_score = weight
                    
                    # Apply context boost if applicable
                    if check_context_boost(tokens, idx, cat):
                        kw_score *= CONTEXT_BOOST
                    
                    score += kw_score
                    
                    if include_details:
                        matched_keywords[cat].append((kw, kw_score))
        
        # Score multi-word phrase patterns
        for pattern, weight in PHRASE_PATTERNS.get(cat, []):
            matches = pattern.finditer(cleaned)
            for match in matches:
                # Calculate token position for negation check
                match_start = match.start()
                tokens_before = cleaned[:match_start].split()
                token_idx = len(tokens_before)
                
                # Check for negation
                if check_negation(tokens, token_idx):
                    continue
                
                # Apply base weight
                phrase_score = weight
                
                # Apply context boost if applicable
                if check_context_boost(tokens, token_idx, cat):
                    phrase_score *= CONTEXT_BOOST
                
                score += phrase_score
                
                if include_details:
                    matched_keywords[cat].append((match.group(), phrase_score))
        
        scores[cat] = score

    # Calculate percentages
    total = sum(scores.values())
    if total == 0:
        percentages = {k: 0.0 for k in scores}
    else:
        percentages = {k: round(v / total * 100, 1) for k, v in scores.items()}
    
    # Apply minimum threshold
    percentages = {k: v for k, v in percentages.items() if v >= MIN_SCORE_THRESHOLD}
    
    # Renormalize after threshold filtering
    total_after_threshold = sum(percentages.values())
    if total_after_threshold > 0 and total_after_threshold < 99:
        percentages = {k: round(v / total_after_threshold * 100, 1) 
                      for k, v in percentages.items()}
    
    if not include_details:
        return percentages
    
    # Include details: confidence and matched keywords
    result = {
        "scores": percentages,
        "matched_keywords": dict(matched_keywords),
        "confidence": {}
    }
    
    for cat, score in percentages.items():
        num_matches = len(matched_keywords.get(cat, []))
        if score > 40 and num_matches >= 5:
            confidence = "High"
        elif score > 20 and num_matches >= 3:
            confidence = "Medium"
        else:
            confidence = "Low"
        result["confidence"][cat] = confidence
    
    return result


def get_top_interests(scores: Dict[str, float], top_n: int = 3) -> List[str]:
    """Get top N interest categories with non-zero scores."""
    sorted_items = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [k for k, v in sorted_items if v > 0][:top_n]


def format_interest_table(scores: Dict[str, float]) -> List[Dict]:
    """Format interest scores for display as table."""
    sorted_items = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [{"Category": k, "Score (%)": v} for k, v in sorted_items]


def analyze_text(text: str, verbose: bool = False) -> Dict:
    """
    Main analysis function with optional verbose output.
    
    Args:
        text: Input text to analyze
        verbose: If True, includes matched keywords and confidence levels
    
    Returns:
        Analysis results with scores and optional details
    """
    results = score_interests(text, include_details=verbose)
    
    if verbose:
        scores = results["scores"]
    else:
        scores = results
    
    analysis = {
        "scores": scores,
        "top_interests": get_top_interests(scores),
        "formatted_table": format_interest_table(scores)
    }
    
    if verbose:
        analysis["matched_keywords"] = results["matched_keywords"]
        analysis["confidence"] = results["confidence"]
    
    return analysis


# Example usage
if __name__ == "__main__":
    # Test examples
    test_texts = [
        "I spent all day coding in Python and debugging my machine learning model. Need to optimize the neural network architecture.",
        "Have a midterm exam tomorrow and finals next week. Been studying in the library all day for my algorithms class.",
        "Just got an internship offer! The salary and benefits look great. Need to update my LinkedIn and negotiate.",
        "Hit a new PR at the gym today! Been training hard and upping my protein intake. Basketball practice later.",
        "Going to that new pizza place for dinner, then meeting friends at a party. Should be fun!",
        "Been playing Valorant all weekend. Also watched some Netflix and listened to new albums on Spotify.",
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n{'='*60}")
        print(f"Example {i}:")
        print(f"Text: {text[:80]}...")
        print(f"{'='*60}")
        
        # Basic analysis
        result = analyze_text(text, verbose=False)
        print(f"\nTop 3 Interests: {', '.join(result['top_interests'])}")
        print(f"\nScore Breakdown:")
        for item in result['formatted_table']:
            print(f"  {item['Category']}: {item['Score (%)']}%")
        
        # Verbose analysis for first example
        if i == 1:
            print(f"\n{'*'*60}")
            print("VERBOSE ANALYSIS (Example 1 only):")
            print(f"{'*'*60}")
            verbose_result = analyze_text(text, verbose=True)
            
            for cat in verbose_result['top_interests']:
                print(f"\n{cat}:")
                print(f"  Confidence: {verbose_result['confidence'].get(cat, 'N/A')}")
                print(f"  Matched Keywords: {verbose_result['matched_keywords'].get(cat, [])[:5]}")  # Show first 5