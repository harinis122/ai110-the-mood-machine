# Model Card: Mood Machine

This model card covers both versions of the Mood Machine mood classifier:

1. A **rule-based model** implemented in `mood_analyzer.py`
2. A **machine learning model** implemented in `ml_experiments.py` using scikit-learn

---

## 1. Model Overview

**Model type:**  
Both models were implemented and compared. The rule-based model was the primary focus; the ML model was explored to compare approaches.

**Intended purpose:**  
Classify short text messages (social media posts, messages) into mood labels: `positive`, `negative`, `neutral`, or `mixed`.

**How it works (brief):**  
The rule-based model assigns a numeric score to each text by scanning tokens for positive/negative words and emojis, applying weights, handling negation, and checking for sarcasm phrases. The score is mapped to a label. The ML model converts each post into a bag-of-words vector using `CountVectorizer` and trains a `LogisticRegression` classifier to predict labels from those word counts.

---

## 2. Data

**Dataset description:**  
The dataset contains 18 posts in `SAMPLE_POSTS` with matching labels in `TRUE_LABELS`. The starter set had 14 posts; 4 new posts were added covering sarcasm, mixed emotions, slang, and informal negation.

**Labeling process:**  
Labels were assigned by reading each post and judging the overall mood. Posts with both positive and negative signals were labeled `"mixed"`. Some posts were genuinely ambiguous — for example, `"Sarcasm is the best way to express my feelings. :)"` could be read as ironic (negative) or playfully self-aware (neutral), and `"I can't even deal with this right now"` could be frustration or exhaustion depending on context.

**Important characteristics of the dataset:**  
- Contains slang: `"lowkey"`, `"highkey"`, `"no cap"`, `"fire"`
- Includes text-style emojis (`:)`, `:(`) and Unicode emojis (`😎`)
- Includes sarcasm: `"I absolutely love getting stuck in traffic"`
- Includes negation: `"I am not happy about this"`
- Some posts express mixed feelings: `"Feeling tired but kind of hopeful"`
- Posts are short (one to two sentences), similar to social media messages

**Possible issues with the dataset:**  
- Only 18 examples — too small to train a reliable ML model; accuracy on the training set is misleading
- Slight imbalance: more positive and negative examples than neutral or mixed
- Some labels are subjective and another person might assign a different label
- No held-out test set, so neither model's accuracy reflects real-world performance

---

## 3. How the Rule-Based Model Works

**Scoring rules:**  
- Each token is matched against word lists; regular positive/negative words score ±1
- Strong words (`"love"`, `"hate"`, `"terrible"`, `"amazing"`) score ±2
- Positive and negative emojis (`:)`, `😎`, `:(`, `😭`) score ±2
- Negation words (`"not"`, `"never"`, `"can't"`, etc.) flip the sign of the next scored token
- Known sarcasm phrases (`"absolutely love"`, `"oh great"`, etc.) apply a -3 penalty before token scoring
- Preprocessing normalizes repeated characters (`"happyyyyy"` → `"happy"`) and strips punctuation while preserving emoji tokens

**Label mapping:**  
- score > 0 → `"positive"`
- score < 0 → `"negative"`
- score == 0 → `"neutral"`
- `"mixed"` is never predicted

**Strengths:**  
- Handles negation explicitly (`"not happy"` → negative)
- Catches known sarcasm phrases
- Letter extensions work (`"loooove"` → `"love"`)
- Emoji signals are weighted more heavily than regular words
- Transparent and easy to debug — you can trace exactly why any score was assigned

**Weaknesses:**  
- Never predicts `"mixed"`, so all mixed-labeled posts are counted wrong
- Sarcasm detection only works for phrases explicitly in the list
- Negation only flips the next token, not all tokens in the clause
- Unknown slang (`"fire"`, `"lowkey"`) is ignored unless added to a word list
- Rule-based accuracy on the 18-post dataset: **56% (10/18)**

---

## 4. How the ML Model Works

**Features used:**  
Bag of words using `CountVectorizer` — each post is represented as a vector of word counts across the full training vocabulary.

**Training data:**  
Trained on all 18 posts in `SAMPLE_POSTS` with labels from `TRUE_LABELS`.

**Training behavior:**  
Adding more labeled examples improved the model's ability to associate words with labels. With only 18 examples, the model is effectively memorizing the training set rather than generalizing, which is why training accuracy (94%) is much higher than what you'd expect on new data.

**Strengths:**  
- Learns patterns automatically without hand-crafted rules
- Picks up on co-occurrence patterns (e.g. `"tired"` + `"stressed"` → mixed)
- Handles slang if it appears in training data with consistent labels
- Training accuracy on the 18-post dataset: **94% (17/18)**

**Weaknesses:**  
- No concept of negation — `"not happy"` and `"happy"` look similar to it
- Unknown words at inference time are silently ignored
- With 18 examples it is almost certainly overfitting — it won't generalize to new posts
- Cannot explain its predictions

---

## 5. Evaluation

**How the models were evaluated:**  
Both models were evaluated on the same 18 labeled posts in `dataset.py` (training accuracy — no separate test set exists).

**Examples of correct predictions (rule-based):**  
- `"I love this class so much"` → `positive` — `"love"` is a strong positive word (+2), clear signal
- `"I am not happy about this"` → `negative` — negation correctly flips `"happy"` from +1 to -1
- `"I absolutely love getting stuck in traffic"` → `negative` — sarcasm phrase `"absolutely love"` applies -3 penalty

**Examples of incorrect predictions (rule-based):**  
- `"Feeling tired but kind of hopeful"` → `negative` (true: `mixed`) — `"tired"` scores -1 but `"hopeful"` is not in any word list, so the mixed signal is missed
- `"This is lowkey fire"` → `neutral` (true: `positive`) — `"lowkey"` and `"fire"` are slang not in any word list, so score stays 0
- `"I can't even deal with this right now"` → `neutral` (true: `negative`) — no words in the sentence match the negative word list, so nothing is scored

---

## 6. Limitations

- **Dataset is very small** — 18 posts is not enough to train or evaluate either model reliably
- **No test set** — both models are evaluated on their training data, so reported accuracy is optimistic
- **Mixed label is never predicted by the rule-based model** — the scoring threshold maps everything to positive, negative, or neutral
- **Sarcasm detection is brittle** — only catches explicitly listed phrases; novel sarcasm is missed
- **Slang coverage is incomplete** — words like `"fire"`, `"lowkey"`, `"no cap"` are not in the word lists unless manually added
- **Negation scope is limited** — only the immediately following scored token is flipped

---

## 7. Ethical Considerations

- **Misclassifying distress** — a message like `"I can't even deal with this"` could reflect genuine crisis; labeling it `neutral` instead of `negative` could cause harm in an application meant to detect struggling users
- **Slang and dialect bias** — the word lists and training data reflect a narrow set of language patterns; the model will perform worse on posts that use different dialects, languages, or communities' slang
- **Sarcasm mislabeling** — sarcastic posts not in the phrase list will be labeled positive, potentially misrepresenting someone's actual mood
- **Privacy** — mood detection on personal messages raises consent and privacy concerns; users should know their text is being analyzed

---

## 8. Ideas for Improvement

- **Add more labeled data** — at minimum 100–200 diverse examples to reduce overfitting in the ML model
- **Add a real test set** — hold out 20% of data before training so accuracy reflects generalization, not memorization
- **Expand slang coverage** — add `"fire"`, `"lowkey"`, `"highkey"`, `"no cap"`, `"ngl"`, `"fr"` to the appropriate word lists
- **Predict `"mixed"` label** — use a threshold range (e.g. score between -1 and +1 with both positive and negative tokens present) to return `"mixed"`
- **Improve negation scope** — flip all tokens until the next punctuation or conjunction rather than just the next token
- **Use TF-IDF instead of CountVectorizer** — down-weights common words and gives more signal to distinctive terms
- **Use a small pre-trained model** — a fine-tuned BERT or DistilBERT would handle sarcasm, negation, and slang far better with limited training data
