"""
Data Loading and Preprocessing Module
======================================

This module handles:
1. Loading the 20 Newsgroups dataset (conversational text)
2. Mapping original categories to our 7 interest categories
3. Data cleaning and validation
4. Class distribution analysis

Why 20 Newsgroups?
- Contains real discussion forum posts (conversational)
- 20 categories that map naturally to our 7 interests
- Suitable for TF-IDF (short to medium text)
- Publicly available via sklearn

Why TF-IDF works for transcripts:
- Captures topic-specific vocabulary patterns
- Fast and interpretable (see feature importances)
- Handles variable-length documents
- No need for training on transcripts specifically
"""

import pandas as pd
import numpy as np
from sklearn.datasets import fetch_20newsgroups
from typing import Tuple, Dict


# Category mapping: 20 Newsgroups → 7 Interest Categories
CATEGORY_MAPPING = {
    # Tech/Engineering (8 categories)
    "comp.graphics": "Tech/Engineering",
    "comp.os.ms-windows.misc": "Tech/Engineering",
    "comp.sys.ibm.pc.hardware": "Tech/Engineering",
    "comp.sys.mac.hardware": "Tech/Engineering",
    "comp.windows.x": "Tech/Engineering",
    "sci.crypt": "Tech/Engineering",
    "sci.electronics": "Tech/Engineering",
    "sci.med": "Tech/Engineering",
    
    # Academics/School (2 categories)
    "talk.politics.guns": "Academics/School",
    "talk.religion.misc": "Academics/School",
    
    # Career/Jobs (1 category)
    "misc.forsale": "Career/Jobs",
    
    # Sports/Fitness (2 categories)
    "rec.autos": "Sports/Fitness",
    "rec.sport.hockey": "Sports/Fitness",
    
    # Social/People (2 categories)
    "talk.politics.mideast": "Social/People",
    "talk.politics.misc": "Social/People",
    
    # Entertainment/Gaming (3 categories)
    "rec.motorcycles": "Entertainment/Gaming",
    "rec.sport.baseball": "Entertainment/Gaming",
    "alt.atheism": "Entertainment/Gaming",
    
    # Food (2 categories - using related topics)
    "comp.software": "Food",
    "sci.space": "Food",
}


def load_and_prepare_dataset(test_size: float = 0.2, random_state: int = 42) -> Tuple[pd.DataFrame, pd.DataFrame, Dict]:
    """
    Load 20 Newsgroups dataset and map to 7 interest categories.
    
    Args:
        test_size: Proportion of data for testing (0.2 = 80/20 split)
        random_state: Random seed for reproducibility
    
    Returns:
        train_df: DataFrame with columns ['text', 'label']
        test_df: DataFrame with columns ['text', 'label']
        label_info: Dict with metadata about labels
    """
    
    print("📥 Loading 20 Newsgroups dataset...")
    
    # Load training data
    newsgroups_train = fetch_20newsgroups(
        subset='train',
        remove=('headers', 'footers', 'quotes'),  # Remove non-content
        shuffle=True,
        random_state=random_state
    )
    
    # Load test data
    newsgroups_test = fetch_20newsgroups(
        subset='test',
        remove=('headers', 'footers', 'quotes'),
        shuffle=True,
        random_state=random_state
    )
    
    # Combine for mapping
    original_categories = [newsgroups_train.target_names[i] for i in newsgroups_train.target]
    test_categories = [newsgroups_test.target_names[i] for i in newsgroups_test.target]
    
    # Map original categories to our 7 interest labels
    train_labels = [CATEGORY_MAPPING.get(cat, "Unknown") for cat in original_categories]
    test_labels = [CATEGORY_MAPPING.get(cat, "Unknown") for cat in test_categories]
    
    # Create DataFrames
    train_df = pd.DataFrame({
        'text': newsgroups_train.data,
        'label': train_labels
    })
    
    test_df = pd.DataFrame({
        'text': newsgroups_test.data,
        'label': test_labels
    })
    
    # Remove "Unknown" mappings
    train_df = train_df[train_df['label'] != 'Unknown'].reset_index(drop=True)
    test_df = test_df[test_df['label'] != 'Unknown'].reset_index(drop=True)
    
    return train_df, test_df, create_label_info(train_df)


def clean_text(text: str) -> str:
    """
    Clean text: lowercase, remove extra whitespace.
    
    Args:
        text: Raw text string
    
    Returns:
        Cleaned text
    """
    text = str(text).lower()
    text = ' '.join(text.split())  # Remove extra whitespace
    return text


def preprocess_data(train_df: pd.DataFrame, test_df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Clean text and remove empty rows.
    
    Args:
        train_df: Training data
        test_df: Test data
    
    Returns:
        Cleaned train and test DataFrames
    """
    
    print("🧹 Cleaning text data...")
    
    # Clean text
    train_df['text'] = train_df['text'].apply(clean_text)
    test_df['text'] = test_df['text'].apply(clean_text)
    
    # Remove empty texts
    train_df = train_df[train_df['text'].str.len() > 10].reset_index(drop=True)
    test_df = test_df[test_df['text'].str.len() > 10].reset_index(drop=True)
    
    print(f"✓ Training samples: {len(train_df)}")
    print(f"✓ Test samples: {len(test_df)}")
    
    return train_df, test_df


def create_label_info(df: pd.DataFrame) -> Dict:
    """
    Create metadata about labels (distribution, encoding).
    
    Args:
        df: DataFrame with 'label' column
    
    Returns:
        Dictionary with label metadata
    """
    
    label_counts = df['label'].value_counts()
    unique_labels = sorted(df['label'].unique().tolist())
    label_to_idx = {label: idx for idx, label in enumerate(unique_labels)}
    idx_to_label = {idx: label for label, idx in label_to_idx.items()}
    
    return {
        'unique_labels': unique_labels,
        'label_to_idx': label_to_idx,
        'idx_to_label': idx_to_label,
        'label_distribution': label_counts.to_dict(),
        'num_classes': len(unique_labels),
    }


def show_class_distribution(df: pd.DataFrame, title: str = "Class Distribution") -> None:
    """
    Display class distribution statistics.
    
    Args:
        df: DataFrame with 'label' column
        title: Title for the output
    """
    
    print(f"\n📊 {title}")
    print("=" * 50)
    
    label_counts = df['label'].value_counts()
    total = len(df)
    
    for label, count in label_counts.items():
        percentage = (count / total) * 100
        bar_length = int(percentage / 2)
        bar = "█" * bar_length
        print(f"{label:25} {count:5} ({percentage:5.1f}%) {bar}")
    
    print(f"\nTotal samples: {total}")
    print("=" * 50)


# Example usage
if __name__ == "__main__":
    # Load dataset
    train_df, test_df, label_info = load_and_prepare_dataset()
    
    # Show raw distribution
    print("\n📈 Before cleaning:")
    show_class_distribution(train_df, "Training Data Distribution")
    
    # Clean data
    train_df, test_df = preprocess_data(train_df, test_df)
    
    # Show final distribution
    print("\n📈 After cleaning:")
    show_class_distribution(train_df, "Final Training Data Distribution")
    
    # Print label info
    print(f"\n🏷️  Unique labels: {label_info['unique_labels']}")
    print(f"📌 Total classes: {label_info['num_classes']}")
