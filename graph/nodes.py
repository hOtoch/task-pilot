from langchain_openai import ChatOpenAI
from .state import AgentState
import re
import json


llm = ChatOpenAI(model="gpt-4o")

def architect_node(state: AgentState):
    idea = state["project_idea"]
    platform = state["platform"]
    
    system_prompt = """
    Você é um Arquiteto de Sistemas e Gerente de Projetos Sênior. 
    Sua especialidade é decompor visões de produtos complexas em backlogs técnicos acionáveis.

    Use as seguintes tags XML para organizar sua resposta:
    <thinking>: Onde você planeja a decomposição, analisa dependências e define a prioridade.
    <tasks>: Onde você listará as tarefas estritamente em formato JSON.
    """

    user_content = f"""
    Analise a ideia de projeto abaixo e crie um backlog de tarefas para o {platform}.

    <project_idea>
    {idea}
    </project_idea>

    <instructions>
    1. Decomponha o projeto em no mínimo 5 tarefas granulares.
    2. Cada tarefa deve ter: 'title', 'description' (detalhada tecnicamente) e 'priority' (High, Medium, Low).
    3. No campo 'description', inclua critérios de aceitação básicos.
    4. Pense passo a passo antes de gerar o JSON final dentro da tag <thinking>.
    </instructions>

    <output_format>
    Retorne uma lista de objetos JSON dentro da tag <tasks>. Exemplo:
    [
        {{"title": "Setup Base de Dados", "description": "Configurar schema no PostgreSQL...", "priority": "High"}}
    ]
    </output_format>
    """

    response = llm.invoke([("system", system_prompt), ("user", user_content)])
    content = response.content

    # Extração de dados usando Regex (Prática recomendada para lidar com tags XML)
    tasks_match = re.search(r'<tasks>(.*?)</tasks>', content, re.DOTALL)

    if tasks_match:
        try:
            tasks_json = json.loads(tasks_match.group(1).strip())
        except json.JSONDecodeError:
            tasks_json = [{"title": "Erro na geração", "description": "O modelo falhou ao gerar JSON válido.", "priority": "High"}]
    else:
        tasks_json = []

    return {
        "tasks": tasks_json,
        "status": "architected"
    }