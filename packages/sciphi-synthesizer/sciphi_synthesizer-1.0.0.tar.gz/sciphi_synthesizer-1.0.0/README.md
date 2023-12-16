# Synthesizer[ΨΦ]: A multi-purpose LLM framework 💡

<p align="center">
<img width="716" alt="SciPhi Logo" src="https://github.com/emrgnt-cmplxty/sciphi/assets/68796651/195367d8-54fd-4281-ace0-87ea8523f982">
</p>

With Synthesizer, users can:

- **Custom Data Creation**: Generate datasets via LLMs that are tailored to your needs.
   - Anthropic, OpenAI, vLLM, and HuggingFace.
- **Retrieval-Augmented Generation (RAG) on Demand**: Built-in RAG Provider Interface to anchor generated data to real-world sources. 
   - Turnkey integration with Agent Search API. 
- **Custom Data Creation**: Generate datasets via LLMs that are tailored to your needs, for LLM training, RAG, and more.

---

## Documentation

For more detailed information, tutorials, and API references, please visit the official [Synthesizer Documentation](https://sciphi.readthedocs.io/en/latest/).

## Fast Setup

```bash
pip install sciphi-synthesizer
```
## Features

### Community & Support

- Engage with our vibrant community on [Discord](https://discord.gg/j9GxfbxqAe).
- For tailored inquiries or feedback, please [email us](mailto:owen@sciphi.ai).


### Example

The following example demonstrates how to construct a connection to the AgentSearch API with the synthesizer RAG interface. Then, the example goes on to use the RAG interface to generate a response with an OpenAI hosted LLM.

```python

   from synthesizer.core import LLMProviderName, RAGProviderName
   from synthesizer.interface import (
      LLMInterfaceManager,
      RAGInterfaceManager,
   )
   from synthesizer.llm import GenerationConfig

   # RAG Provider Settings
   rag_interface = RAGInterfaceManager.get_interface_from_args(
      RAGProviderName(rag_provider_name),
      api_base=rag_api_base,
      limit_hierarchical_url_results=rag_limit_hierarchical_url_results,
      limit_final_pagerank_results=rag_limit_final_pagerank_results,
   )
   rag_context = rag_interface.get_rag_context(query)

   # LLM Provider Settings
   llm_interface = LLMInterfaceManager.get_interface_from_args(
      LLMProviderName(llm_provider_name),
   )

   generation_config = GenerationConfig(
      model_name=llm_model_name,
      max_tokens_to_sample=llm_max_tokens_to_sample,
      temperature=llm_temperature,
      top_p=llm_top_p,
      # other generation params here ...
   )

   formatted_prompt = rag_prompt.format(rag_context=rag_context)
   completion = llm_interface.get_completion(
      formatted_prompt, generation_config
   )
   print(completion)
```
