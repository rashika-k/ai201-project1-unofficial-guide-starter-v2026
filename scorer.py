"""
Decide whether an answer counts as correct.

`run_eval.py` finds this file automatically: once it exists, the Run columns
in results/ carry True/False verdicts instead of raw answers.

The rule here is fuzzy substring matching via rapidfuzz: the answer passes if
the expected phrase appears somewhere in it, allowing small differences in
wording, case, or punctuation. "Tree" still matches "trees", "$" matches
"$3.50", but "Summer" does not match an answer that never mentions a season.
"""

from rapidfuzz import fuzz

# How close the best-matching stretch of the answer must be to the expected
# phrase, 0-100. 85 tolerates plurals and punctuation without letting a
# different word through. Tune it if you see verdicts you disagree with.
MATCH_THRESHOLD = 85


def judge(question: str, expects: str, answer: str, results) -> bool:
    """
    True if `answer` contains something close enough to `expects`.

    Args:
        question: the question that was asked (unused by this rule, but part
                  of the signature run_eval.py calls with).
        expects:  the word or short phrase from questions.py.
        answer:   what the system said, or a refusal.
        results:  the retrieved chunks (unused here; available if you want to
                  score retrieval instead of the answer).
    """
    expects = (expects or "").strip()
    answer = (answer or "").strip()
    if not expects or not answer:
        return False

    # Very short expectations ("No", "$") are too easy to fuzzy-match by
    # accident, so require them to appear literally.
    if len(expects) <= 3:
        return expects.lower() in answer.lower()

    # partial_ratio finds the best-matching window of the answer, so a long
    # answer that contains the phrase somewhere still scores high.
    score = fuzz.partial_ratio(expects.lower(), answer.lower())
    return score >= MATCH_THRESHOLD
