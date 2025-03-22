# coding=utf-8
from atlassian import Confluence

"""This example shows how to use the cql
   More detail documentation located here https://developer.atlassian.com/server/confluence/advanced-searching-using-cql
"""

confluence = Confluence(url="http://localhost:8090", username="admin", password="admin")

WORD = "componentname"


def search_word(word):
    """
    Get all found pages with order by created date
    :param word:
    :return: json answer
    """
    cql = f"siteSearch ~ {word} order by created"
    answers = confluence.cql(cql)
    for answer in answers.get("results"):
        print(answer)


def search_word_in_space(space, word):
    """
    Get all found pages with order by created date
    :param space
    :param word:
    :return: json answer
    """
    cql = f"space.key={space} and (text ~ {word})"
    answers = confluence.cql(cql, expand="space,body.view")
    for answer in answers.get("results"):
        print(answer)


if __name__ == "__main__":
    search_word(word=WORD)
    search_word_in_space(space="TST", word=WORD)
