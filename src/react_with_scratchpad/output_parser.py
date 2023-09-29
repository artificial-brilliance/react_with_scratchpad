import re

from typing import Dict, Tuple

KEY_VALUE_REGEX = re.compile("^([\\w ]+):(.*)$")

def parseOutput(output: str) -> Tuple[str, Dict[str, str]]:
    lines = output.split('\n')
    text = ''
    for line in lines:
        if line.startswith('Observation:'):
            break
        text += line + '\n'
    return text.strip(), parseOutputValues(text)

def parseOutputValues(output: str) -> Dict[str, str]:
    """
    Used to parse the output from an LLM and identify keys and
    values in text that looks like the following:
    ```
    Thought: some thought
    Action: some action
    Action Input: some action input
    Observation: some observation
    ```
    For that input, the output from this function will be:
    ```
    {
      "Thought": "some thought",
      "Action": "some action",
      "Action Input": "some action input",
      "Observation": "some observation"
    }
    ```
    Note: If the input has repeated keys, the FIRST value is used,
    i.e. given the input:
    ```
    Some Key: some value 1
    Some Key: some value 2
    ```
    then the output is:
    ```
    {
      "Some Key": "some value 1"
    }
    ```
    """

    result = {}
    lines = output.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]
        i += 1
        regexMatch = KEY_VALUE_REGEX.match(line)
        if not regexMatch:
            continue
        key, value = regexMatch.groups()
        text = value
        while i < len(lines) and KEY_VALUE_REGEX.match(lines[i]) is None:
            text += '\n' + lines[i]
            i += 1
        result[key] = text.strip()
    return result
