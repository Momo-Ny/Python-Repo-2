import os
from pydantic import BaseModel, Field
from typing import List
from groq import Groq
import instructor


class Response(BaseModel):
    answer: str = Field(..., description="The answer to the user's question")


def get_groq_response(question: str) -> str:
    # Initialize Groq client
    client = Groq(
        api_key=os.environ.get('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'),
    )
   
    # Enable instructor integration
    client = instructor.from_groq(client, mode=instructor.Mode.TOOLS)
   
    # Make API call
    resp = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[
            {
                "role": "user",
                "content": question,
            }
        ],
        response_model=Response,
    )
    return resp.answer


def main():
    # Check for API key
    if not os.environ.get('GROQ_API_KEY'):
        print("Please set your GROQ_API_KEY environment variable")
        return
   
    print("Welcome to Groq Chat! Type 'quit' to exit.")
   
    # Main conversation loop
    while True:
        # Get user input
        question = input("\nYou: ")
       
        # Check for quit command
        if question.lower() == 'quit':
            print("Goodbye!")
            break
           
        try:
            # Get and print response
            response = get_groq_response(question)
            print(f"\nGroq: {response}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")


if _name_ == "_main_":
    main()
