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
        # Normalize input values
        topic = topic.strip().lower()
        language = language.strip().lower()

        print(f"[DEBUG] Filtering {resource_type} for {user_type}s on topic '{topic}' in '{language}' with rating >= {min_rating}")

        # Filter recommendations based on criteria
        recommendations = [
            (
                item['title'],
                f"Matched {resource_type} titled '{item['title']}' on topic '{item['topic']}' in {item['language']} "
                f"with rating {item['rating']} suitable for {user_type}."
            )
            for item in self.data
            if item['type'] == resource_type
               and topic in item['topic'].lower()
               and language in item['language'].lower()
               and item['rating'] >= min_rating
               and (  # User-specific preferences
                       (user_type == 'student' and resource_type == 'book') or
                       (user_type == 'teacher' and resource_type == 'journal') or
                       (user_type == 'researcher' and resource_type == 'article')
               )
        ]

        print(f"[DEBUG] Matched Recommendations: {recommendations}")

        # Declare recommendations and explanations fact
        if recommendations:
            self.declare(Fact(recommendation=[rec[0] for rec in recommendations],
                              explanation=[rec[1] for rec in recommendations]))
        else:
            self.declare(Fact(recommendation=["No resources found matching your criteria."],
                              explanation=["The system could not find any resources meeting all the provided criteria."]))

    @Rule(Fact(user_type='student'), Fact(resource_type='book'))
    def explain_student_books(self):
        """Explain rule for student book recommendations."""
        self.declare(Fact(rule_applied="Student-specific rule: Recommends books that align with the topic."))

    @Rule(Fact(user_type='teacher'), Fact(resource_type='journal'))
    def explain_teacher_journals(self):
        """Explain rule for teacher journal recommendations."""
        self.declare(Fact(rule_applied="Teacher-specific rule: Recommends journals that align with the topic."))

    @Rule(Fact(recommendation=MATCH.rec), Fact(explanation=MATCH.exp), salience=-1)
    def output_recommendation_with_explanation(self, rec, exp):
        """Output the recommendations with explanations."""
        print("Recommendations:")
        for i, recommendation in enumerate(rec):
            print(f"{i+1}. {recommendation}")
            print(f"   Explanation: {exp[i]}")
        print()

    @Rule(Fact(recommendation=MATCH.rec), salience=-2)
    def output_no_recommendations(self, rec):
        """Handle cases where no recommendations are found."""
        if rec == ["No resources found matching your criteria."]:
            print("No recommendations found.")
