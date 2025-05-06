# __Autism Parent Helper (RAG Chatbot)__

__TODO:__ 
* Explore sentence clustering / non-DL / naive approaches for data cleaning / organization
* Switch Database type
* Shift to a different deployment platform / migrate to a blog website (odidya?)

### _Description:_
Parents of children diagnosed with autism often face confusion about their child’s condition, especially with nonverbal children—how do i help them communicate? Are there better strategies for gauging their learning?. These questions are rarely answered, with minimal tools that directly educate parents of both verbal and nonverbal special needs children. Although tools and datasets exist to support speech and early autism detection, a comprehensive educational solution remains lacking.

### _Data Sources:_ 
Lived experiences and firsthand accounts are of paramount importance. This project draws insights from such information, specifically through the following sources:
- *Sincerely, Your Autistic Child* – Emily Paige Ballou, Sharon daVanport, Morénike Giwa Onaiwu  
- *Plankton Dreams* – Mukhopadhyay  
- *Leaders Around Me* – Edlyn Peña  
- *Communication Alternatives in Autism* – Edlyn Vallejo Peña  
- *Look Me In The Eye* – John Elder Robison  
- *Loud Hands: Autistic People, Speaking* – Julia Bascom  
- *Thinking in Pictures* – Temple Grandin  
- *The Reason I Jump* – Naoki Higashida

### _Design Decisions:_
The approach uses the above sources as a corpus for a RAG Chatbot powered by Cohere’s Aya Expanse. Users ask a question, which is searched via cosine similarity in a ChromaDB vector store of our source material. The retrieved context is added to the question to form a prompt, passed to the model for an answer. For chunking, OpenAI’s embedding-based semantic chunking struck the best balance between character limits and computational cost. Aya Expanse (8B) was used locally via Ollama for testing and Hugging Face for deployment. LangChain's PDF loader processed the sources into `Document` pages, which were semantically chunked. Appendices and TOCs were excluded to keep search results relevant.

### _Modeling Approach & Results:_
The deep learning RAG chatbot's identity comes from a simple, prompt-based input and clear output based on writing from autistic individuals and trusted community voices—unlike confusing advice from traditional organizations.

Running Aya Expanse locally via Ollama and LangChain yielded strong results. However, switching to Hugging Face’s inference API revealed issues: NUL characters from database retrieval were breaking outputs. These weren’t picked up locally but impacted the API, so preprocessing was added to strip them out.

Results:
- **DL (Aya)**: As expected, this performed best, enabling context-aware generation. Evaluated via LLM judgment and feedback from two parents of special needs children—results were great.

### _Why is RAG the only viable approach?_
The RAG chatbot was the only viable approach for this task because both the naive and non-deep learning (non-DL) methods were far too simplistic as a means for generating text while gauging contextual nuance and situations where a word's meaning can be changed between homonyms, synonyms and antonyms (a common problem for these approaches). The naive method, primarily used for surface-level similarity via the Jaccard score, could only identify exact or near-exact sentence matches. For obvious reasons, this fails to capture deeper semantic meaning/contextuality. The non-DL approach, which attempted topic modeling and clustering using methods like Hidden Markov Models (HMMs), struggled with convergence and produced overly simplistic groupings, often based on sentence length because of the complex corpus of autobiographical information. These methods also lacked the capacity for natural language understanding or generation, making them unusable for producing helpful answers. Alternatively, the RAG framework, paired with our LLM, allowed for coherent answer generation—making it the only approach capable of handling the task.

### _How do I run this project?_
#### Run Locally
To run the chatbot locally using the Aya Expanse model:

```bash
python scripts/main
```

from the project's root directory.

Make sure you have the `aya-expanse:latest` model running on your local Ollama instance.

#### Running Tests Locally
To run the test suite:

```bash
python tests
```

#### Website Link
You can also access the deployed version here:  
[[Render Link](https://nlp-aph.onrender.com)]