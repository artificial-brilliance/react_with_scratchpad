
import sys

from react_with_scratchpad.prompt import buildSystemPrompt, Tool
from react_with_scratchpad.search import Search
from react_with_scratchpad.react_runner import ReactRunner

def main(task: str):
    searcher = Search(log=lambda x: print(f"* {x}"))
    tools = [Tool(
        name="search",
        input_description="The query used to search wikipedia",
        tool_description="Used to search wikipedia",
    )]
    system_prompt = buildSystemPrompt(task, tools)
    answer = ReactRunner(
        actions={
            "search": lambda query: searcher.search(query),
        },
        log=lambda x: print(f"> {x}"),
        system_prompt=system_prompt,
        max_iterations=10,
    ).run()
    if answer is None:
        print("\nCould not determine the answer within the max number of iterations")
    else:
        print(f"\nFinal Answer: {answer}")

if len(sys.argv) < 2:
    print("A task must be specified")
    exit(1)

task = ""
for i in range(1, len(sys.argv)):
    task += sys.argv[i] + " "

main(task)
