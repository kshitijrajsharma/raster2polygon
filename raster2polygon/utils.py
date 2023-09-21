
import collections
import functools
import warnings

import pyproj
import shapely.ops
from rtree.index import Index, Property

class UndirectedGraph:
    """Simple undirected graph.
    From: https://github.com/mapbox/robosat

    Note: stores edges; can not store vertices without edges.
    """

    def __init__(self):
        """Creates an empty `UndirectedGraph` instance."""

        # Todo: We might need a compressed sparse row graph (i.e. adjacency array)
        # to make this scale. Let's circle back when we run into this limitation.
        self.edges = collections.defaultdict(set)

    def add_edge(self, s, t):
        """Adds an edge to the graph.

        Args:
          s: the source vertex.
          t: the target vertex.

        Note: because this is an undirected graph for every edge `s, t` an edge `t, s` is added.
        """
        self.edges[s].add(t)
        self.edges[t].add(s)

    def targets(self, v):
        """Returns all outgoing targets for a vertex.

        Args:
          v: the vertex to return targets for.

        Returns:
          A list of all outgoing targets for the vertex.
        """
        return self.edges[v]

    def vertices(self):
        """Returns all vertices in the graph.

        Returns:
          A set of all vertices in the graph.
        """
        return self.edges.keys()

    def empty(self):
        """Returns true if the graph is empty, false otherwise.

        Returns:
          True if the graph has no edges or vertices, false otherwise.
        """
        return len(self.edges) == 0

    def dfs(self, v):
        """Applies a depth-first search to the graph.

        Args:
          v: the vertex to start the depth-first search at.

        Yields:
          The visited graph vertices in depth-first search order.

        Note: does not include the start vertex `v` (except if an edge targets it).
        """
        stack = []
        stack.append(v)

        seen = set()

        while stack:
            s = stack.pop()

            if s not in seen:
                seen.add(s)

                for t in self.targets(s):
                    stack.append(t)

                yield s

    def components(self):
        """Computes connected components for the graph.

        Yields:
          The connected component sub-graphs consisting of vertices; in no particular order.
        """
        seen = set()

        for v in self.vertices():
            if v not in seen:
                component = set(self.dfs(v))
                component.add(v)

                seen.update(component)

                yield component


def project(shape, source, target):
    """Projects a geometry from one coordinate system into another.
    This function is an adaptation to bypass a bug in pyproj package
    Args:
      shape: the geometry to project.
      source: the source EPSG spatial reference system identifier.
      target: the target EPSG spatial reference system identifier.

    Returns:
      The projected geometry in the target coordinate system.
    """
    with warnings.catch_warnings():  # To exclude the warnings of Proj deprecation
        warnings.simplefilter("ignore")
        proj_in = pyproj.Proj(init=source)
        proj_out = pyproj.Proj(init=target)
    project_fun = pyproj.Transformer.from_proj(proj_in, proj_out).transform

    return shapely.ops.transform(project_fun, shape)


def union(shapes):
    """Returns the union of all shapes.
    From: https://github.com/mapbox/robosat

    Args:
      shapes: the geometries to merge into one.

    Returns:
      The union of all shapes as one shape.
    """
    assert shapes

    def fn(lhs, rhs):
        return lhs.union(rhs)

    return functools.reduce(fn, shapes)


def make_index(shapes):
    """Creates an index for fast and efficient spatial queries.
    From: https://github.com/mapbox/robosat

    Args:
      shapes: shapely shapes to bulk-insert bounding boxes for into the spatial index.

    Returns:
      The spatial index created from the shape's bounding boxes.
    """
    # Todo: benchmark these for our use-cases
    prop = Property()
    prop.dimension = 2
    prop.leaf_capacity = 1000
    prop.fill_factor = 0.9

    def bounded():
        for i, shape in enumerate(shapes):
            yield (i, shape.bounds, None)

    return Index(bounded(), properties=prop)