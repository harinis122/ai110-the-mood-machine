# mood_analyzer.py
"""
Rule based mood analyzer for short text snippets.

This class starts with very simple logic:
  - Preprocess the text
  - Look for positive and negative words
  - Compute a numeric score
  - Convert that score into a mood label
"""

import re
from typing import List, Dict, Tuple, Optional

from dataset import (
    POSITIVE_WORDS, NEGATIVE_WORDS,
    STRONG_POSITIVE_WORDS, STRONG_NEGATIVE_WORDS,
    POSITIVE_EMOJIS, NEGATIVE_EMOJIS,
    NEGATION_WORDS, SARCASM_PHRASES,
)


class MoodAnalyzer:
    """
    A very simple, rule based mood classifier.
    """

    def __init__(
        self,
        positive_words: Optional[List[str]] = None,
        negative_words: Optional[List[str]] = None,
    ) -> None:
        # Use the default lists from dataset.py if none are provided.
        positive_words = positive_words if positive_words is not None else POSITIVE_WORDS
        negative_words = negative_words if negative_words is not None else NEGATIVE_WORDS

        # Store as sets for faster lookup.
        self.positive_words = set(w.lower() for w in positive_words)
        self.negative_words = set(w.lower() for w in negative_words)

    # ---------------------------------------------------------------------
    # Preprocessing
    # ---------------------------------------------------------------------

    def preprocess(self, text: str) -> List[str]:
        """
        Convert raw text into a list of tokens the model can work with.

        TODO: Improve this method.

        Right now, it does the minimum:
          - Strips leading and trailing whitespace
          - Converts everything to lowercase
          - Splits on spaces

        Ideas to improve:
          - Remove punctuation
          - Handle simple emojis separately (":)", ":-(", "🥲", "😂")
          - Normalize repeated characters ("soooo" -> "soo")
        """
        # Normalize repeated characters: "happyyyyy" -> "happy", "!!!!" -> "!"
        text = re.sub(r'(.)\1{2,}', r'\1', text)

        cleaned = text.strip().lower()

        all_emojis = set(POSITIVE_EMOJIS) | set(NEGATIVE_EMOJIS)

        # Strip punctuation from each token but preserve emoji-style text like ":)"
        tokens = []
        for token in cleaned.split():
            if token in all_emojis:
                tokens.append(token)
            else:
                token = token.strip('.,!?;:\'"')
                if token:
                    tokens.append(token)

        return tokens

    # ---------------------------------------------------------------------
    # Scoring logic
    # ---------------------------------------------------------------------

    def score_text(self, text: str) -> int:
        """
        Compute a numeric score for a piece of text.
        """
        strong_pos = set(w.lower() for w in STRONG_POSITIVE_WORDS)
        strong_neg = set(w.lower() for w in STRONG_NEGATIVE_WORDS)
        emoji_pos = set(POSITIVE_EMOJIS)
        emoji_neg = set(NEGATIVE_EMOJIS)
        negations = set(NEGATION_WORDS)

        score = 0

        # Check for sarcasm phrases in the raw lowercased text before token scoring
        lowered = text.lower()
        for phrase in SARCASM_PHRASES:
            if phrase in lowered:
                score -= 3
                break

        tokens = self.preprocess(text)
        negate = False

        for token in tokens:
            if token in negations:
                negate = True
                continue
            # treat emojis and strong words as stronger signals
            if token in emoji_pos:
                weight = 2
            elif token in emoji_neg:
                weight = -2
            # treat strong positive and negative words as stronger signals
            elif token in strong_pos:
                weight = 2
            elif token in strong_neg:
                weight = -2
            elif token in self.positive_words:
                weight = 1
            elif token in self.negative_words:
                weight = -1
            else:
                weight = 0
            # handle basic negation: if the previous token was a negation word, flip the weight of this token
            if negate and weight != 0:
                weight = -weight
                negate = False

            score += weight

        return score

    # ---------------------------------------------------------------------
    # Label prediction
    # ---------------------------------------------------------------------

    def predict_label(self, text: str) -> str:
        """
        Turn the numeric score for a piece of text into a mood label.

        The default mapping is:
          - score > 0  -> "positive"
          - score < 0  -> "negative"
          - score == 0 -> "neutral"

        TODO: You can adjust this mapping if it makes sense for your model.
        For example:
          - Use different thresholds (for example score >= 2 to be "positive")
          - Add a "mixed" label for scores close to zero
        Just remember that whatever labels you return should match the labels
        you use in TRUE_LABELS in dataset.py if you care about accuracy.
        """
        score = self.score_text(text)
        if score > 0:
            return "positive"
        elif score < 0:
            return "negative"
        else:
            return "neutral"

    # ---------------------------------------------------------------------
    # Explanations (optional but recommended)
    # ---------------------------------------------------------------------

    def explain(self, text: str) -> str:
        """
        Return a short string explaining WHY the model chose its label.

        TODO:
          - Look at the tokens and identify which ones counted as positive
            and which ones counted as negative.
          - Show the final score.
          - Return a short human readable explanation.

        Example explanation (your exact wording can be different):
          'Score = 2 (positive words: ["love", "great"]; negative words: [])'

        The current implementation is a placeholder so the code runs even
        before you implement it.
        """
        tokens = self.preprocess(text)

        positive_hits: List[str] = []
        negative_hits: List[str] = []
        score = 0

        for token in tokens:
            if token in self.positive_words:
                positive_hits.append(token)
                score += 1
            if token in self.negative_words:
                negative_hits.append(token)
                score -= 1

        return (
            f"Score = {score} "
            f"(positive: {positive_hits or '[]'}, "
            f"negative: {negative_hits or '[]'})"
        )
