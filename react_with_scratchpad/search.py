
import os
import json
import requests

from dataclasses import dataclass
from pathlib import Path
from typing import cast, Callable, Dict

API_KEY = os.environ["VALUE_SERP_API_KEY"]

@dataclass
class Search(object):
    log: Callable[[str], None]

    def search(self, query: str) -> str:
      """
      Peforms a search of the given query through ValueSerp using a very simple
      filesystem backed cache to reduce the number of actual network calls.
      However, the cache doesn't use an expiration policy and so it will
      continue to grow over time.  This is fine for experimentation, but should
      not be used in production.
      """

      # create the cache file if it doesn't already exist
      cache_file = os.path.join(Path.home(), '.search_cache')
      if not os.path.exists(cache_file):
          Path(cache_file).write_text('{}')

      # load the cache.  The cache is of the form `cache[query] = query result`
      with open(cache_file, 'r') as f:
          cache = cast(Dict[str, str], json.load(f))

      # return early if the query's result is already in the cache
      if query in cache:
          self.log(f'Cache hit for query "{query}"')
          return cache[query]

      # use the valueserp API to perform the search
      self.log(f'Cache miss for query "{query}"')
      params = {
          "api_key": API_KEY,
          "q": query,
      }
      response = requests.get('https://api.valueserp.com/search', params).json()

      # if the google search result has an answer box at the top of the search
      # page, use the answer in the box
      result = None
      if 'answer_box' in response:
        answer_box = response['answer_box']
        if 'answers' in answer_box:
            answers = answer_box['answers']
            if len(answers) > 0:
                first = answers[0]
                if 'answer' in first:
                    result = first['answer']

      # otherwise, if the search result doesn't have an answer box use the
      # first organic search result if there is one
      if result is None:
          if 'organic_results' in response:
              organic_results = response['organic_results']
              if len(organic_results) > 0:
                  first = organic_results[0]
                  if 'snippet' in first:
                      result = first['snippet']

      # last if neither an answer box nor an organic result exists,
      # return that the search returned 'Not found'.  Having a string
      # returned instead of None in this case makes the cache implementation
      # easier as well as the usage of this class.  Specifically, callers
      # don't need to worry about how to handle results not found.  However,
      # this comes at the cost of less flexibility.
      if result is None:
          result = 'Not found'

      # update the cache
      cache[query] = result
      with open(cache_file, 'w') as f:
          json.dump(cache, f)

      return result
