from bs4 import BeautifulSoup
import pprint
import argparse

PATH = 'file_path'
IS_JOIN_ROW = 'is_join_row'


def parse_tables(path: str, is_join_cells: bool = False) -> iter:
    """
    Parse provided html file for <table> tag and makes a list of lists
    or strings

    :param      path:           path to html file
    :type       path:           str
    :param      is_join_cells:  True - row cells will be joined to string,
                                False - each cell will be a list item
    :type       is_join_cells:  boolean

    :returns:   table as list
    :rtype:     iter
    """
    def join_cells_(cells: list):
        return ''.join(cells)

    join_cells = join_cells_ if is_join_cells else lambda x: x

    with open(path, "r") as file:
        soup = BeautifulSoup(file, features='lxml')
        tables = soup.find_all('table')

        for t in tables:
            rows = t.find_all('tr')
            rlist = []
            for r in rows:
                clist = []
                cells = r.find_all('td')
                for c in cells:
                    # empty cells generate \xA0 symbol - replace it with space
                    text = c.p.get_text().replace('В\xa0', ' ')
                    clist += text
                rlist.append(join_cells(clist))
            yield rlist


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="""Parse html file for tables and pack them """
                    """as list of lists or list of strings """
                    """in case of -j flag""")

    parser.add_argument(
        'path',
        metavar='path',
        type=str,
        help='path to html file')

    parser.add_argument(
        '-j',
        '--joincells',
        help='join cells of a row to produce string',
        action='store_true',
        default=False,
        dest='is_join_cells')

    args = parser.parse_args()

    pp = pprint.PrettyPrinter(indent=4)
    for t in parse_tables(args.path, args.is_join_cells):
        pp.pprint(t)
