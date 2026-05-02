from langchain_deepseek import ChatDeepSeek
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from app.config import settings
from app.retriever import retriever

@tool
def search_knowledge_base(query: str) -> str:
    """Searches the knowledge base for relevant information about real estate projects."""
    return retriever.search(query)

class RAGAgent:
    def __init__(self):
        self.llm = ChatDeepSeek(
            model=settings.DEEPSEEK_MODEL,
            api_key=settings.DEEPSEEK_API_KEY,
            temperature=0
        )
        self.tools = [search_knowledge_base]
        self.memory_store = {}
        self.agent_executor = self._create_executor()

    def _create_executor(self):
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful real estate assistant. Use the tool to find information about real estate projects."),
            ("system", f"extract unit specs, and meta data from user question;"),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        agent = create_tool_calling_agent(self.llm, self.tools, prompt)
        return AgentExecutor(agent=agent, tools=self.tools)

    def _get_session_history(self, session_id: str):
        if session_id not in self.memory_store:
            self.memory_store[session_id] = ChatMessageHistory()
        return self.memory_store[session_id]

    def chat(self, session_id: str, message: str):
        runnable = RunnableWithMessageHistory(
            self.agent_executor,
            self._get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
        )
        response = runnable.invoke(
            {"input": message},
            config={"configurable": {"session_id": session_id}}
        )
        return response["output"]

agent_service = RAGAgent()
