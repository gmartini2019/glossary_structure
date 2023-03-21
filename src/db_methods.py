import sys
from py2neo import Graph, Node, Relationship, NodeMatch, NodeMatcher
from collections import defaultdict
import difflib
import itertools

def init_import(graph, to_import):
    root_node = Node("business_modeler_terms", name="", description="")
    graph.create(root_node)

    for word, definition in to_import.items():
        node = Node("business_modeler_terms", name=word, description=definition)
        graph.create(node)
        relationship = Relationship(root_node, "HAS", node)
        graph.create(relationship)


def get_words_from_graph(graph):
    matcher = NodeMatcher(graph)
    nodes = matcher.match("business_modeler_terms").where("_.name <> ''")
    return [node["name"] for node in nodes]


def search_node_in_graph(graph, word):
    query = "MATCH (n:business_modeler_terms) WHERE toLower(n.name) = toLower($word) RETURN n.description AS description"
    result = graph.run(query, word=word).data()
    description = result[0]['description'] if result else None
    return description


def update_description(graph, word, new_description):
    query = "MATCH (n:business_modeler_terms {name: $word}) SET n.description = $new_description"
    graph.run(query, word=word, new_description=new_description)


def insert_node(graph, word, description):
    node = Node("business_modeler_terms", name=word, description=description)
    graph.create(node)

    root_node = graph.nodes.match("business_modeler_terms", name="", description="").first()
    relationship = Relationship(root_node, "HAS", node)

    graph.create(relationship)

def insert_dict(graph, to_insert):
    for word, desc in to_insert.items():
        insert_node(graph, word, desc)

def get_close_matches_icase(word, possibilities, *args, **kwargs):
    """ Case-insensitive version of difflib.get_close_matches """
    lword = word.lower()
    lpos = {}
    for p in possibilities:
        if p.lower() not in lpos:
            lpos[p.lower()] = [p]
        else:
            lpos[p.lower()].append(p)
    lmatches = difflib.get_close_matches(lword, lpos.keys(), *args, **kwargs)
    ret = [lpos[m] for m in lmatches]
    ret = itertools.chain.from_iterable(ret)
    return set(ret)

def fuzzy_search(graph, word, cutoff, n):
    exact = search_node_in_graph(graph, word)
    if exact == None:
        results = get_close_matches_icase(word, get_words_from_graph(graph), n=n, cutoff=cutoff)
        res = {result: (search_node_in_graph(graph, result), difflib.SequenceMatcher(None, word.lower(), result.lower()).ratio()) for result in results}
        return dict(sorted(res.items(), key=lambda item: item[1][1], reverse=True))
    return {word: exact}


def fuzzy_search_native(graph, word, n):
    query = """
        CALL db.index.fulltext.queryNodes("businessGlossaryIndex", $word, {limit:$n}) YIELD node, score 
        RETURN node.name, node.description, score
    """
    parameters = {"word": word + "~", "n": n}
    return graph.run(query, parameters=parameters).data()

