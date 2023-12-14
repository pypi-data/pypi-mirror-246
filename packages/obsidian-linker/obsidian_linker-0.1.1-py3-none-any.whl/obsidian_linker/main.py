import os
import openai
from typing import List
from dotenv import load_dotenv
import re
import click

load_dotenv()


# Set up the OpenAI client with your API key
def get_openai_client():
    return openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def extract_first_500_words(text: str) -> str:
    """Extract the first 500 words from a given text."""
    return " ".join(text.split()[:500])


def wrap_keywords_in_brackets(text: str, keywords: List[str]) -> str:
    """Wrap the identified keywords in double brackets."""
    keywords_wrapped = 0
    for keyword in keywords:
        if re.match("^[A-Za-z ]*$", keyword) and keyword in text:
            text = text.replace(keyword, f"[[{keyword}]]", 1)
            keywords_wrapped += 1
            if keywords_wrapped >= 5:
                break
    return text


def analyze_text(text: str, openai_client) -> List[str]:
    try:
        response = openai_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": """
            Extract 3-5 MEANINGFUL and RELEVANT keywords,
            WORDS ONLY - NO NUMBERS OR SPECIAL CHARACTERS,
            preferably 2-3 word phrases,
            4 words MAXIMUM,
            from the following text:""",
                },
                {"role": "user", "content": text},
            ],
            model="gpt-3.5-turbo-16k",
            max_tokens=8000,
        )
        keywords = response.choices[0].message.content.strip().split(", ")
        print(f"Extracted keywords: {keywords}")
        return keywords
    except openai.BadRequestError:
        print("Text is too long, skipping")
        return []


@click.command()
@click.option(
    "--directory",
    prompt="Directory path",
    help="The directory to process markdown files.",
)
def process_markdown_files(directory: str):
    """Process all markdown files in the given directory."""
    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            filepath = os.path.join(directory, filename)
            with open(filepath, "r", encoding="utf-8") as file:
                content = file.read()

            first_500_words = extract_first_500_words(content)
            openai_client = get_openai_client()
            keywords = analyze_text(first_500_words, openai_client)
            if not keywords:
                print(f"No keywords found for {filename}, skipping")
                continue
            modified_content = wrap_keywords_in_brackets(content, keywords)

            with open(filepath, "w", encoding="utf-8") as file:
                file.write(modified_content)
            print(f"Processed {filename}")


def main():
    process_markdown_files()


if __name__ == "__main__":
    main()
