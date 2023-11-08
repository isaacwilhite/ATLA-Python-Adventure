import random

def get_element(answers):
    """
    Calculate the element based on the answers provided.
    :param answers: list of answers provided by the user
    :return: the calculated element
    """
    scores = {'Water': 0, 'Earth': 0, 'Fire': 0, 'Air': 0}

    for answer in answers:
        scores[answer] += 1

    # In case of a tie, we'll pick a random element from the tied elements
    max_score = max(scores.values())
    potential_elements = [element for element, score in scores.items() if score == max_score]
    return random.choice(potential_elements)

def main():
    questions = [
        "When faced with a challenge, you:",
        "What is your preferred climate?",
        "In a group project, you are:",
        "Your favorite time of day is:",
        "When learning new things, you prefer:",
        "You feel most at peace when:",
        "In stressful situations, you:",
        "Which animal do you feel most connected to?"
    ]

    options = {
        'A': ["Flow around it and find the path of least resistance.", "Humid and rainy.", "Adaptable and cooperative.", "Twilight, when the night meets the day.", "Watching and mimicking.", "You're near a body of water.", "Remain calm and use diplomacy.", "Dolphin or fish."],
        'B': ["Stand firm and confront it head-on.", "Mountainous and stable.", "Dependable and organized.", "Noon, when the sun is at its peak.", "Hands-on experience.", "You're surrounded by nature and wildlife.", "Are stable and look for practical solutions.", "Badger or ox."],
        'C': ["Power through it with sheer force.", "Warm and sunny.", "Ambitious and motivating.", "Sunrise, the start of a new day.", "Challenges that test your abilities.", "You're engaged in a passionate discussion or activity.", "Take charge and lead others.", "Dragon or phoenix."],
        'D': ["Find a creative and peaceful solution.", "Breezy and open.", "Harmonious and idea-driven.", "Early morning, when the world is waking up.", "Theoretical and abstract concepts.", "You have the freedom to explore and roam.", "Try to ease tension with humor or diversion.", "Bird or butterfly."]
    }

    answers = []

    print("Welcome to the Avatar Element Quiz!\nAnswer the following questions to discover your element:")

    for i, question in enumerate(questions):
        print(f"\nQuestion {i+1}: {question}")

        # Shuffle the answer keys to randomize the order
        answer_keys = list(options.keys())
        random.shuffle(answer_keys)

        # Display the options in the randomized order
        for key in answer_keys:
            print(f"{key}. {options[key][i]}")

        answer = input("Choose your answer (A, B, C, D): ").strip().upper()
        while answer not in answer_keys:
            print("Invalid answer. Please select A, B, C, or D.")
            answer = input("Choose your answer (A, B, C, D): ").strip().upper()

        # Save the element corresponding to the chosen answer
        if answer == 'A':
            answers.append('Water')
        elif answer == 'B':
            answers.append('Earth')
        elif answer == 'C':
            answers.append('Fire')
        elif answer == 'D':
            answers.append('Air')

    # Calculate the resulting element
    element = get_element(answers)
    print(f"\nYour element is: {element}")

if __name__ == "__main__":
    main()
