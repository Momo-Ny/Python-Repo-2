import os
from pydantic import BaseModel, Field
from typing import List
from groq import Groq
import instructor


class Character(BaseModel):
    name: str
    fact: List[str] = Field(..., description="A list of facts about the subject")


def get_groq_response(question: str) -> Character:
    # Initialize Groq client
    client = Groq(
        api_key=os.environ.get('GROQ_API_KEY'),  # Ensure API key is set
    )

    # Enable instructor integration
    client = instructor.from_groq(client, mode=instructor.Mode.TOOLS)

    # Make API call
    resp = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[{"role": "user", "content": question}],
        response_model=Character,
    )
    
    return resp


def main():
    # Check if API key is set
    if not os.environ.get('GROQ_API_KEY'):
        print("Please set your GROQ_API_KEY environment variable.")
        return

    print("Welcome! Type the subject that you want to know about or type 'quit' to exit.")

    while True:
        # Get user input
        question = input("\nYou: ")

        # Exit condition
        if question.lower() == "quit":
            print("Goodbye!")
            break

        try:
            # Get response
            response = get_groq_response(question)
            print(f"\nGroq: {response.model_dump_json(indent=2)}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
