from sys import argv
from pyswip import Prolog
from query import Query
from result import Result
from typing import Generator
import re


def debug(msg):
    return
    print("(dg)", msg)


request_formats = [
    {
        'regex': r'^Кто дружит с (.+)\?$',
        'help': 'Запрос: «Кто дружит с [Игрок]?»',
        'query': "player('{0}'),is_friends('{0}',X)",
        'vars': ('X'),
        'answer': lambda players: f'C ним/ней дружит {", а еще ".join(players)}.'
    },

    {
        'regex': r'^(.+) дружит с (.+)\?$',
        'help': 'Запрос: «[Игрок А] дружит с [Игрок Б]?»',
        'query': "player('{0}'), player('{1}'),is_friends('{0}','{1}')",
        'vars': None,
        'answer': lambda res: "Да, это так." if res else "Нет, это не так."
    },

    {
        'regex': r'^(.+) может играть с (.+)\?$',
        'help': 'Запрос: «[Игрок А] может играть с [Игрок Б]?»',
        'query': "player('{0}'),player('{1}'),can_play_in_team('{0}','{1}')",
        'vars': None,
        'answer': lambda res: "Да, это так." if res else "Нет, это не так."
    },

    {
        'regex': r'^Какой уровень у (.+)\?$',
        'help': 'Запрос: «Какой уровень у [Игрок]?»',
        'query': "player('{0}'),has_level('{0}',X)",
        'vars': ('X'),
        'answer': lambda level:
            'Непонятно какой уровень.' if not level
            else f'Он(а) достиг(ла) {level} уровня.'
    },
    {
        'regex': r'^У кого такой же уровень, как и у (.+)\?$',
        'help': 'Запрос: «У кого такой же уровень, как и у [Игрок]?»',
        'query': r"player('{0}'),same_level('{0}',X), X \= '{0}'",
        'vars': ('X'),
        'answer': lambda players:
            'Нет игроков с таким же уровнем.' if len(players) == 0
            else f'У следующих игроков такой же уровень как и у него/нее: { ", ".join(players) }.'
    },
    {
        'regex': r'^У (.+) и (.+) одинаковые уровни\?$',
        'help': 'Запрос: «У [Игрок А] и [Игрок Б] одинаковые уровни?»',
        'query': "player('{0}'),player('{1}'),same_level('{0}','{1}')",
        'vars': None,
        'answer': lambda res: "Да, это так." if res else "Нет, это не так."
    },
]


def print_help_msg():
    print('Используйте команду `help` или `?` для получения этой справки.')
    print('== Справка по использованию запросов ==')
    for f in request_formats:
        print(f['help'])


def request_for_input() -> Generator[str, None, None]:
    while True:
        try:
            i = input("kb-rq> ")
            debug(f"req_inp {i}")

            if i == "exit":
                return
            if i == "help" or i == "?":
                print_help_msg()
                continue
            yield i
        except (EOFError, KeyboardInterrupt) as e:
            print("request for exit")
            return


def parse_request_params(req: str) -> Query | None:
    req = re.sub(r'\s+', ' ', req.strip())

    for f in request_formats:
        match = re.search(f['regex'], req, re.IGNORECASE)
        if match:
            debug(f"parsed params {match.groups()} and query ({f['query']})")

            q = Query(format=f, params=match.groups())

            debug(f"{q.to_string()}")
            return q

    return None


def execute_query(query: Query, kb: Prolog) -> Result | None:
    solutions = kb.query(query.to_string())
    res = []
    for s in solutions:
        debug(f"execute_query solution: {s}")
        if query.format['vars'] != None:
            for v in query.format['vars']:
                res.append(s[v])
        else:
            res.append(s)

    debug(f"execute_query {res}")

    return Result(res, query.format)


def present_result(res: Result):
    print(res.to_string())


def main(argv: list[str]):
    kb = Prolog()
    try:
        kb.consult(argv[1] if len(argv) > 1 else "../lab-1/knowledge-base.pl")
    except:
        print("Incorrect path to KB! Try againg!")
        return

    print_help_msg()

    for i in request_for_input():
        q = parse_request_params(i)
        if q == None:
            print('Bad query! Pls, check formats!')
            continue
        res = execute_query(q, kb)
        present_result(res)


if __name__ == "__main__":
    main(argv)
