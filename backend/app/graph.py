import langgraph
from app.main import call_deepseek


def get_user_input():
    user_input = input("What would you like to learn? ")
    return user_input

def analyze_input(input_text):
    prompt = f"Extract the main learning goals or skills from: '{input_text}'."
    markers = call_deepseek(prompt)
    print(f"Markers found: {markers}")
    return markers

def ask_for_missing_markers():
    clarification = input("Please clarify or add more details: ")
    return clarification

def generate_subskill_prompts(markers):
    prompt = f"For each of these skills: {markers}, list 2-3 important sub-skills."
    subskills = call_deepseek(prompt)
    print(f"Sub-skills: {subskills}")
    return subskills

def search_skills(prompts):
    # For now, just echo the prompts
    print(f"Searching for: {prompts}")
    return prompts

def select_and_organize(skills):
    # For now, just echo the skills
    print(f"Selected skills: {skills}")
    return skills

def display_roadmap(roadmap):
    print("\n--- Your Learning Roadmap ---")
    print(roadmap)

def main():
    user_input = get_user_input()
    markers = analyze_input(user_input)
    # Optionally, add logic to check if markers are missing and call ask_for_missing_markers()
    subskills = generate_subskill_prompts(markers)
    searched = search_skills(subskills)
    selected = select_and_organize(searched)
    display_roadmap(selected)

if __name__ == "__main__":
    main()