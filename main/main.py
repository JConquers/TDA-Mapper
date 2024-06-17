import clustering as cls
import display as dsp
import myMapper.auxillary.dataStoreRetrieve as dsr
import myMapper.auxillary.dummy as dmy
import get_OpenCover as goc
import filter_functions as ff
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize
from inspect import signature
import networkx as nx
import numpy as np


class Mapper:
    def __init__(self, dataPts, filter, get_cov, get_cov_dataPts, is3D=False):
        self.dataPts = dataPts
        self.filter = filter # filter function
        self.get_cov_dataPts = get_cov_dataPts
        self.is3D = is3D
        self.title1 = ''
        self.title2 = ''
        self.filter_name = ''

        # Initialize resolution parameters with default values
        self.overlapRatio = 0.5
        self.sizeOfInterval = -1
        self.numOfIntervals = -1
        self.threshold = 0.27

        # Perform the checks for get_cov, get_cov_dataPts, and filter functions
        self._check_callable_with_params(get_cov, 3, "get_cov", ["values", "sizeOfIntervals", "overlapRatio"])
        self._check_callable_with_params(get_cov_dataPts, 3, "get_cov_dataPts", ["dataPts", "values", "paramCov"])
        self._check_callable_with_params(filter, 1, "filter", ["dataPts"])

        self.get_cov = get_cov

    @staticmethod
    def _check_callable_with_params(func, num_params, func_name, param_names):
        if not callable(func):
            raise ValueError(f"{func_name} must be a callable function.")

        sig = signature(func)
        if len(sig.parameters) != num_params:
            raise ValueError(
                f"{func_name} function must take exactly {num_params} arguments: {', '.join(param_names)}.")
    @staticmethod
    def set_resolution_params(mapper_instance, overlapRatio, sizeOfInterval, numOfIntervals, threshold):
        if not (0 <= overlapRatio <= 1):
            raise ValueError('overlapRatio must be a real number in [0, 1]')
        mapper_instance.overlapRatio = overlapRatio
        mapper_instance.sizeOfInterval = sizeOfInterval
        mapper_instance.numOfIntervals = numOfIntervals
        mapper_instance.threshold = threshold
    def apply_mapper(self, overlapRatio=None, sizeOfInterval=None, numOfIntervals=None, threshold=None, layout = nx.kamada_kawai_layout):

        if overlapRatio is not None or sizeOfInterval is not None or numOfIntervals is not None or threshold is not None:
            Mapper.set_resolution_params(
                self,
                overlapRatio if overlapRatio is not None else self.overlapRatio,
                sizeOfInterval if sizeOfInterval is not None else self.sizeOfInterval,
                numOfIntervals if numOfIntervals is not None else self.numOfIntervals,
                threshold if threshold is not None else self.threshold
            )
        loi = 0  # length of interval
        ovlpr = self.overlapRatio
        values = self.filter(points=self.dataPts)
        # ------------------------------------------------------------------------
        if self.numOfIntervals != -1:
            loi = (max(values) - min(values)) / self.numOfIntervals  # loi: Length of interval
        elif self.sizeOfInterval != -1:
            loi = self.sizeOfInterval
        # ------------------------------------------------------------------------
        paramCov = self.get_cov(values=values, sizeOfIntervals=self.sizeOfInterval, overlapRatio=self.overlapRatio)
        paramCov.sort()
        paramCovMeanValues = [(ele[0] + ele[1]) / 2 for ele in paramCov]
        dataPtsCov = self.get_cov_dataPts(dataPts=self.dataPts, values=values, paramCov=paramCov)

        clusterVertices = set()  # set of vertices
        edgeList = list()  #
        coveringToCluster = list()

        cls.partialCluster(threshold=self.threshold, pointsSet=self.dataPts, coveringSet=dataPtsCov,
                           clusterVertices=clusterVertices, edgeList=edgeList, coveringToCluster=coveringToCluster)
        G = []  # graph
        try:
            G = dsp.create_undirected_graph(nodes=clusterVertices, edges=edgeList)
        except TypeError:
            print("The output requires more than 1 dimensional complex to visualize.")
            exit(0)
        # ------------ setting colors scheme ------------------------
        norm = Normalize(vmin=min(values), vmax=max(values))
        cmap = plt.cm.viridis  # will be used for mapper output too
        colors = cmap(norm(values))  # colors for points in original dataset
        # -----------------------------------------------------------
        #dmy.plot_colored_subsets(dataPts=self.dataPts, colors=colors, dataPtsCov=dataPtsCov, covToclus=coveringToCluster)
        # Map the colors to the nodes
        node_colors = {}
        for i, cluster in enumerate(coveringToCluster):
            color_value = paramCovMeanValues[i]
            color = cmap(norm(color_value))
            for node in cluster:
                node_colors[node] = color

        # Create a list of colors for all nodes in the graph
        node_colors_list = [node_colors[node] for node in G.nodes()]

        dsp.draw_plots(dataPts=self.dataPts, values=values, Graph=G, title1=self.title1,
                       title2=self.title2, colors1=colors, node_colors_list=node_colors_list,
                       norm=norm, cmap=cmap, filter_name= self.filter_name, is3D=self.is3D,layout= layout, showSidebySide= True)
    def assign_naming(self, t1, t2, ff_name):
        self.title1 = t1
        self.title2 = t2
        self.filter_name = ff_name


def main():
    print("Mapper")
    # EXAMPLE 1: Noisy circle
    # dataPts, radius, noise_level, num_points, sizeOfInterval, overlapRatio = dsr.retrieve_data_noisy_circle("..\source\\noisy_circle.bin")
    # mymap = Mapper(dataPts, filter=ff.y_extract, get_cov=goc.get_cov_y_extract, get_cov_dataPts=goc.get_cov_y_extract_datapts, is3D=False)
    # mymap.assign_naming('Noisy Circle', 'Mapper Output', 'Vertical projection/Height')
    # mymap.apply_mapper(overlapRatio=overlapRatio, sizeOfInterval=sizeOfInterval, threshold=1)
    # print(f'Radius: {radius}\n'
    #       f'length of interval: {sizeOfInterval}\n'
    #       f'overlap ratio: {overlapRatio}\n'
    #       f'num of points: {num_points}\n'
    #       f'noise level (0-1): {noise_level}')

    # EXAMPLE 2: Noisy pair of internally touching cirlces
    # dataPts, circle1_radius, circle2_radius, num_points, noise_level, sizeOfInterval, overlapRatio = dsr.retrieve_data_noisy_pOITC("..\source\\noisy_pOITC.bin")
    # mymap = Mapper(dataPts, filter=ff.y_extract, get_cov=goc.get_cov_y_extract, get_cov_dataPts=goc.get_cov_y_extract_datapts, is3D=False)
    # mymap.assign_naming('Noisy Circle', 'Mapper Output', 'Vertical projection/Height')
    # mymap.apply_mapper(overlapRatio=overlapRatio, sizeOfInterval=sizeOfInterval, threshold=1)
    # print(f'c1 radius: {circle1_radius}, c2 radius: {circle2_radius}\n'
    #       f'length of interval: {sizeOfInterval}, overlap ratio: {overlapRatio}\n'
    #       f'num of points: {num_points}, noise level: {noise_level}\n')

    # EXAMPLE 3: Non-overlapping 2 armed spiral
    # dataPts = np.load('..\source\ma_spiral.npy')
    # mymap = Mapper(dataPts, filter=ff.y_extract, get_cov=goc.get_cov_y_extract, get_cov_dataPts=goc.get_cov_y_extract_datapts, is3D=False)
    # mymap.assign_naming('2-armed spiral', 'Mapper Output', 'Vertical projection/Height')
    # mymap.apply_mapper(overlapRatio=0.07, sizeOfInterval=2.5, threshold=0.55, layout= nx.spring_layout)

    # EXAMPLE 4: Non-overlapping 4 armed spiral
    # dataPts = np.load('..\source\our_spiral.npy')
    # mymap = Mapper(dataPts, filter=ff.y_extract, get_cov=goc.get_cov_y_extract, get_cov_dataPts=goc.get_cov_y_extract_datapts, is3D=False)
    # mymap.assign_naming('4-armed spiral', 'Mapper Output', 'Vertical projection/Height')
    # mymap.apply_mapper(overlapRatio=0.07, sizeOfInterval=10.5, threshold=0.3, layout=nx.spring_layout)
if __name__ == "__main__":
    main()