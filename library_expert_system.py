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

    @Rule(Fact(user_type=MATCH.user_type), Fact(topic=MATCH.topic), Fact(resource_type=MATCH.resource_type),
          Fact(language=MATCH.language), Fact(min_rating=MATCH.min_rating))
    def recommend_resources(self, user_type, topic, resource_type, language, min_rating):
        """Recommend resources based on user inputs."""
        topic = topic.strip().lower()
        language = language.strip().lower() if language != "any" else ""  # Handle 'any' language

        # Main recommendation logic (exact match)
        recommendations = [
            (
                item['title'],
                f"Matched {resource_type} titled '{item['title']}' on topic '{item['topic']}' in {item['language']} "
                f"with rating {item['rating']} suitable for {user_type}."
            )
            for item in self.data
            if item['type'] == resource_type
               and topic in item['topic'].lower()
               and (language in item['language'].lower() or not language)  # Match any language if empty
               and item['rating'] >= min_rating
               and (
                       (user_type == 'student' and resource_type == 'book') or
                       (user_type == 'teacher' and resource_type == 'journal') or
                       (user_type == 'researcher' and resource_type == 'article')
               )
        ]

        # Alternative recommendations (if no match found, suggest similar topics or different languages)
        alternative_recommendations = [
            (
                item['title'],
                f"Alternative match: '{item['title']}' on topic '{item['topic']}' available in another language '{item['language']}' with rating {item['rating']}."
            )
            for item in self.data
            if topic in item['topic'].lower()  # Same topic, any resource type and language
               and item['rating'] >= min_rating
               and (user_type == 'student' or user_type == 'teacher' or user_type == 'researcher')
        ]

        # Declare recommendations and alternative recommendations facts
        if recommendations:
            self.declare(Fact(recommendation=[rec[0] for rec in recommendations],
                              explanation=[rec[1] for rec in recommendations]))
        else:
            self.declare(Fact(recommendation=["No resources found matching your criteria."],
                              explanation=["The system could not find any resources meeting all the provided criteria."]))

        if alternative_recommendations:
            self.declare(Fact(alternative_solution=[alt[0] for alt in alternative_recommendations],
                              alternative_explanation=[alt[1] for alt in alternative_recommendations]))

    @Rule(Fact(recommendation=MATCH.rec), Fact(explanation=MATCH.exp), salience=-1)
    def output_recommendation_with_explanation(self, rec, exp):
        """Output the recommendations with explanations."""
        print("Recommendations:")
        for i, recommendation in enumerate(rec):
            print(f"{i + 1}. {recommendation}")
            print(f"   Explanation: {exp[i]}")
        print()

    @Rule(Fact(alternative_solution=MATCH.alt_rec), Fact(alternative_explanation=MATCH.alt_exp), salience=-2)
    def output_alternative_solution(self, alt_rec, alt_exp):
        """Output alternative solutions when main recommendations are unavailable."""
        print("Alternative Recommendations:")
        for i, alt in enumerate(alt_rec):
            print(f"{i + 1}. {alt}")
            print(f"   Explanation: {alt_exp[i]}")
        print()

    @Rule(Fact(recommendation=MATCH.rec), salience=-3)
    def output_no_recommendations(self, rec):
        """Handle cases where no recommendations are found."""
        if rec == ["No resources found matching your criteria."]:
            print("No recommendations found.")
