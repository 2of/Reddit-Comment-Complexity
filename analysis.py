import numpy as np
from transformers import pipeline
from textstat import textstat  # Library for readability metrics

class SentimentAnalyzer:
    def __init__(self):
        """
        Initialize the sentiment, emotion, and writing level analysis models.
        """
        # Load pre-trained sentiment analysis model
        self.sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

        # Load pre-trained emotion detection model
        self.emotion_pipeline = pipeline("text-classification", model="bhadresh-savani/distilbert-base-uncased-emotion")

    def _analyze_sentiment(self, comment):
        """
        Analyze the sentiment of a single comment.
        """
        result = self.sentiment_pipeline(comment)[0]
        return {
            "sentiment_label": result["label"],
            "sentiment_score": result["score"]
        }

    def _analyze_emotion(self, comment):
        """
        Analyze the emotion of a single comment.
        """
        result = self.emotion_pipeline(comment)[0]
        return {
            "emotion_label": result["label"],
            "emotion_score": result["score"]
        }

    def _analyze_writing_level(self, comment):
        """
        Analyze the writing level of a single comment using readability metrics.
        """
        return {
            "flesch_reading_ease": textstat.flesch_reading_ease(comment),  # Higher score = easier to read
            "flesch_kincaid_grade": textstat.flesch_kincaid_grade(comment),  # U.S. school grade level
            "gunning_fog": textstat.gunning_fog(comment),  # Years of education needed to understand
            "smog_index": textstat.smog_index(comment),  # Years of education needed to understand
            "lexical_diversity": self._calculate_lexical_diversity(comment)  # Unique words / total words
        }

    def _calculate_lexical_diversity(self, text):
        """
        Calculate lexical diversity (unique words / total words).
        """
        words = text.split()
        if len(words) == 0:
            return 0
        return len(set(words)) / len(words)

    def _calculate_statistics(self, scores):
        """
        Calculate statistical features (mean, median, std) for a list of scores.
        """
        return {
            "mean": np.mean(scores),
            "median": np.median(scores),
            "std": np.std(scores)
        }

    def __call__(self, comments):
        """
        Process a list of comments and return:
        1. Individual scores for each metric.
        2. Overall average scores and statistical features.
        """
        results = []
        sentiment_scores = []
        emotion_scores = []
        flesch_reading_ease_scores = []
        flesch_kincaid_grade_scores = []
        gunning_fog_scores = []
        smog_index_scores = []
        lexical_diversity_scores = []

        for comment in comments:
            # Analyze sentiment
            sentiment_result = self._analyze_sentiment(comment)
            sentiment_scores.append(sentiment_result["sentiment_score"])

            # Analyze emotion
            emotion_result = self._analyze_emotion(comment)
            emotion_scores.append(emotion_result["emotion_score"])

            # Analyze writing level
            writing_level_result = self._analyze_writing_level(comment)
            flesch_reading_ease_scores.append(writing_level_result["flesch_reading_ease"])
            flesch_kincaid_grade_scores.append(writing_level_result["flesch_kincaid_grade"])
            gunning_fog_scores.append(writing_level_result["gunning_fog"])
            smog_index_scores.append(writing_level_result["smog_index"])
            lexical_diversity_scores.append(writing_level_result["lexical_diversity"])

            # Combine results for this comment
            results.append({
                "comment": comment,
                "sentiment": sentiment_result,
                "emotion": emotion_result,
                "writing_level": writing_level_result
            })

        # Calculate overall statistics
        overall_stats = {
            "sentiment": self._calculate_statistics(sentiment_scores),
            "emotion": self._calculate_statistics(emotion_scores),
            "flesch_reading_ease": self._calculate_statistics(flesch_reading_ease_scores),
            "flesch_kincaid_grade": self._calculate_statistics(flesch_kincaid_grade_scores),
            "gunning_fog": self._calculate_statistics(gunning_fog_scores),
            "smog_index": self._calculate_statistics(smog_index_scores),
            "lexical_diversity": self._calculate_statistics(lexical_diversity_scores)
        }

        return {
            "individual_results": results,
            "overall_statistics": overall_stats
        }


# Example usage
if __name__ == "__main__":
    analyzer = SentimentAnalyzer()
    comments = [
        "I love this product! It's amazing!",
        "I hate this product. It's terrible.",
        "This is okay, but could be better.",
        "I'm so excited to use this!",
        "I'm really disappointed with the quality."
    ]

    output = analyzer(comments)

    # Print individual results
    print("Individual Results:")
    for result in output["individual_results"]:
        print(f"Comment: {result['comment']}")
        print(f"Sentiment: {result['sentiment']}")
        print(f"Emotion: {result['emotion']}")
        print(f"Writing Level: {result['writing_level']}")
        print()

    # Print overall statistics
    print("Overall Statistics:")
    print(f"Sentiment: {output['overall_statistics']['sentiment']}")
    print(f"Emotion: {output['overall_statistics']['emotion']}")
    print(f"Flesch Reading Ease: {output['overall_statistics']['flesch_reading_ease']}")
    print(f"Flesch-Kincaid Grade: {output['overall_statistics']['flesch_kincaid_grade']}")
    print(f"Gunning Fog: {output['overall_statistics']['gunning_fog']}")
    print(f"SMOG Index: {output['overall_statistics']['smog_index']}")
    print(f"Lexical Diversity: {output['overall_statistics']['lexical_diversity']}")