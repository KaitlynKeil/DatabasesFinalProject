######################################################################
#
# Final Project Combination
#
# Due: Sat 5/11/19 12h00.
#
# Name: Paige and Kaitlyn
#
# Email:  kaitlyn.keil@students.olin.edu, paige.pfenninger@students.olin.edu
#
# This file imports the relation implementations in order to run their
#  functions and compare them.
#
######################################################################

import timeit
import nestedLoops as nl
import hashJoin as hj

BOOKS_NL = nl.Relation(["title","year","numberPages","isbn"],
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
            ( "The Poisonwood Bible", 1998, 560, "0060175400"),
            ( "The Way of Kings", 2010, 1007, "9780765326355")
            ])


PERSONS_NL = nl.Relation(["firstName", "lastName", "birthYear"],
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
             ( "Barbara", "Kingsolver", 1955),
             ( "Kaitlyn", "Keil", 1996),
             ( "Paige", "Pfenninger", 1997)
           ])


AUTHORED_BY_NL = nl.Relation(["isbn","lastName"],
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
               ( "0375724886" , "Lethem" ),
               ( "0387977102" , "Mac Lane" ),
               ( "0387977102" , "Moerdijk" ),
               ( "0387984032" , "Mac Lane" ),
               ( "0060175400" , "Kingsolver")
             ])

BOOKS_HJ = hj.Relation(["title","year","numberPages","isbn"],
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
            ( "The Poisonwood Bible", 1998, 560, "0060175400"),
            ( "The Way of Kings", 2010, 1007, "9780765326355")
            ])


PERSONS_HJ = hj.Relation(["firstName", "lastName", "birthYear"],
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
             ( "Barbara", "Kingsolver", 1955),
             ( "Kaitlyn", "Keil", 1996),
             ( "Paige", "Pfenninger", 1997)
           ])


AUTHORED_BY_HJ = hj.Relation(["isbn","lastName"],
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
               ( "0375724886" , "Lethem" ),
               ( "0387977102" , "Mac Lane" ),
               ( "0387977102" , "Moerdijk" ),
               ( "0387984032" , "Mac Lane" ),
               ( "0060175400" , "Kingsolver")
             ])

def test_format(testName,nl_res, hj_res, isSuccess = False):
  print("""{} {}""".format(testName, "Passed" if isSuccess else "Failed"))
  print("\tNested Loop\t\t\t|\tHash Join")
  print("-------------------------------------------------")
  print("\t{}\t|\t{}\n".format(nl_res, hj_res))

def test_equality(rel1, rel2):
  tup1_set = set(rel1.tuples())
  tup2_set = set(rel2.tuples())
  for tup in rel1.tuples():
    if tup in tup2_set:
      tup1_set.remove(tup)
      tup2_set.remove(tup)
  if len(tup1_set) == 0 and len(tup2_set) == 0:
    return True
  return False

if __name__ == '__main__':
  query_nl = {
    "select": ["a.lastName", "b.title"],
    "from": [ (BOOKS_NL,"b")],
    "join": [ ('full',AUTHORED_BY_NL, 'a')],
    "on": [ ("n=n", "b.isbn", "a.isbn")],
    "where": [ ]
  }
  query_hj = {
    "select": ["a.lastName", "b.title"],
    "from": [ (BOOKS_HJ,"b")],
    "join": [ ('full',AUTHORED_BY_HJ, 'a')],
    "on": [ ("n=n", "b.isbn", "a.isbn")],
    "where": [ ]
  }
  nl_time = timeit.timeit("nl.evaluate_query(query_nl)", globals=globals(), number=10000)
  hj_time = timeit.timeit('hj.evaluate_query(query_hj)', globals=globals(), number=10000)
  nl_res = nl.evaluate_query(query_nl)
  hj_res = hj.evaluate_query(query_hj)
  test_format("Full Join", nl_time, hj_time, test_equality(nl_res, hj_res))

  query_nl = {
    "select": ["p.lastName", "a.isbn"],
    "from": [ (PERSONS_NL,"p")],
    "join": [ ('left',AUTHORED_BY_NL, 'a')],
    "on": [ ("n=n", "p.lastName", "a.lastName")],
    "where": [ ]
  }
  query_hj = {
    "select": ["p.lastName", "a.isbn"],
    "from": [ (PERSONS_HJ,"p")],
    "join": [ ('left',AUTHORED_BY_HJ, 'a')],
    "on": [ ("n=n", "p.lastName", "a.lastName")],
    "where": [ ]
  }
  nl_time = timeit.timeit("nl.evaluate_query(query_nl)", globals=globals(), number=10000)
  hj_time = timeit.timeit('hj.evaluate_query(query_hj)', globals=globals(), number=10000)
  nl_res = nl.evaluate_query(query_nl)
  hj_res = hj.evaluate_query(query_hj)
  test_format("Left Join", nl_time, hj_time, test_equality(nl_res, hj_res))

  query_nl = {
    "select": ["p.lastName", "a.isbn"],
    "from": [ (PERSONS_NL,"p")],
    "join": [ ('right',AUTHORED_BY_NL, 'a')],
    "on": [ ("n=n", "p.lastName", "a.lastName")],
    "where": [ ]
  }
  query_hj = {
    "select": ["p.lastName", "a.isbn"],
    "from": [ (PERSONS_HJ,"p")],
    "join": [ ('right',AUTHORED_BY_HJ, 'a')],
    "on": [ ("n=n", "p.lastName", "a.lastName")],
    "where": [ ]
  }
  nl_time = timeit.timeit("nl.evaluate_query(query_nl)", globals=globals(), number=10000)
  hj_time = timeit.timeit('hj.evaluate_query(query_hj)', globals=globals(), number=10000)
  nl_res = nl.evaluate_query(query_nl)
  hj_res = hj.evaluate_query(query_hj)
  test_format("Right Join", nl_time, hj_time, test_equality(nl_res, hj_res))

  query_nl = {
    "select": ["b.title", "a.lastName"],
    "from": [ (BOOKS_NL,"b")],
    "join": [ ('inner',AUTHORED_BY_NL, 'a')],
    "on": [ ("n=n", "b.isbn", "a.isbn")],
    "where": [ ]
  }
  query_hj = {
    "select": ["b.title", "a.lastName"],
    "from": [ (BOOKS_HJ,"b")],
    "join": [ ('inner',AUTHORED_BY_HJ, 'a')],
    "on": [ ("n=n", "b.isbn", "a.isbn")],
    "where": [ ]
  }
  nl_time = timeit.timeit("nl.evaluate_query(query_nl)", globals=globals(), number=10000)
  hj_time = timeit.timeit('hj.evaluate_query(query_hj)', globals=globals(), number=10000)
  nl_res = nl.evaluate_query(query_nl)
  hj_res = hj.evaluate_query(query_hj)
  test_format("Inner Join", nl_time, hj_time, test_equality(nl_res, hj_res))
