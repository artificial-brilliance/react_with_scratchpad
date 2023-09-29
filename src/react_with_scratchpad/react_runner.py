
import re

from dataclasses import dataclass
from typing import Callable, Optional, Dict

from react_with_scratchpad.llm import complete
from react_with_scratchpad.output_parser import parseOutput

KEY_VALUE_REGEX = re.compile("^([\\w ]+):(.*)$")

FINAL_ANSWER = "Final Answer"
ACTION = "Action"
ACTION_INPUT = "Action Input"
OBSERVATION = "Observation"

@dataclass
class ReactRunner(object):
    # The actions (i.e. tools) that the LLM can perform/run
    # The key is the name of the tool and the value is the callable
    # to run for that tool
    actions: Dict[str, Callable[[str], str]]
    # The system prompt that describes what the LLM should do
    system_prompt: str
    # A callable that is called whenever a log statement is made
    log: Callable[[str], None]
    # The max number of react loops that will be performed
    # This helps prevent infinite loops
    max_iterations: int

    def run(self) -> Optional[str]:
        """
        Starts the ReAct loop with the optional initial text.
        """
        self.log(f"System Prompt: {self.system_prompt}\n")
        scratchpad = ''
        for _ in range(self.max_iterations):
            self.log(f"Scratchpad:\n{scratchpad}")
            input_message = self.system_prompt + '\n' + scratchpad
            response = complete(input_message)
            output, parsed_output = parseOutput(response)
            scratchpad += '\n' + output

            # If the FINAL_ANSWER key is in the output return the result
            if FINAL_ANSWER in parsed_output:
                return parsed_output[FINAL_ANSWER]

            # If the ACTION key is not in the output specify an observation
            # that the model didn't provide an action to give it a hint
            # for future loops to provide an action
            if ACTION not in parsed_output:
                scratchpad += "\nObservation: I didn't specify an action to perform"
                continue

            # Similar to above, if the ACTION_INPUT is not in the output,
            # use an observation to let the LLM know
            if ACTION_INPUT not in parsed_output:
                scratchpad += "\nObservation: I specified an action, but not an input for it"
                continue

            action = parsed_output[ACTION]
            action_input = parsed_output[ACTION_INPUT]

            # Also similar to above, if the action given is invalid,
            # uses an observation that tells the LLM so that, in future
            # loops, it might correct itself
            if action not in self.actions:
                scratchpad += f"\nObservation: I specified an unrecognized {action}"
                continue

            # Invoke the action and have the next message in the
            # conversation to be an observation whose value is the
            # result of the action's tool
            self.log(f"Running: {action} {action_input}")
            observation = self.actions[action](action_input)
            scratchpad += f"\nObservation: {observation}"

        # If this point is reached, it means a FINAL_ANSWER key was
        # never found and max iterations were reached.  Thus, there
        # is not an answer.
        return None
