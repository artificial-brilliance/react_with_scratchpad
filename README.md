# React with Scratchpad

This codebase demonstrates a way to implement the ReAct (Reason+Action) framework for interacting with Large Language Models (LLMs) to produce better responses to inputs by utilizing a scratchpad to help address the problem of the model hallucinating observations.

See the [artificial-brilliance/react](https://github.com/artificial-brilliance/react) repo for a demonstration of the ReAct framework using the Thought/Action/Observation pattern.

The code is inspired from a mixture approaches from the following along
with custom tweaks and additions:
* [The original ReAct paper](https://arxiv.org/abs/2210.03629)
* [Simon Willison's blog](https://til.simonwillison.net/llms/python-react-pattern)
* [LangChain](https://www.langchain.com)

## Usage

This repository was written using Python 3.11 and uses the [pdm](https://pdm.fming.dev) tool to handle dependencies.

To get started
1. Clone the repo:
   ```
     git clone git@github.com:artificial-brilliance/inverted_react.git
   ```
2. At the root of the repo, install necessary dependencies:
   ```
     pdm install
   ```
3. At the root of the repo, run the code with:
   ```
     pdm run start '<some question to answer>'
   ```
4. (Optionally) run tests using:
   ```
     pdm run test
   ```

## Examples

The following example shows what happens when asking the LLM a question that it cannot know because (at the time the code was run) the iphone 15 was not released yet and descriptions of its release date were (most-likely) not in any training data.

```yaml
$ pdm run start 'when was the iphone 15 released'
> System Prompt:
You are an assistant helping a human.

Your task is to answer the following:
when was the iphone 15 released

You use a Thought/Action/Action Input/Observation pattern:
'''
Thought: The thought you are having based on the observation
Action: The action you want to take.  One of [search]
Action Input: The input to the action
Observation: An observation
'''

(...this Thought/Action/Action Input/Observation pattern can repeat N times)

== TOOLS ==

You have access to the following tools:


Tool 1:
Action: search
Action Input: The query used to search wikipedia
Description: Used to search wikipedia



== OPTIONS ==

Select ONLY ONE option below:

Option 1: To use a tool, you MUST use the following format:
'''
Thought: Do I need to use a tool? Yes because of the observation [the reason why you need to use a tool...]
Action: MUST be one of [search]
Action Input: The input to the tool
Observation: The observation from the action
'''

Option 2: To output the final answer, you MUST use the following format:
'''
Final Answer: The final answer for the task
'''



> Scratchpad:

> Running: search "iPhone 15 release date"
* Cache hit for query ""iPhone 15 release date""
> Scratchpad:

Thought: Do I need to use a tool? Yes, because I don't know the release date of the iPhone 15.
Action: search
Action Input: "iPhone 15 release date"
Observation: Friday, September 15 (updated) Eastern and 1 p.m. U.K. Despite persistent rumors that the iPhone 15 Pro Max would be delayed. it's due for September 22 as well, though I think it's possible that it may be in short supply, so prompt pre-ordering is suggested to avoid delays.Sep 12, 2023

Final Answer: The iPhone 15 was released on September 22, 2023.
```
