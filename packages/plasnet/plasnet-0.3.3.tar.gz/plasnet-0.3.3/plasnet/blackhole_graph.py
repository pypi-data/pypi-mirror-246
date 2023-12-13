import logging
from typing import Any, Optional

import networkx as nx

from plasnet.base_graph import BaseGraph


class BlackholeGraph(BaseGraph):
    """
    This is a class that recognises and labels blackhole plasmids.
    """

    def __init__(
        self,
        graph: Optional[nx.Graph] = None,
        blackhole_connectivity_threshold: int = 0,
        edge_density: float = 0.0,
        label: str = "",
    ):
        super().__init__(graph, label)
        self._blackhole_connectivity_threshold = blackhole_connectivity_threshold
        self._edge_density = edge_density

    def _get_node_shape(self, node: str) -> str:
        if node in self._get_blackhole_plasmids():
            return "star"
        return "circle"

    def _add_special_node_attributes(self, node: str, attrs: dict[str, Any]) -> None:
        if node in self._get_blackhole_plasmids():
            attrs["is_blackhole"] = True
        else:
            attrs["is_blackhole"] = False

    def _get_blackhole_plasmids(self) -> list[str]:
        blackhole_plasmids_in_graph = []
        for node in self.nodes:
            if self.degree(node) >= self._blackhole_connectivity_threshold:
                neighbors = list(self.neighbors(node))
                subgraph = nx.induced_subgraph(self, neighbors)
                nb_of_edges_between_neighbours = subgraph.number_of_edges()
                max_nb_of_edges_between_neighbours = (len(neighbors) * (len(neighbors) - 1)) // 2
                edge_rate = nb_of_edges_between_neighbours / max_nb_of_edges_between_neighbours
                if edge_rate <= self._edge_density:
                    blackhole_plasmids_in_graph.append(node)
                    logging.debug(f"{node} is a blackhole plasmid")
                else:
                    logging.debug(
                        f"{node} is highly connected but does not connect "
                        f"unrelated plasmids, not a blackhole plasmid"
                    )
        return blackhole_plasmids_in_graph

    def get_nb_of_blackhole_plasmids(self) -> int:
        return len(self._get_blackhole_plasmids())

    def remove_blackhole_plasmids(self) -> None:
        self.remove_nodes_from(self._get_blackhole_plasmids())

    def _get_filters_HTML(self) -> str:
        nb_of_black_holes = len(self._get_blackhole_plasmids())
        return (
            f'<label for="hide_blackholes">'
            f"Hide blackhole plasmids ({nb_of_black_holes} present)"
            f"</label>"
            f'<input type="checkbox" id="hide_blackholes" name="hide_blackholes"><br/>'
        )

    def _get_custom_buttons_HTML(self) -> str:
        return '<div><input type="submit" value="Redraw" onclick="redraw()"></div>'

    @property
    def description(self) -> str:
        description = super().description
        blackholes_detected = self.get_nb_of_blackhole_plasmids() > 0
        if blackholes_detected:
            description += " - WARNING: BLACKHOLE SPOTTED!"
        return description
