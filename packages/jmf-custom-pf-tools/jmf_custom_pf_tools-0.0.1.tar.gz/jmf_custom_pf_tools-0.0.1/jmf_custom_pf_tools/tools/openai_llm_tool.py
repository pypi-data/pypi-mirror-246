from jinja2 import Template
from promptflow import tool
from promptflow.connections import CustomConnection
from promptflow.contracts.types import PromptTemplate
from openai import AzureOpenAI

@tool
def openai_chat(client: AzureOpenAI, seed: int, prompt: PromptTemplate, 
                model_deployment_name:str = 'gpt-35-turbo' , **kwargs) -> str:
    rendered_prompt = Template(prompt, trim_blocks=True, keep_trailing_newline=True).render(**kwargs)
    
    response = client.chat.completions.create(
                model=model_deployment_name,
                messages=[{"role": "system", "content": ''},
                        {"role": "user","content": rendered_prompt}
                    ],
                seed=seed)
    results = response.choices[0].message.content
    return results