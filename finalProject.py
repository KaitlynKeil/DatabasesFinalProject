######################################################################
#
# HOMEWORK 3
#
# Due: Sun 3/17/19 23h59.
#
# Name: Paige and Kaitlyn
#
# Email:  kaitlyn.keil@students.olin.edu, paige.pfenninger@students.olin.edu
#
# Remarks, if any:
#
#
######################################################################


######################################################################
#
# Python 3 code
#
# Please fill in this file with your solutions and submit it
#
# The functions below are stubs that you should replace with your
# own implementation.
#
######################################################################
import sys
from copy import copy


class Relation:

  def __init__ (self, columns, primary_key, tuples=[]):

    self._columns = columns
    self._primary_key = primary_key
    self._tuples = set(tuples)
    self._primary_key_indices = [columns.index(v) for v in primary_key]

  def __repr__ (self):

    result = "------------------------------------------------------------\n"
    result += (", ".join(self._columns)) + "\n"
    result += "------------------------------------------------------------\n"
    result += "".join([ str(t)+"\n" for t in self._tuples ])
    result += "------------------------------------------------------------"
    return result

  def columns (self):

    return self._columns

  def primary_key (self):

    return self._primary_key

  def primary_key_indices (self):

    return self._primary_key_indices

  def tuples (self):

    return self._tuples

  def primary_key_values (self):

     primary_key_values = [[tup[v] for v in self._primary_key_indices] for tup in self._tuples]
     return primary_key_values


  ########################################
  # LOW-LEVEL CRUD OPERATIONS
  ########################################

  def create_tuple (self,tup):

    if len(tup)  != len(self._columns):
      raise ValueError("Tuple is the incorrect size")

    pk = [tup[v] for v in self._primary_key_indices]

    for key in self.primary_key_values():
      if key == pk:
        raise ValueError("Primary Key Group already exists")

    self._tuples.add(tup)


  def read_tuple (self,pkey):
    pkey_list = list(pkey)

    for tup in self._tuples:
      if pkey_list == [tup[v] for v in self._primary_key_indices]:
        return tup

    raise ValueError("Cannot find tuple with key {}".format(pkey))


  def delete_tuple (self,pkey):

    pkey_list = list(pkey)

    for tup in self._tuples:
      if pkey_list == [tup[v] for v in self._primary_key_indices]:
        self._tuples.remove(tup)
        return

    raise ValueError("Cannot find tuple with key {}".format(pkey))

    pass


  ########################################
  # RELATIONAL ALGEBRA OPERATIONS
  ########################################

  def project (self,names):

    names_indices = [self._columns.index(v) for v in names]

    projected_values = [tuple([tup[n] for n in names_indices]) for tup in self._tuples]

    primary_key = []

    for n in names:
      if n in self._primary_key:
        primary_key.append(n)

    new_rel = Relation(names, primary_key, projected_values)
    return new_rel


  def select (self,pred):
    new_relation_list = []
    for tup in self._tuples:
      d = dict(zip(self._columns, tup))
      if pred(d):
        new_relation_list.append(tup)

    return Relation(self._columns, self._primary_key, new_relation_list)



  def union (self,rel):
    if self._columns != rel._columns:
      raise ValueError("Columns do not match")
    if self._primary_key != rel._primary_key:
      raise ValueError("Primary keys do not match")

    new_rel = Relation(self._columns, self._primary_key, self._tuples)

    for tup in rel.tuples():
      try:
        new_rel.create_tuple(tup)
      except:
        pass

    return new_rel

  def rename (self,r_list):
    new_columns = self.columns()
    new_primary_key = self.primary_key()

    for (old, new) in r_list:
      old_index = new_columns.index(old)
      new_columns[old_index] = new
      try:
        old_index_pk = new_primary_key.index(old)
        new_primary_key[old_index_pk] = new
      except:
        pass


    new_rel = Relation(new_columns, new_primary_key, self.tuples())
    return new_rel


  def product (self,rel):
    if len(list(set(self.columns()) & set(rel.columns()))) > 0:
      raise Exception("Column attributes are not disjoint")

    new_columns = self.columns() + rel.columns()
    new_pk = self.primary_key() + rel.primary_key()

    new_rel = Relation(new_columns, new_pk)

    for tup1 in self.tuples():
      for tup2 in rel.tuples():
        big_tup = (tup1 + tup2)
        new_rel.create_tuple(big_tup)

    return new_rel

  def aggregate (self,aggr):
    #sum, count, average, max, min

    name_list =[]
    value_list = []

    for name, op, attr in aggr:
      name_list.append(name)
      if op == "sum":
        value_list.append(self.sum_attr(attr))
      elif op == "count":
        value_list.append(self.count_attr(attr))
      elif op == "avg":
        value_list.append(self.avg_attr(attr))
      elif op == "min":
        value_list.append(self.min_attr(attr))
      elif op == "max":
        value_list.append(self.max_attr(attr))
      else:
        raise ValueError("Operation not found")

    return Relation(name_list, [], [tuple(value_list)])


  def sum_attr(self, attr):
    index = self.columns().index(attr)
    total = 0
    for tup in self.tuples():
      total += tup[index]
    return total

  def count_attr(self, attr):
    return len(self.tuples())

  def avg_attr(self, attr):
    total = self.sum_attr(attr)
    count = self.count_attr(attr)
    return total / count

  def min_attr(self, attr):
    index = self.columns().index(attr)
    current_min = sys.maxsize
    for tup in self.tuples():
      if tup[index] < current_min:
        current_min = tup[index]
    return current_min

  def max_attr(self, attr):
    index = self.columns().index(attr)
    current_max = -1*sys.maxsize
    for tup in self.tuples():
      if tup[index] > current_max:
        current_max = tup[index]
    return current_max

  #########
  # JOINS #
  #########

  def cross_join(self, rel):
    return self.product(rel)

  def inner_join(self, rel, col, lam_fun):
    temp_col = "r." + col
    rel = rel.rename([(col, temp_col)])
    p = self.product(rel)
    p = p.select(lam_fun)
    cols = p.columns()
    cols = cols.remove(temp_col)
    return p.project(cols)

  def left_outer(self, rel, left_col, right_col, lam_fun):
    left_cols = self.colums()
    right_cols = rel.columns().remove(right_col)
    temp_cols = left_cols + right_cols
    r = Relation(temp_cols, self.primary_key())

    left_col_index = self.columns().index(left_col)
    right_col_index = rel.columns().index(right_col)

    for tup in self.tuples():
      for rtup in rel.tuples():
        if lam_fun(tup[left_col_index], rtup[right_col_index]):
          temp_list = list(rtup)
          temp_list.pop(right_col_index)
          temp_tup = tuple(temp_list)
          r.create_tuple(tup+temp_tup)
          break

      r.create_tuple(tup + tuple([None]*len(right_cols)))

    return r


  def right_outer(self, rel, left_col, right_col, lam_fun):
    return rel.left_outer(self, right_col, left_col, lam_fun)
    

  def full_outer(self, rel, left_col, right_col, lam_fun):
    left_cols = self.colums()
    right_cols = rel.columns().remove(right_col)
    temp_cols = left_cols + right_cols
    r = Relation(temp_cols, self.primary_key() + rel.primary_key())

    left_col_index = self.columns().index(left_col)
    right_col_index = rel.columns().index(right_col)

    temp_rtup = copy(rel.tuples())

    for tup in self.tuples():
      for rtup in temp_rtup:
        if lam_fun(tup[left_col_index], rtup[right_col_index]):
          temp_list = list(rtup)
          temp_list.pop(right_col_index)
          temp_tup = tuple(temp_list)
          r.create_tuple(tup+temp_tup)
          temp_rtup.remove(rtup)
          break

      r.create_tuple(tup + tuple([None]*len(right_cols)))

    for rtup in temp_rtup:
      r.create_tuple(tuple([None]*len(left_cols)) + rtup)

    return r



BOOKS = Relation(["title","year","numberPages","isbn"],
          ["isbn"],
          [
            ( "A Distant Mirror", 1972, 677, "0345349571"),
            ( "The Guns of August", 1962, 511, "034538623X"),
            ( "Norse Mythology", 2017, 299, "0393356182"),
            ( "American Gods", 2003, 591, "0060558121"),
            ( "The Ocean at the End of the Lane", 2013, 181, "0062255655"),
            ( "Good Omens", 1990, 432, "0060853980"),
            ( "The American Civil War", 2009, 396, "0307274939"),
            ( "The First World War", 1999, 500, "0712666451"),
            ( "The Kidnapping of Edgardo Mortara", 1997, 350, "0679768173"),
            ( "The Fortress of Solitude", 2003, 509, "0375724886"),
            ( "The Wall of the Sky, The Wall of the Eye", 1996, 232, "0571205992"),
            ( "Stories of Your Life and Others", 2002, 281, "1101972120"),
            ( "The War That Ended Peace", 2014, 739, "0812980660"),
            ( "Sheaves in Geometry and Logic", 1994, 630, "0387977102"),
            ( "Categories for the Working Mathematician", 1978, 317, "0387984032"),
            ( "The Poisonwood Bible", 1998, 560, "0060175400")
            ])


PERSONS = Relation(["firstName", "lastName", "birthYear"],
           ["lastName"],
           [
             ( "Barbara", "Tuchman", 1912 ),
             ( "Neil", "Gaiman", 1960 ),
             ( "Terry", "Pratchett", 1948),
             ( "John", "Keegan", 1934),
             ( "Jonathan", "Lethem", 1964),
             ( "Margaret", "MacMillan", 1943),
             ( "David", "Kertzer", 1948),
             ( "Ted", "Chiang", 1967),
             ( "Saunders", "Mac Lane", 1909),
             ( "Ieke", "Moerdijk", 1958),
             ( "Barbara", "Kingsolver", 1955)
           ])


AUTHORED_BY = Relation(["isbn","lastName"],
             ["isbn","lastName"],
             [
               ( "0345349571", "Tuchman" ),
               ( "034538623X", "Tuchman" ),
               ( "0393356182" , "Gaiman" ),
               ( "0060558121" , "Gaiman" ),
               ( "0062255655" , "Gaiman" ),
               ( "0060853980" , "Gaiman" ),
               ( "0060853980" , "Pratchett" ),
               ( "0307274939" , "Keegan" ),
               ( "0712666451" , "Keegan" ),
               ( "1101972120" , "Chiang" ),
               ( "0679768173" , "Kertzer" ),
               ( "0812980660" , "MacMillan" ),
               ( "0571205992" , "Lethem" ),
               ( "0375724886" , "Lethem" ),
               ( "0387977102" , "Mac Lane" ),
               ( "0387977102" , "Moerdijk" ),
               ( "0387984032" , "Mac Lane" ),
               ( "0060175400" , "Kingsolver")
             ])



def evaluate_query (query):
  relationList = query['from']
  nicknameDict = {}
  for relation,nickname in relationList:
    nicknameDict[nickname] = relation
    for column in relation.columns():
      if not nickname+'.' in column:
        relation.rename([(column, nickname+'.'+column)])

  totalProduct = relationList[0][0]
  if len(relationList) > 1:
    for relation, nickname in relationList[1:]:
      totalProduct=totalProduct.product(relation)


  whereList = query['where']
  for item in whereList:
    if item[0] == 'n=n':
      attr1 = item[1]
      attr2 = item[2]
      totalProduct = totalProduct.select(lambda t: t[attr1]==t[attr2])
    elif item[0] == 'n=v':
      attr1 = item[1]
      totalProduct = totalProduct.select(lambda t: t[attr1]==item[2])
    elif item[0] == 'n>v':
      attr1 = item[1]
      totalProduct = totalProduct.select(lambda t: t[attr1]>item[2])
  return totalProduct.project(query['select'])


def evaluate_query_aggr (query):
  subquery = {}
  subquery['select'] = [tup[2] for tup in query['select-aggr']]
  subquery['from'] = query['from']
  subquery['where'] = query['where']
  res = evaluate_query(subquery)

  return res.aggregate(query['select-aggr'])


def evaluate_query_aggr_group (query):
  # we are a smol group and do not have aggr group
  pass

import pyparsing as pp


def parseQuery (input):

    # parse a string into an abstract query

    # <sql> ::= select <columns> from <tables> (where <conditions>)?

    idChars = pp.alphas+"_*"

    pIDENTIFIER = pp.Word(idChars, idChars+"0123456789.")
    pIDENTIFIER.setParseAction(lambda result: result[0])

    pCOMMAIDENT = pp.Suppress(pp.Word(",")) + pIDENTIFIER

    pIDENTIFIER2 = pp.Group(pIDENTIFIER + pIDENTIFIER)

    pCOMMAIDENT2 = pp.Suppress(pp.Word(",")) + pIDENTIFIER2

    pINTEGER = pp.Word("-0123456789","0123456789")
    pINTEGER.setParseAction(lambda result: int(result[0]))

    pSTRING = pp.QuotedString("'")

    pKEYWORD = lambda w : pp.Suppress(pp.Keyword(w))

    pSELECT = pKEYWORD("select") + pp.Group(pIDENTIFIER + pp.ZeroOrMore( pCOMMAIDENT))

    pFROM = pKEYWORD("from") + pp.Group(pIDENTIFIER2 + pp.ZeroOrMore( pCOMMAIDENT2))

    pCONDITION_NEQN = pIDENTIFIER + pp.Word("=") + pIDENTIFIER
    pCONDITION_NEQN.setParseAction(lambda result: ("n=n",result[0],result[2]))

    pCONDITION_NEQV1 = pIDENTIFIER + pp.Word("=") + pINTEGER
    pCONDITION_NEQV1.setParseAction(lambda result: ("n=v",result[0],result[2]))

    pCONDITION_NEQV2 = pIDENTIFIER + pp.Word("=") + pSTRING
    pCONDITION_NEQV2.setParseAction(lambda result: ("n=v",result[0],result[2]))

    pCONDITION_NGEV = pIDENTIFIER + pp.Word(">") + pINTEGER
    pCONDITION_NGEV.setParseAction(lambda result: ("n>v",result[0],result[2]))

    pCONDITION = pCONDITION_NEQV1 | pCONDITION_NEQV2 | pCONDITION_NEQN | pCONDITION_NGEV

    pANDCONDITION = pKEYWORD("and") + pCONDITION

    pCONDITIONS = pp.Group(pCONDITION + pp.ZeroOrMore( pANDCONDITION))

    pWHERE = pp.Optional(pKEYWORD("where") + pCONDITIONS )

    pSQL = pSELECT + pFROM + pWHERE + pp.StringEnd()
    pSQL.setParseAction(lambda result: { "select": result[0].asList(),
                                         "from": result[1].asList(),
                                         "where": result[2].asList() if len(result)>2 else []})


    result = pSQL.parseString(input)[0]
    return result    # the first element of the result is the expression


sample_db = {
    "Books": BOOKS,
    "Persons": PERSONS,
    "AuthoredBy": AUTHORED_BY
}



def convert_abstract_query (db,aq):
  aq['from'] = [(db[tup[0]], tup[1]) for tup in aq['from']]
  return aq

def shell (db):
  print("Available tables:")
  for key in db:
    print('\t'+key)
  while True:
    try:
      newRelName = None
      x = input("> ")
      if x == 'quit':
        break
      if ':' in x:
        [newRelName, x] = x.split(':')
      y = parseQuery(x)
      y = convert_abstract_query(db, y)
      evaled = evaluate_query(y)
      print(evaled)
      if newRelName:
        db[newRelName] = evaled
        print("Relation {} created".format(newRelName))
    except Exception as e:
      print("Error: " + e)

if __name__ == '__main__':
  shell(sample_db)
  # print(convert_abstract_query(sample_db,{ "select": ["a.lastName", "b.title"], "from": [ ("Books","b"), ("AuthoredBy","a") ], "where": [ ("n=n", "b.isbn", "a.isbn"), ("n=v", "a.lastName", "Gaiman")] }))
