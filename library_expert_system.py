from experta import *
import json


def load_data():
    """Load data from the JSON file."""
    try:
        with open("books_data.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Error: books_data.json not found.")
        return []


class LibraryExpertSystem(KnowledgeEngine):
    """Expert system for library recommendations."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = load_data()

    @Rule(Fact(user_type=MATCH.user_type),
          Fact(topic=MATCH.topic),
          Fact(resource_type=MATCH.resource_type),
          Fact(language=MATCH.language),
          Fact(min_rating=MATCH.min_rating))
    def recommend_resources(self, user_type, topic, resource_type, language, min_rating):
        """Recommend resources based on user inputs."""

        # Allow missing values (i.e., handle None)
        topic = topic.strip().lower() if topic else None
        language = language.strip().lower() if language else None

        recommendations = []
        confidence_scores = []

        # Loop through data and calculate confidence based on available data
        for item in self.data:
            confidence = 100  # Start with full confidence

            # Adjust confidence based on missing information
            if topic and topic not in item['topic'].lower():
                confidence -= 20  # Deduct confidence if topic doesn't match
            if language and language not in item['language'].lower():
                confidence -= 20  # Deduct confidence if language doesn't match

            # Check if item matches the user type and resource type
            if item['type'] == resource_type and item['rating'] >= min_rating:
                if (user_type == 'student' and resource_type == 'book') or \
                   (user_type == 'teacher' and resource_type == 'journal') or \
                   (user_type == 'researcher' and resource_type == 'article'):
                    recommendations.append(
                        (
                            item['title'],
                            f"Matched {resource_type} titled '{item['title']}' on topic '{item['topic']}' in {item['language']} "
                            f"with rating {item['rating']} suitable for {user_type}."
                        )
                    )
                    confidence_scores.append(confidence)

        # Declare facts for recommendations and their confidence scores
        if recommendations:
            self.declare(Fact(recommendation=[rec[0] for rec in recommendations],
                              explanation=[rec[1] for rec in recommendations],
                              confidence=confidence_scores))
        else:
            self.declare(Fact(recommendation=["No resources found matching your criteria."],
                              explanation=["The system could not find any resources meeting all the provided criteria."]))

        # Alternative recommendations if no match found
        alternative_recommendations = []
        alternative_confidence = []

        for item in self.data:
            confidence = 100
            if (not topic or topic in item['topic'].lower()) and item['rating'] >= min_rating:
                alternative_recommendations.append(
                    (
                        item['title'],
                        f"Alternative match: '{item['title']}' on topic '{item['topic']}' available in another language '{item['language']}' with rating {item['rating']}."
                    )
                )
                alternative_confidence.append(confidence)

        if alternative_recommendations:
            self.declare(Fact(alternative_solution=[alt[0] for alt in alternative_recommendations],
                              alternative_explanation=[alt[1] for alt in alternative_recommendations],
                              alternative_confidence=alternative_confidence))
