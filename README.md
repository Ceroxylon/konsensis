# konsensis
A command line platform to get a second opinion of a LLM's response from itself or another LLM.

# Getting Started:

1. After cloning repo, add API keys to .env file in the format:
OPENAI_API_KEY=<API KEY>
ANTHROPIC_API_KEY=<API KEY>

2. Create venv environment and/or install dependencies in requirements.txt

3. Run konsensis.py from the terminal of your choice (tested on zsh):

   $ python3 konsensis.py

# Using the tool:

1. Follow the prompts to give the initial instructions to get the conversation started:
- Choose models to use: For now only OpenAI's GPT4 and Anthropic's Claude are supported as a proof of concept, but it will be easy to add more later (HF and local models are next).
Enter in 1,2 for GPT4 to give the initial response and Claude be the grader, or 2,1 for the other way around. Getting one or either to grade itself is accomplished with "recursive mode"
  
- Enable recursive mode? (yes/no): This will get a model to grade itself.
  
- Enter a quality threshold (1-100): Claude seems to think the average GPT4 response is around 90, so the range from 90-100 is where things heat up.
  
- Enter an initial system prompt: This is the starting prompt that lets you outline the scope, personality, and mission of the inital model's response.
  
- Enter your prompt: Finally, enter in the prompt that you want to assess. It will display the initial response, the grade, and either pass or fail depending on the threshold you require.
