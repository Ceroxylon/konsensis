# Konsensis
A command line platform to get a second opinion of an LLM's response from itself or another LLM.

# Getting Started:

1. After cloning repo, add API keys to .env file in the format:
<pre>OPENAI_API_KEY={API KEY}
ANTHROPIC_API_KEY={API KEY}</pre>

2. Create venv environment and/or install dependencies in requirements.txt

# Usage:

1. Run Konsensis.py from the terminal of your choice (developed using zsh on MacOS):

<pre> % python3 Konsensis.py [OPTIONS] USER_QUESTION </pre>

Options:
<pre>
  --models TEXT                      /// Choose models to use: OpenAI is 1, Claude is 2 (use "1,2" for both, "2,1" to get the first answer from Claude)

                         
  --recursive                       ///  Enable recursive mode. This along with selecting a single model will feed the response back into the original model.

  
  --threshold INTEGER               ///  Enter a quality threshold (1-100). Things get interesting above 90 with the more sophisitcated models.

  
  --initial_prompt TEXT             ///  Enter an Initial System Prompt. This sets the intention, behavior, and purpse of the USER_QUESTION

   
  --help                            ///  Show this message and exit.
</pre>
The two models used to start this project are OpenAI GPT4 (Option 1), and Anthropic's Claude (option 2)

# EXAMPLE INPUT:

python3 Konsensis.py --models 1,2 --threshold 90 --initial_prompt "You are a professional tropical plant botanist." "Name 3 very rare palm trees from Madagascar"

# EXAMPLE OUTPUT:

Response from OPENAI: Madagascar is home to an incredibly rich diversity of flora and fauna, much of which is endemic to the island. Among its rare treasures are several palm species that are not only unique but also critically endangered. Here are three very rare palm species from Madagascar:

1. **Dypsis saintelucei** - This rare palm tree is known for its slender trunk and relatively small size compared to other palms. It is limited to a very specific region in Madagascar and faces threats from habitat destruction and over-collecting. Its precise habitat requirements and limited distribution make it especially vulnerable.

2. **Tahina spectabilis** - Also known as the "Dimaka" palm or Tahina palm, this species was only discovered in 2007 in northwestern Madagascar. It is remarkable not only for its rarity but also for its spectacular life cycle; the palm grows for several decades before flowering once and then dying. Its habitat is restricted, and with only a few hundred individuals known, it is considered critically endangered. The discovery of Tahina spectabilis has been a significant event in the botanical world due to its unique characteristics and the urgency to conserve it.

3. **Voanioala gerardii** - Commonly referred to as the "Forest Coconut," this species is found in a limited area of northeastern Madagascar's lowland rainforests. It is critically endangered, primarily due to habitat loss and its very low reproduction rate. Voanioala gerardii has a very distinct appearance, with a large, robust trunk and leaves that can grow several meters long. Its seeds, resembling coconuts, are the largest among all the palm species in Madagascar, but unfortunately, this has also made it a target for collectors, further endangering its survival. [...]

Response from ANTHROPIC: 95

Final response meets threshold: 95.0

Accepted answer: Madagascar is home to an incredibly rich [...]

