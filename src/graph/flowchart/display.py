import networkx as nx
from matplotlib import pyplot as plt


class InteractiveGraph:
    def __init__(self, G: nx.DiGraph):
        self.G = G
        self.pos = nx.spring_layout(G)
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.selected_node = None
        self.cid_press = self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.cid_release = self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.cid_motion = self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.draw_graph()

    def draw_graph(self):
        self.ax.clear()
        labels = nx.get_node_attributes(self.G, 'label')
        edge_labels = nx.get_edge_attributes(self.G, 'label')
        nx.draw(self.G, self.pos, with_labels=True, labels=labels, node_size=3000, node_color="lightblue",
                edge_color="gray", font_size=10, ax=self.ax)
        nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels=edge_labels, font_size=9, ax=self.ax)
        plt.title("Graph Visualization from Draw.io")
        plt.draw()

    def on_press(self, event):
        if event.inaxes is None:
            return
        for node, (x, y) in self.pos.items():
            if (event.xdata - x) ** 2 + (event.ydata - y) ** 2 < 0.01:
                self.selected_node = node
                return

    def on_release(self, event):
        self.selected_node = None

    def on_motion(self, event):
        if self.selected_node is None or event.inaxes is None:
            return
        self.pos[self.selected_node] = (event.xdata, event.ydata)
        self.draw_graph()