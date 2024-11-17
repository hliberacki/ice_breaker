from dotenv import load_dotenv
import os
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI

from third_parties.linkedin import scrape_linkedin_profile


def generate_summary():
    summary_template = """
  Given the LinkedIn information {information} about a person, I would like to create:
  1. a short summary
  2. two intresting facts about them
  """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found. Ensure it's set in the .env file.")

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", openai_api_key=api_key)

    chain = summary_prompt_template | llm
    linkedin_data = scrape_linkedin_profile(
        profile_url="https://www.linkedin.com/in/hubert-liberacki-07183580/"
    )
    res = chain.invoke(input={"information": linkedin_data})

    print(res)


def main():
    generate_summary()


if __name__ == "__main__":
    load_dotenv()
    main()
