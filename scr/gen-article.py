from typing import Union, List
from langchain.agents import Tool
from langchain.agents import AgentType
from langchain.memory import ConversationBufferMemory
from langchain import OpenAI
from langchain.utilities import SerpAPIWrapper
from langchain.agents import initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool, AgentOutputParser
from langchain.chains import RetrievalQA
from langchain.agents import AgentType
from langchain.schema import AgentAction, AgentFinish
from langchain.memory import ConversationBufferMemory
from langchain.prompts import StringPromptTemplate
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser
from langchain.prompts import StringPromptTemplate
from langchain.schema import AgentAction, AgentFinish, OutputParserException
from langchain import LLMChain
from webscrape import scrape_team_links, scrape_rosters, scrape_random_game_this_week
import os, random, re

config = {
    "articles_to_write": "3",
    "current_week" : "1"
}

llm = ChatOpenAI(temperature=0, model_name="gpt-4")

# Disabling search until I test this more, since I only get 100 free per month.
#search = SerpAPIWrapper()
tools = [
    # Tool(
    #     name = "Current Search",
    #     func=search.run,
    #     description="useful for when you need to answer questions about current events or the current state of the world"
    # ),
]

class CustomPromptTemplate(StringPromptTemplate):
    # The template to use
    template: str
    # The list of tools available
    tools: List[Tool]

    def format(self, **kwargs) -> str:
        # Get the intermediate steps (AgentAction, Observation tuples)
        # Format them in a particular way
        intermediate_steps = kwargs.pop("intermediate_steps")
        thoughts = ""
        for action, observation in intermediate_steps:
            thoughts += action.log
            thoughts += f"\nObservation: {observation}\nThought: "
        # Set the agent_scratchpad variable to that value
        kwargs["agent_scratchpad"] = thoughts
        # Create a tools variable from the list of tools provided
        kwargs["tools"] = "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])
        # Create a list of tool names for the tools provided
        kwargs["tool_names"] = ", ".join([tool.name for tool in self.tools])
        return self.template.format(**kwargs)


template = """You are a sports analyst for college football.
    You will provide expert analysis on what to expect during the game, making sure to carefully use the correct information based on what is provided to you on the two teams.
    Be sure to be very critical and doubtful of teams in the SEC conference, and very confident in ACC teams.
    You have access to the following tools:

    {tools}

    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    You will receive information in this format:
    TEAM A: (team name)
    Favored by: (favored by)
    TEAM B: (team name)
    Favored by: (favored by)

    Begin! Remember to give you expert opinion on who will win, and key moments in the game. Use inflammatory language. Mention player names. Be emotional. Remember that you have to abide by the Favored by, even if you don't think the favored team will win. Go!

    Input: {input}
    {agent_scratchpad}
"""

class CustomOutputParser(AgentOutputParser):

    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        # Check if agent should finish
        if "Final Answer:" in llm_output:
            return AgentFinish(
                # Return values is generally always a dictionary with a single `output` key
                # It is not recommended to try anything else at the moment :)
                return_values={"output": llm_output.split("Final Answer:")[-1].strip()},
                log=llm_output,
            )
        # Parse out the action and action input
        regex = r"Action\s*\d*\s*:(.*?)\nAction\s*\d*\s*Input\s*\d*\s*:[\s]*(.*)"
        match = re.search(regex, llm_output, re.DOTALL)
        if not match:
            raise OutputParserException(f"Could not parse LLM output: `{llm_output}`")
        action = match.group(1).strip()
        action_input = match.group(2)
        # Return the action and action input
        return AgentAction(tool=action, tool_input=action_input.strip(" ").strip('"'), log=llm_output)

prompt = CustomPromptTemplate(
    template=template,
    tools=tools,
    # This omits the `agent_scratchpad`, `tools`, and `tool_names` variables because those are generated dynamically
    # This includes the `intermediate_steps` variable because that is needed
    input_variables=["input", "intermediate_steps"]
)

def output_to_md(content, team_1, team_2):
    markdown_content = f"""
    ## {team_1} vs {team_2}

    This is a sample Markdown file created using Python.

    ## Our Prediction

    {content}
    """

def main():
    #links = scrape_team_links()
    #rosters = scrape_rosters(links)
    current_week = config['current_week']
    total_articles = int(config['articles_to_write'])
    list_of_teams_to_write_about = scrape_random_game_this_week(current_week)
    articles = random.sample(list_of_teams_to_write_about, total_articles)
    print(articles)
    agent_chain = initialize_agent(tools, llm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, verbose=True)
    output_parser = CustomOutputParser()
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    tool_names = [tool.name for tool in tools]
    agent = LLMSingleActionAgent(
        llm_chain=llm_chain,
        output_parser=output_parser,
        stop=["\nObservation:"],
        allowed_tools=tool_names
    )
    agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True)

    valid_spreads = [3, 6.5, 7, 10, 13.5, 14, 17, 20, 24, 27, 28, 31, 35, 41, 45]

    for article in articles:
        # Generate a random point spread from the valid_spreads list
        point_spread = random.choice(valid_spreads)
        print("Generated Point Spread:", point_spread)

        team1 = article[0]
        team2 = article[1]
        team1_point_spread = point_spread
        team2_point_spread = -point_spread

        input_game_facts = f"""
        WEEK: {current_week}
        TEAM NAME: {team1}
        Favored by: {team1_point_spread}

        TEAM NAME: {team2}
        Favored by: {team2_point_spread}
        """
        input_game_takeaways = f"""
        What are some weird considerations of the upcoming CFB {current_week} {team1} vs {team2}?
        """
        game_resp = agent_executor.run(input_game_facts)
        print(game_resp)
        takeaway_resp = agent_executor.run(input_game_takeaways)
        article_content = f"""

        # {current_week}: {team1} vs {team2}

        ## Our Take

        {game_resp}

        ## Key Considerations

        {takeaway_resp}

        ## Our Point Spread

        Our spread predicts {team1} by {team1_point_spread}.
        """

        file_name = f"posts/{current_week}-{team1}-vs-{team2}.md".strip()

        with open(file_name, "w") as file:
            file.write(article_content)

        print(f"Markdown content has been written to '{file_name}'.")

if __name__=='__main__':
    main()