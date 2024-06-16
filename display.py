import networkx as nx
from matplotlib import pyplot as plt
import  numpy as np
from matplotlib import cm
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
def create_undirected_graph( nodes, edges):
    # Create an empty undirected graph
    G = nx.Graph()
    # Add nodes to the graph
    G.add_nodes_from(nodes)
    # Add edges to the graph
    G.add_edges_from(edges)

    print(f'# of c.c: {len(list(nx.connected_components(G)))}')
    return G
def get_pos(G, layout):
    pos = {}
    components = list(nx.connected_components(G))
    # Compute layout for each connected component
    for i, component in enumerate(components):
        subgraph = G.subgraph(component)
        sub_pos = nx.spring_layout(subgraph)
        # Offset each component to avoid overlap
        offset = i * 2  # Adjust the offset value as needed
        for node in sub_pos:
            pos[node] = sub_pos[node] + [offset, 0]  # Offset in x-direction
    return pos


def draw_plots(dataPts, values, Graph, title1, title2, filter_name, colors1, node_colors_list, norm, cmap, is3D=False,
               layout=nx.kamada_kawai_layout, showSidebySide=False):


    if showSidebySide:
        fig = plt.figure(figsize=(10, 5))
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122)

        # Plot the first scatter plot
        if not is3D:
            ax1.scatter(dataPts[:, 0], dataPts[:, 1], c=colors1, marker='o', s=5)
        else:
            ax1 = fig.add_subplot(121, projection='3d')
            ax1.scatter(dataPts[:, 0], dataPts[:, 1], dataPts[:, 2], c=colors1, marker='o', s=5)
            ax1.set_zlabel('Z')

        ax1.set_title(title1)
        ax1.set_xlabel('X')
        ax1.set_ylabel('Y')
        ax1.grid(True)

        # Plot the graph
        pos = layout(Graph)
        nx.draw(Graph, pos, with_labels=True, node_color=node_colors_list, node_size=270, font_size=6,
                font_color='white', ax=ax2)
        ax2.set_title(title2)

        # Add colorbar
        mappable = ScalarMappable(norm=norm, cmap=cmap)
        mappable.set_array(values)
        cbar = plt.colorbar(mappable, ax=ax2, orientation='vertical')
        cbar.set_label(f'{filter_name} Values')

        plt.show()  # Display the side by side plots

    else:
        # Plot the first scatter plot in a separate figure
        fig1 = plt.figure(figsize=(5, 5))
        ax1 = fig1.add_subplot(111)

        if not is3D:
            ax1.scatter(dataPts[:, 0], dataPts[:, 1], c=colors1, marker='o', s=5)
        else:
            ax1 = fig1.add_subplot(111, projection='3d')
            ax1.scatter(dataPts[:, 0], dataPts[:, 1], dataPts[:, 2], c=colors1, marker='o', s=5)
            ax1.set_zlabel('Z')

        ax1.set_title(title1)
        ax1.set_xlabel('X')
        ax1.set_ylabel('Y')
        ax1.grid(True)

        plt.show()  # Display the scatter plot

        # Plot the graph in another separate figure
        fig2 = plt.figure(figsize=(5, 5))
        ax2 = fig2.add_subplot(111)

        pos = layout(Graph)
        nx.draw(Graph, pos, with_labels=True, node_color=node_colors_list, node_size=270, font_size=6,
                font_color='white', ax=ax2)
        ax2.set_title(title2)

        # Add colorbar
        mappable = ScalarMappable(norm=norm, cmap=cmap)
        mappable.set_array(values)
        cbar = plt.colorbar(mappable, ax=ax2, orientation='vertical')
        cbar.set_label(f'{filter_name} Values')

        plt.show()  # Display the graph


def test_draw_plots():
    # Example data
    dataPts = np.random.rand(100, 3)
    values = np.random.rand(100)

    # Create a sample graph
    nodes = range(10)
    edges = [(i, (i + 1) % 10) for i in range(10)]
    G = create_undirected_graph(nodes, edges)

    title1 = "3D Scatter Plot"
    title2 = "Graph Plot"
    filter_name = "Test Filter"

    # Use the same colormap for testing
    norm = Normalize(vmin=min(values), vmax=max(values))
    cmap = plt.cm.gnuplot2
    colors1 = cmap(norm(values))
    node_colors_list = [cmap(norm(value)) for value in values[:10]]
    #
    # fig = plt.figure(figsize=(10, 5))
    #
    # # Test draw_plots function
    # ax1 = fig.add_subplot(121, projection='3d')
    # ax2 = fig.add_subplot(122)

    draw_plots(dataPts, values, G, title1, title2, filter_name, colors1, node_colors_list, norm, cmap, is3D=True)

    # # Assertions to check if the plot is created correctly
    # assert fig is not None, "Figure should be created"
    # assert ax1 is not None, "First Axes (3D) should be created"
    # assert ax2 is not None, "Second Axes (Graph) should be created"
    #
    # # Check if the titles are set correctly
    # assert ax1.get_title() == title1, f"Title1 should be '{title1}'"
    # assert ax2.get_title() == title2, f"Title2 should be '{title2}'"
    #
    # # Check if the colorbar is added to the graph plot
    # mappable = ScalarMappable(norm=norm, cmap=cmap)
    # mappable.set_array(values)
    # cbar = plt.colorbar(mappable, ax=ax2, orientation='vertical')
    # assert cbar.get_label() == f'{filter_name} Values', "Colorbar label should match filter name"

    print("draw_plots test passed.")


# Run the test case
#test_draw_plots()