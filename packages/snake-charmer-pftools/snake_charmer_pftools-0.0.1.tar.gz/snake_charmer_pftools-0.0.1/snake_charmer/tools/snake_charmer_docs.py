import sys
import logging
from promptflow import tool
from promptflow.entities import AzureOpenAIConnection
from pandasai import Agent, SmartDataframe
from pandasai.llm import AzureOpenAI
from pandas import pandas


@tool
def query_doc(document_id: str, query: str, connection: AzureOpenAIConnection, explain: bool = False) -> str:
    """Entry point for the query_doc function."""

    # Replace with your tool code.
    # Usually connection contains configs to connect to an API.
    # Use CustomConnection is a dict. You can use it like: connection.api_key, connection.api_base
    # Not all tools need a connection. You can remove it if you don't need it.

    # Create a smart dataframe from the file specified
    config = create_llm_config(connection)

    # Get the smart dataframe
    sdf = get_smart_dataframe(document_id, config)

    # Instantiate and agent to interact with the smart dataframe and
    # use the query to chat with the agent
    agent = Agent(sdf, config=config)
    agent_chat = agent.chat(query)

    # Initially just add the chat result to response
    result_parts = [agent_chat]

    # If the user wants and explanation though, grab that also and add
    # it on to the response
    if explain:
        agent_explain = agent.explain()
        result_parts.append(agent_explain)

    # Aggregate the parts of the response, log it and return it to the user
    result = "\n\n".join(result_parts)
    logging.info("Result: %s", result)
    return result


def get_smart_dataframe(document_id: str, config: dict) -> SmartDataframe:
    """Helper function to get a file based on an id and return a pandasai smart dataframe."""

    file_loc = "../data/Stock in Location.xlsx"
    df = pandas.read_excel(file_loc)
    sdf = SmartDataframe(df, config=config)

    return sdf


def create_llm_config(connection: AzureOpenAIConnection, deployment_name: str):
    """Helper function to create dataframe with Azure OpenAI or OpenAI services."""

    logging.info("Using Azure OpenAI: %s %s %s %s", 
                 deployment_name, 
                 connection.api_key, 
                 connection.api_base, 
                 connection.api_version)

    # Use the connection settings to create an Azure OpenAI interface
    llm = AzureOpenAI(
        api_base = connection.api_base, # AZURE_OPENAI_BASE_PATH            
        api_token = connection.api_key, # AZURE_OPENAI_API_KEY
        api_version = connection.api_version, # AZURE_OPENAI_API_VERSION
        deployment_name = deployment_name, # AZURE_OPENAI_API_DEPLOYMENT_NAME
        temperature = 0 # AZURE_OPENAI_TEMPERATURE
    )

    # Associate any additional settings with config payload and return it to be
    # used to instantiate a smart dataframe or agent
    return {
        "llm": llm, 
        "save_logs": False, 
        "enable_cache": False
        }


if __name__ == "__main__":
    print(query_doc(*sys.argv[1:]))
