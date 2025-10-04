import os
from dotenv import load_dotenv

# Add references
# Add references
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from openai import AzureOpenAI

def main(): 

    # Clear the console
    os.system('cls' if os.name=='nt' else 'clear')
        
    try: 
    
        # Get configuration settings 
        load_dotenv()
        project_endpoint = os.getenv("PROJECT_ENDPOINT")
        model_deployment =  os.getenv("MODEL_DEPLOYMENT")

        # Initialize the project client
        project_client = AIProjectClient(            
            credential=DefaultAzureCredential(
                exclude_environment_credential=True,
                exclude_managed_identity_credential=True
            ),
            endpoint=project_endpoint,
        )

        # Get a chat client
        openai_client = project_client.get_openai_client(api_version="2024-10-21")

        # Initialize prompt with system message
        prompt = [
                 {"role": "system", "content": "You are a helpful AI assistant that answers questions."}
        ]

        # Loop until the user types 'quit'
        while True:
            # Get input text
            input_text = input("Enter the prompt (or type 'quit' to exit): ")
            if input_text.lower() == "quit":
                break
            if len(input_text) == 0:
                print("Please enter a prompt.")
                continue
            
            # Get a chat completion
            append_message = {"role": "user", "content": input_text}
            prompt.append(append_message)
            response = openai_client.chat.completions.create(
                model=model_deployment,
                messages=prompt
            )
            completion_text = response.choices[0].message.content
            print(f"Response: {completion_text}\n")
            prompt.append({"role": "assistant", "content": completion_text})
            
    except Exception as ex:
        print(ex)

if __name__ == '__main__': 
    main()