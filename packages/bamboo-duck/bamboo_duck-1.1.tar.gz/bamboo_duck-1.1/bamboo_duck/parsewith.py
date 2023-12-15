from parsimonious.grammar import Grammar, NodeVisitor
from dataclasses import dataclass
from typing import Tuple

QGrammar = Grammar(r'''
  # OG code
  q = _ withclause? query?
  withclause = with def_list
  # My code
  # q = with? def_list? query?
  def_list = def (comma def)*
  def = name _ as? lparen query rparen
  query = select? _ restofquery
  restofquery = (string? parens?)+ _
  parens = lparen restofquery rparen
  string = ~r"[^()]+"

  select = ("select" / "SELECT") _
  with = ("WITH" / "with") _
  as = ("AS" / "as") _
  comma = "," _
  lparen = "(" _
  rparen = ")" _


  _ = meaninglessness*
  meaninglessness = ~r"\s+" / comment
  comment = ~r"--[^\r\n]*"
  name = ~"[a-zA-Z][a-zA-Z_0-9]*" 

                   ''')

@dataclass
class Query(object):
  """
  WITH a AS (...), b AS (...) 
  body
  """
  # a list of (name, query definition) pairs
  defs: list[Tuple[str,str]]
  # the body of the query, may be empty string
  query: str = ''

  def add(self, name: str, query_definition: str):
    self.defs.append((name, query_definition))

class QVisitor(NodeVisitor):

  def visit_q(self, node, children):
    _, withclause, query = children
    if not withclause:
      withclause = [] 
    if all(isinstance(sublist,list) for sublist in withclause):
      new_with_clause = []
      for sublist in withclause:
        for item in sublist:
          new_with_clause.append(item)
      withclause = new_with_clause
    q = Query(withclause, query)
    return Query(withclause, query)

  def visit_withclause(self, node, children):
    _with, deflist = children
    return deflist

  def visit_def_list(self, node, children):
    first, rest = children
    if isinstance(rest, list):
      rest = [o[1] for o in rest]
      return [first] + rest
    return first

  def visit_def(self, node, children):
    name, _ws, _as, _l, query, _r = children
    return (name, query)

  def visit_query(self, node, children):
    return node.text

  def generic_visit(self, node, visited_children):
    return visited_children or node.text


def parse_with_query(s):
  """
  @param s with query string that optionally has a query body
  @returns a Query object (see above)
  """
  tree = QGrammar.parse(s)
  v = QVisitor()
  query = v.visit(tree)
  return query



if __name__ == "__main__":

  
  tests = [
      # "with unpivot_result as ( select * from 'evi_raw'), gid_map as ( select *)",
      # "select *",
      # "with source as ( select a.year, ()) select * from source",
      # "with source as ( select (), (())) select * from source",
      # "with source as ( select (), (())), source2 as ( select ()('') where () () ) select * from source",
      # "with source as ( select a.year as year, {{ var('sum_early_weight')}}*a.payout + ())select * from source",
      # "with source as ( select a.year as year, {{ var('sum_early_weight')}}*a.payout + {{ var('vegetation_weight')}}*GREATEST(b.payout,c.payout) as combined_payout, a.payout as sum_early, b.payout as sum_late, c.payout as vegetation from  payout_sum_early a join payout_sum_late b on a.year = b.year left join payout_vegetation_evi c on a.year = c.year)select * from source",
        # "WITH a ( select * )",
      # "WITH a AS ( select * ), b AS (select *)",
      # "WITH a AS ( select * ), b AS (select *) SELECT *",
      # "WITH a ( select a() )",
      # "WITH a ( select ( x ) ), b AS ( select ( ( e ) . ) ) SELECT * FROM blah",
      # "WITH unpivot_result as ( select * from chirps_raw), gid_map as ({{ gid_map('unpivot_result', 'admin_raw') }}), filter_year_admin as (select *from gid_map where gid = '{{ var('region') }}' and YEAR >= {{ var('year_start') }} and YEAR <= {{ var('year_end') }}), cap as ({{ dekcap_f('filter_year_admin') }}), output as ({{ ag('cap') }})select * from output",
      ]

  for test in tests:
    print(test)
    try:
      query= parse_with_query(test)
      print(query.defs)
      print("\n\n\n")
      #print(query)
    except Exception as e:
      # Code to handle the exception
      print("An error occurred:", e)
      break
   
  
  
