"""
Shared data for the Mood Machine lab.

This file defines:
  - POSITIVE_WORDS: starter list of positive words
  - NEGATIVE_WORDS: starter list of negative words
  - SAMPLE_POSTS: short example posts for evaluation and training
  - TRUE_LABELS: human labels for each post in SAMPLE_POSTS
"""

# ---------------------------------------------------------------------
# Starter word lists
# ---------------------------------------------------------------------

POSITIVE_WORDS = [
    "happy",
    "great",
    "good",
    "love",
    "excited",
    "awesome",
    "fun",
    "chill",
    "relaxed",
    "amazing",
]

NEGATIVE_WORDS = [
    "sad",
    "bad",
    "terrible",
    "awful",
    "angry",
    "upset",
    "tired",
    "stressed",
    "hate",
    "boring",
    "disappointed",
]

# Words worth +2 (stronger positive signal)
STRONG_POSITIVE_WORDS = [
    "love", "amazing", "awesome", "excited", "excellent", "fantastic",
]

# Words worth -2 (stronger negative signal)
STRONG_NEGATIVE_WORDS = [
    "hate", "terrible", "awful", "horrible", "disgusting", "miserable",
]

# Emojis and emoji-style text that signal positive mood (weight +2)
POSITIVE_EMOJIS = [":)", ":-)", ":d", "😊", "😍", "😎", "🥰", "😂", "❤️", "🎉"]

# Emojis and emoji-style text that signal negative mood (weight -2)
NEGATIVE_EMOJIS = [":(", ":-(", "😢", "😭", "😡", "💀", "😤", "🙄", "😞"]

# Words that flip the sentiment of the next scored token
NEGATION_WORDS = [
    "not", "never", "no", "didn't", "don't", "doesn't",
    "wasn't", "isn't", "aren't", "won't", "can't", "cannot",
]

# ---------------------------------------------------------------------
# Starter labeled dataset
# ---------------------------------------------------------------------

# Short example posts written as if they were social media updates or messages.
SAMPLE_POSTS = [
    "I love this class so much",
    "Today was a terrible day",
    "Feeling tired but kind of hopeful",
    "This is fine",
    "So excited for the weekend",
    "I am not happy about this",
    "Lowkey stressed but kind of proud of myself",
    "Highkey excited about the new project",
    "No cap, this is actually pretty good",
    "I'm so tired of this",
    "I absolutely love getting stuck in traffic",
    "Excited to see my friends tonight! :)",
    "Just got a promotion at work! Feeling on top of the world! 😎",
    "Ugh, I can't believe I have to work late again. So frustrating. :(",
]

# Human labels for each post above.
# Allowed labels in the starter:
#   - "positive"
#   - "negative"
#   - "neutral"
#   - "mixed"
TRUE_LABELS = [
    "positive",  # "I love this class so much"
    "negative",  # "Today was a terrible day"
    "mixed",     # "Feeling tired but kind of hopeful"
    "neutral",   # "This is fine"
    "positive",  # "So excited for the weekend"
    "negative",  # "I am not happy about this"
    "mixed",     # "Lowkey stressed but kind of proud of myself"
    "positive",  # "Highkey excited about the new project"
    "positive",  # "No cap, this is actually pretty good"
    "negative",  # "I'm so tired of this"
    "negative",  # "I absolutely love getting stuck in traffic"
    "positive",  # "Excited to see my friends tonight! :)"
    "positive",  # "Just got a promotion at work! Feeling on top of the world! 😎"
    "negative",  # "Ugh, I can't believe I have to work late again. So frustrating. :("
]

# TODO: Add 5-10 more posts and labels.
#
# Requirements:
#   - For every new post you add to SAMPLE_POSTS, you must add one
#     matching label to TRUE_LABELS.
#   - SAMPLE_POSTS and TRUE_LABELS must always have the same length.
#   - Include a variety of language styles, such as:
#       * Slang ("lowkey", "highkey", "no cap")
#       * Emojis (":)", ":(", "🥲", "😂", "💀")
#       * Sarcasm ("I absolutely love getting stuck in traffic")
#       * Ambiguous or mixed feelings
#
# Tips:
#   - Try to create some examples that are hard to label even for you.
#   - Make a note of any examples that you and a friend might disagree on.
#     Those "edge cases" are interesting to inspect for both the rule based
#     and ML models.
#
# Example of how you might extend the lists:
#
# SAMPLE_POSTS.append("Lowkey stressed but kind of proud of myself")
# TRUE_LABELS.append("mixed")
#
# Remember to keep them aligned:
#   len(SAMPLE_POSTS) == len(TRUE_LABELS)
