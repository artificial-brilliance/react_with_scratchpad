import unittest

from react_with_scratchpad.output_parser import parseOutputValues, parseOutput

class OutputParserTest(unittest.TestCase):
    def testParsedOutputValues(self):
        self.assertEqual(parseOutputValues("""
Line that should not be in parsed output
Thought: some
thought
Action: some action
and more

Observation: some observation
Empty:
"""), {
    "Thought": "some\nthought",
    "Action": "some action\nand more",
    "Observation": "some observation",
    "Empty": "",
})

    def testParsedOutputValuesUsesLastValue(self):
        self.assertEqual(parseOutputValues("""
Some Key: some value 1
Some Key: some value 2
"""), {
    "Some Key": "some value 2",
})

    def testParseOutput(self):
        text = f"""
Some prefix text
Thought: some thought
Action: some action
Action Input: some input
Observation: some hallucinated observation
more text
Thought: another thought
Action: another action
Observation: another observation
"""
        newOutput, values = parseOutput(text)
        self.assertEqual(newOutput, f"""Some prefix text
Thought: some thought
Action: some action
Action Input: some input""")
        self.assertDictEqual(values, {
            "Thought": "some thought",
            "Action": "some action",
            "Action Input": "some input"
        })
