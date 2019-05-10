######################################################################
#
# Final Project
#
# Due: Sat 5/11/19 12h00.
#
# Name: Paige and Kaitlyn
#
# Email:  kaitlyn.keil@students.olin.edu, paige.pfenninger@students.olin.edu
#
# This implementation uses a Hash Table when possible in order to join
#  two tables.
#  If an equi join is being used, the tables are joined using a hash join.
#  Otherwise, the nested loop method is used.
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

  def inner_join(self, rel, left_col, right_col, lam_fun):
    left_cols = self.columns()
    right_cols = list(rel.columns())
    temp_cols = left_cols + right_cols
    rel_primary = list(rel.primary_key())
    r = Relation(temp_cols, self.primary_key()+rel_primary)

    left_col_index = self.columns().index(left_col)
    right_col_index = rel.columns().index(right_col)

    for tup in self.tuples():
      for rtup in rel.tuples():
        if lam_fun(tup[left_col_index], rtup[right_col_index]):
          r.create_tuple(tup+rtup)

    return r

  def inner_hash(self, rel, left_col, right_col):
    right_cols = list(rel.columns())
    temp_cols = self.columns() + right_cols
    rel_primary = list(rel.primary_key())
    r = Relation(temp_cols, self.primary_key()+rel_primary)

    joinHash = make_hash(rel, right_col)
    i = self.columns().index(left_col)

    for tup in self.tuples():
      joinkey = tup[i]
      if joinkey in joinHash:
        for tup2 in joinHash[joinkey]:
          r.create_tuple(tup+tup2)

    return r

  def left_outer(self, rel, left_col, right_col, lam_fun):
    left_cols = self.columns()
    right_cols = list(rel.columns())
    temp_cols = left_cols + right_cols
    rel_primary = list(rel.primary_key())
    r = Relation(temp_cols, self.primary_key()+rel_primary)

    left_col_index = self.columns().index(left_col)
    right_col_index = rel.columns().index(right_col)

    for tup in self.tuples():
      tup_seen = False
      for rtup in rel.tuples():
        if lam_fun(tup[left_col_index], rtup[right_col_index]):
          tup_seen = True
          temp_list = list(rtup)
          temp_list.pop(right_col_index)
          temp_tup = tuple(temp_list)
          r.create_tuple(tup+temp_tup)
      if not tup_seen:
        r.create_tuple(tup + tuple([None]*len(right_cols)))

    return r

  def left_outer_hash(self, rel, left_col, right_col):
    right_cols = list(rel.columns())
    temp_cols = self.columns() + right_cols
    rel_primary = list(rel.primary_key())
    r = Relation(temp_cols, self.primary_key()+rel_primary)

    joinHash = make_hash(rel, right_col)
    i = self.columns().index(left_col)

    for tup in self.tuples():
      joinkey = tup[i]
      if joinkey in joinHash:
        for tup2 in joinHash[joinkey]:
          r.create_tuple(tup+tup2)
      else:
        r.create_tuple(tup + tuple([None]*len(right_cols)))

    return r


  def right_outer(self, rel, left_col, right_col, lam_fun):
    return rel.left_outer(self, right_col, left_col, lam_fun)

  def right_outer_hash(self, rel, left_col, right_col):
    return rel.left_outer_hash(self, right_col, left_col)


  def full_outer(self, rel, left_col, right_col, lam_fun):
    left_cols = self.columns()
    right_cols = list(rel.columns())
    temp_cols = left_cols + right_cols
    rel_primary = list(rel.primary_key())
    r = Relation(temp_cols, self.primary_key()+rel_primary)

    left_col_index = self.columns().index(left_col)
    right_col_index = rel.columns().index(right_col)

    temp_rtup = copy(rel.tuples())
    seen_rtups = set()

    for tup in self.tuples():
      tup_seen = False
      for rtup in temp_rtup:
        if lam_fun(tup[left_col_index], rtup[right_col_index]):
          tup_seen = True
          temp_list = list(rtup)
          temp_tup = tuple(temp_list)
          r.create_tuple(tup+temp_tup)
          seen_rtups.add(rtup)
      if not tup_seen:
        r.create_tuple(tup + tuple([None]*len(right_cols)))

    for rtup in temp_rtup:
      if rtup not in seen_rtups:
        temp_list = list(rtup)
        temp_tup = tuple(temp_list)
        r.create_tuple(tuple([None]*(len(left_cols))) + temp_tup)

    return r

  def full_outer_hash(self, rel, left_col, right_col):
    left_cols = self.columns()
    right_cols = list(rel.columns())
    temp_cols = left_cols + right_cols
    rel_primary = list(rel.primary_key())
    r = Relation(temp_cols, self.primary_key()+rel_primary)

    i = self.columns().index(left_col)

    joinHash = make_hash(rel, right_col)

    for tup in self.tuples():
      joinkey = tup[i]
      if joinkey in joinHash:
        for tup2 in joinHash[joinkey]:
          r.create_tuple(tup+tup2)
        joinHash.pop(joinkey)
      else:
        r.create_tuple(tup + tuple([None]*len(right_cols)))

    for joinkey, tuplist in joinHash.items():
      for tup in tuplist:
        temp = (None,) * len(left_cols) + tup
      r.create_tuple(temp)

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
            # ( "The American Civil War", 2009, 396, "0307274939"),
            # ( "The First World War", 1999, 500, "0712666451"),
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
               ( "0060853981" , "Pratchett" ),
               ( "0307274939" , "Keegan" ),
               ( "0712666451" , "Keegan" ),
               ( "1101972120" , "Chiang" ),
               ( "0679768173" , "Kertzer" ),
               ( "0812980660" , "MacMillan" ),
               ( "0571205992" , "Lethem" ),
               # ( "0375724886" , "Lethem" ),
               # ( "0387977102" , "Mac Lane" ),
               ( "0387977102" , "Moerdijk" ),
               ( "0387984032" , "Mac Lane" ),
               ( "0060175400" , "Kingsolver")
             ])

def make_hash(rel, joinAttr):
  """ Given a relation and the join attribute,
  creates a hash table of that attribute
  pointing to a list of all the tuples (minus
  the attribute) that match.
  """
  joinHash = {}
  i = rel.columns().index(joinAttr)
  for tup in rel.tuples():
    joinkey = tup[i]
    joinHash[joinkey] = joinHash.get(joinkey, [])
    joinHash[joinkey].append(tup)
  return joinHash

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

  if query['join']:
    isEqui = False
    on_tup = query.get('on',[None])[0]
    if on_tup:
      if on_tup[0] == 'n=n':
        left_col = on_tup[1]
        right_col = on_tup[2]
        isEqui = True
        l = lambda t,y: t==y
      elif on_tup[0] == 'n>n':
        left_col = on_tup[1]
        right_col = on_tup[2]
        l = lambda t,y: t>y
      elif on_tup[0] == 'n<n':
        left_col = on_tup[1]
        right_col = on_tup[2]
        l = lambda t,y: t<y

    join_list = query['join']
    nicknameDict = {}
    for join_type,relation,nickname in join_list:
      nicknameDict[nickname] = relation
      for column in relation.columns():
        if not nickname+'.' in column:
          relation.rename([(column, nickname+'.'+column)])
      if join_type == 'left':
        if isEqui:
          totalProduct = totalProduct.left_outer_hash(relation, left_col, right_col)
        else:
          totalProduct = totalProduct.left_outer(relation, left_col, right_col, l)
      elif join_type == 'right':
        if isEqui:
          totalProduct = totalProduct.right_outer_hash(relation, left_col, right_col)
        else:
          totalProduct = totalProduct.right_outer(relation, left_col, right_col, l)
      elif join_type == 'full':
        if isEqui:
          totalProduct = totalProduct.full_outer_hash(relation, left_col, right_col)
        else:
          totalProduct = totalProduct.full_outer(relation, left_col, right_col, l)
      elif join_type == 'inner':
        if isEqui:
          totalProduct = totalProduct.inner_hash(relation, left_col, right_col)
        else:
          totalProduct = totalProduct.inner_join(relation, left_col, right_col, l)
      elif join_type == 'cross':
        totalProduct = totalProduct.cross_join(relation)

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

  if query['join']:
    subquery['join'] = query['join']
    subquery['on'] = query['on']

  res = evaluate_query(subquery)

  return res.aggregate(query['select-aggr'])

if __name__ == '__main__':
  query = {
  "select": ["a.lastName", "b.title"],
  "from": [ (BOOKS,"b")],
  "join": [ ('inner',AUTHORED_BY, 'a')],
  "on": [ ("n=n", "b.isbn", "a.isbn")],
  "where": [ ]
  }
  print(evaluate_query(query))
