# import loadenv


from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch

from langchain import hub
from langchain.agents import initialize_agent, AgentExecutor, create_react_agent
from langchain_core.output_parsers.pydantic import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda


from prompt import REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS
from schemas import AgentResponse


def main():
    print("Hello from langchain-course!")
    load_dotenv()


    # Initialize the LLM
    llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.5,
    )

    # define the tools to be used by the agent
    tools = [
        TavilySearch()
    ]
    # Define prompt
 
    output_parser = PydanticOutputParser(pydantic_object=AgentResponse)
    react_format_instructions = PromptTemplate(
        template=REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS,
        input_variables=["input", "agent_scratchpad", "tool_names"]
    ).partial(
        react_format_instructions=output_parser.get_format_instructions()

    )


    #create the agent / chain 

    agent = create_react_agent(
        llm=llm,
        tools = tools,
        prompt = react_format_instructions
    )
    
    agent_executor = AgentExecutor(
        agent=agent, 
        tools=tools,
        handle_parsing_errors=True,

        verbose=True
    )

    extract_output = RunnableLambda(
        lambda x: x["output"]
    )
    parse_output = RunnableLambda(lambda x: output_parser.parse(x))
    chain = agent_executor | extract_output | parse_output



    response = chain.invoke(
        {
         "input": "search for 3 job postings for an ai engineer using langchain in the bay area on linkedin and list their details"
        }
    )
    print(response)
   

if __name__ == "__main__":
    main()
