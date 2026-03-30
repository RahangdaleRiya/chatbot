from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

class SupportAgent:
    def __init__(self, config):
        self.llm = OllamaLLM(
            base_url=config['ollama']['host'],
            model=config['ollama']['llm_model']
        )
        self.prompt = PromptTemplate(
            input_variables=["message", "ticket_info", "kb_results"],
            template="""
You are a customer support agent. Help the customer with their issue.

User message: {message}

Ticket info: {ticket_info}

Relevant knowledge base articles: {kb_results}

Provide a helpful response.
"""
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def generate_response(self, message, ticket_info, kb_results):
        ticket_str = str(ticket_info) if ticket_info else "No ticket provided"
        kb_str = "\n".join([f"- {r['title']}: {r['content'][:200]}..." for r in kb_results])
        return self.chain.run(message=message, ticket_info=ticket_str, kb_results=kb_str)