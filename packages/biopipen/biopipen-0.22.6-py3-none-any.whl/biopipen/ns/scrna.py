"""Tools to analyze single-cell RNA"""

from ..core.proc import Proc
from ..core.config import config
from ..utils.common_docstrs import (
    indent_docstr,
    format_placeholder,
    MUTATE_HELPERS_CLONESIZE,
)

MUTATE_HELPERS_CLONESIZE_INDENTED = indent_docstr(MUTATE_HELPERS_CLONESIZE, "    " * 3)


class SeuratLoading(Proc):
    """Seurat - Loading data

    Deprecated, should be superseded by SeuratPreparing

    Input:
        metafile: The metadata of the samples
            A tab-delimited file
            Two columns are required:
            - `Sample` to specify the sample names.
            - `RNAData` to assign the path of the data to the samples
              The path will be read by `Read10X()` from `Seurat`

    Output:
        rdsfile: The RDS file with a list of Seurat object

    Envs:
        qc: The QC filter for each sample.
            This will be passed to `subset(obj, subset=<qc>)`.
            For example
            `nFeature_RNA > 200 & nFeature_RNA < 2500 & percent.mt < 5`
    """

    input = "metafile:file"
    output = "rdsfile:file:{{in.metafile | stem}}.seurat.RDS"
    envs = {"qc": ""}
    lang = config.lang.rscript
    script = "file://../scripts/scrna/SeuratLoading.R"


class SeuratPreparing(Proc):
    """Load, prepare and apply QC to data, using `Seurat`

    This process will -
    - Prepare the seurat object
    - Apply QC to the data

    See also
    - <https://satijalab.org/seurat/articles/pbmc3k_tutorial.html#standard-pre-processing-workflow-1)>
    - <https://nbisweden.github.io/workshop-scRNAseq/labs/compiled/seurat/seurat_01_qc.html#Create_one_merged_object>

    This process will read the scRNA-seq data, based on the information provided by
    `SampleInfo`, specifically, the paths specified by the `RNAData` column.
    Those paths should be either paths to directoies containing `matrix.mtx`,
    `barcodes.tsv` and `features.tsv` files that can be loaded by
    [`Seurat::Read10X()`](https://satijalab.org/seurat/reference/read10x),
    or paths to `h5` files that can be loaded by
    [`Seurat::Read10X_h5()`](https://satijalab.org/seurat/reference/read10x_h5).

    Each sample will be loaded individually and then merged into one `Seurat` object, and then perform QC.

    In order to perform QC, some additional columns are added to the meta data of the `Seurat` object. They are:

    - `precent.mt`: The percentage of mitochondrial genes.
    - `percent.ribo`: The percentage of ribosomal genes.
    - `precent.hb`: The percentage of hemoglobin genes.
    - `percent.plat`: The percentage of platelet genes.

    Input:
        metafile: The metadata of the samples
            A tab-delimited file
            Two columns are required:
            `Sample` to specify the sample names.
            `RNAData` to assign the path of the data to the samples
            The path will be read by `Read10X()` from `Seurat`, or the path
            to the h5 file that can be read by `Read10X_h5()` from `Seurat`.

    Output:
        rdsfile: The RDS file with the Seurat object
            Note that the cell ids are preficed with sample names
            QC plots will be saved in `<job.outdir>/before-qc` and
            `<job.outdir>/after-qc`

    Envs:
        ncores (type=int): Number of cores to use.
            Used in `future::plan(strategy = "multicore", workers = <ncores>)`
            to parallelize some Seurat procedures.
        cell_qc: Filter expression to filter cells, using
            `tidyrseurat::filter()`.
            Available QC keys include `nFeature_RNA`, `nCount_RNA`,
            `percent.mt`, `percent.ribo`, `percent.hb`, and `percent.plat`.

            /// Tip | Example
            Including the columns added above, all available QC keys include
            `nFeature_RNA`, `nCount_RNA`, `percent.mt`, `percent.ribo`, `percent.hb`,
            and `percent.plat`. For example:

            ```toml
            [SeuratPreparing.envs]
            cell_qc = "nFeature_RNA > 200 & percent.mt < 5"
            ```
            will keep cells with more than 200 genes and less than 5%% mitochondrial
            genes.
            ///

        gene_qc (ns): Filter genes. Currently only `min_cells` is supported.
            `gene_qc` is applied after `cell_qc`.
            - min_cells: The minimum number of cells that a gene must be
                expressed in to be kept.

            /// Tip | Example
            ```toml
            [SeuratPreparing.envs]
            gene_qc = { min_cells = 3 }
            ```
            will keep genes that are expressed in at least 3 cells.
            ///

    Requires:
        r-seurat:
            - check: {{proc.lang}} <(echo "library(Seurat)")
        r-future:
            - check: {{proc.lang}} <(echo "library(future)")
        r-bracer:
            - check: {{proc.lang}} <(echo "library(bracer)")
    """  # noqa: E501
    input = "metafile:file"
    output = "rdsfile:file:{{in.metafile | stem}}.seurat.RDS"
    lang = config.lang.rscript
    envs = {
        "ncores": config.misc.ncores,
        "cell_qc": None,  # "nFeature_RNA > 200 & percent.mt < 5",
        "gene_qc": {"min_cells": 3},
    }
    script = "file://../scripts/scrna/SeuratPreparing.R"
    plugin_opts = {
        "report": "file://../reports/scrna/SeuratPreparing.svelte",
    }


class SeuratClustering(Proc):
    """Determine the clusters of cells without reference using Seurat FindClusters
    procedure.

    To perform the clustering, you have two routes to choose from:

    1. Performing integration on datasets normalized with `SCTransform`
        - See: [https://satijalab.org/seurat/articles/integration_rpca.html#performing-integration-on-datasets-normalized-with-sctransform-1](https://satijalab.org/seurat/articles/integration_rpca.html#performing-integration-on-datasets-normalized-with-sctransform-1)
    2. Fast integration using reciprocal PCA (`RPCA`)
        - See: [https://satijalab.org/seurat/articles/integration_rpca.html](https://satijalab.org/seurat/articles/integration_rpca.html)

    Input:
        srtobj: The seurat object loaded by SeuratPreparing

    Output:
        rdsfile: The seurat object with cluster information

    Envs:
        ncores (type=int;order=-100): Number of cores to use.
            Used in `future::plan(strategy = "multicore", workers = <ncores>)`
            to parallelize some Seurat procedures.
            See also: <https://satijalab.org/seurat/articles/future_vignette.html>
        use_sct (flag;order=-99): Whether use SCTransform routine or not
            If `True`, following procedures will be performed in the order:
            * [`SplitObject`](https://satijalab.org/seurat/reference/splitobject).
            * [`SCTransform*`](https://satijalab.org/seurat/reference/sctransform).
            * [`SelectIntegrationFeatures`](https://satijalab.org/seurat/reference/selectintegrationfeatures).
            * [`PrepSCTIntegration`](https://satijalab.org/seurat/reference/prepsctintegration).
            * [`RunPCA*`](https://satijalab.org/seurat/reference/runpca).
            * [`FindIntegrationAnchors`](https://satijalab.org/seurat/reference/findintegrationanchors).
            * [`IntegrateData`](https://satijalab.org/seurat/reference/integratedata).
            * [`RunPCA`](https://satijalab.org/seurat/reference/runpca).
            * [`RunUMAP`](https://satijalab.org/seurat/reference/runumap).
            * [`FindNeighbors`](https://satijalab.org/seurat/reference/findneighbors).
            * [`FindClusters`](https://satijalab.org/seurat/reference/findclusters).
            * `*`: On each sample
            See <https://satijalab.org/seurat/articles/integration_rpca.html#performing-integration-on-datasets-normalized-with-sctransform-1>.
            If `False`, fast integration will be performed, using reciprocal PCA (RPCA) and
            following procedures will be performed in the order:
            * [`SplitObject`](https://satijalab.org/seurat/reference/splitobject).
            * [`NormalizeData*`](https://satijalab.org/seurat/reference/normalizedata).
            * [`FindVariableFeatures*`](https://satijalab.org/seurat/reference/findvariablefeatures).
            * [`SelectIntegrationFeatures`](https://satijalab.org/seurat/reference/selectintegrationfeatures).
            * [`ScaleData*`](https://satijalab.org/seurat/reference/scaledata).
            * [`RunPCA*`](https://satijalab.org/seurat/reference/runpca).
            * [`FindIntegrationAnchors`](https://satijalab.org/seurat/reference/findintegrationanchors).
            * [`IntegrateData`](https://satijalab.org/seurat/reference/integratedata).
            * [`ScaleData`](https://satijalab.org/seurat/reference/scaledata).
            * [`RunPCA`](https://satijalab.org/seurat/reference/runpca).
            * [`RunUMAP`](https://satijalab.org/seurat/reference/runumap).
            * [`FindNeighbors`](https://satijalab.org/seurat/reference/findneighbors).
            * [`FindClusters`](https://satijalab.org/seurat/reference/findclusters).
            * `*`: On each sample.
            See <https://satijalab.org/seurat/articles/integration_rpca.html>.
        SCTransform (ns): Arguments for [`SCTransform()`](https://satijalab.org/seurat/reference/sctransform).
            `object` is specified internally, and `-` in the key will be replaced with `.`.
            - <more>: See <https://satijalab.org/seurat/reference/sctransform>.
        SelectIntegrationFeatures (ns): Arguments for [`SelectIntegrationFeatures()`](https://satijalab.org/seurat/reference/selectintegrationfeatures).
            `object.list` is specified internally, and `-` in the key will be replaced with `.`.
            - nfeatures (type=int): The number of features to select
            - <more>: See <https://satijalab.org/seurat/reference/selectintegrationfeatures>
        PrepSCTIntegration (ns): Arguments for [`PrepSCTIntegration()`](https://satijalab.org/seurat/reference/prepsctintegration).
            `object.list` and `anchor.features` is specified internally, and `-` in the key will be replaced with `.`.
            - <more>: See <https://satijalab.org/seurat/reference/prepsctintegration>
        NormalizeData (ns): Arguments for [`NormalizeData()`](https://satijalab.org/seurat/reference/normalizedata).
            `object` is specified internally, and `-` in the key will be replaced with `.`.
            - <more>: See <https://satijalab.org/seurat/reference/normalizedata>
        FindVariableFeatures (ns): Arguments for [`FindVariableFeatures()`](https://satijalab.org/seurat/reference/findvariablefeatures).
            `object` is specified internally, and `-` in the key will be replaced with `.`.
            - <more>: See <https://satijalab.org/seurat/reference/findvariablefeatures>
        FindIntegrationAnchors (ns): Arguments for [`FindIntegrationAnchors()`](https://satijalab.org/seurat/reference/findintegrationanchors).
            `object.list` and `anchor.features` is specified internally, and `-` in the key will be replaced with `.`.
            `dims=N` will be expanded to `dims=1:N`; The maximal value of `N` will be the minimum of `N` and the number of columns for each sample.
            Sample names can also be specified in `reference` instead of indices only.
            `reduction` defaults to `rpca`.
            `normalization.method` defaults to `SCT` if `use_sct` is `True`.
            **If you want to use reference-based integration, you can also set `reference` to a list of sample names, instead of a list of indices.**
            - <more>: See <https://satijalab.org/seurat/reference/findintegrationanchors>
        IntegrateData (ns): Arguments for [`IntegrateData()`](https://satijalab.org/seurat/reference/integratedata).
            `anchorset` is specified internally, and `-` in the key will be replaced with `.`.
            `dims=N` will be expanded to `dims=1:N`; The maximal value of `N` will be the minimum of `N` and the number of columns for each sample.
            `normalization.method` defaults to `SCT` if `use_sct` is `True`.
            - <more>: See <https://satijalab.org/seurat/reference/integratedata>
        ScaleData (ns): Arguments for [`ScaleData()`](https://satijalab.org/seurat/reference/scaledata).
            `object` and `features` is specified internally, and `-` in the key will be replaced with `.`.
            - verbose (flag): Whether to print the progress
            - <more>: See <https://satijalab.org/seurat/reference/scaledata>
        ScaleData1 (ns): Arguments for [`ScaleData()`](https://satijalab.org/seurat/reference/scaledata) that runs on each sample.
            `object` and `features` is specified internally, and `-` in the key will be replaced with `.`.
            - verbose (flag): Whether to print the progress
            - <more>: See <https://satijalab.org/seurat/reference/scaledata>
        RunPCA (ns): Arguments for [`RunPCA()`](https://satijalab.org/seurat/reference/runpca).
            `object` and `features` is specified internally, and `-` in the key will be replaced with `.`.
            - npcs (type=int): The number of PCs to compute.
                For each sample, `npcs` will be no larger than the number of columns - 1.
            - verbose (flag): Whether to print the progress
            - <more>: See <https://satijalab.org/seurat/reference/runpca>
        RunPCA1 (ns): Arguments for [`RunPCA()`](https://satijalab.org/seurat/reference/runpca) on each sample.
            `object` and `features` is specified internally, and `-` in the key will be replaced with `.`.
            - npcs (type=int): The number of PCs to compute.
                For each sample, `npcs` will be no larger than the number of columns - 1.
            - verbose (flag): Whether to print the progress
            - <more>: See <https://satijalab.org/seurat/reference/runpca>
        RunUMAP (ns): Arguments for [`RunUMAP()`](https://satijalab.org/seurat/reference/runumap).
            `object` is specified internally, and `-` in the key will be replaced with `.`.
            `dims=N` will be expanded to `dims=1:N`; The maximal value of `N` will be the minimum of `N` and the number of columns - 1 for each sample.
            - dims (type=int): The number of PCs to use
            - reduction: The reduction to use for UMAP
            - <more>: See <https://satijalab.org/seurat/reference/runumap>
        FindNeighbors (ns): Arguments for [`FindNeighbors()`](https://satijalab.org/seurat/reference/findneighbors).
            `object` is specified internally, and `-` in the key will be replaced with `.`.
            - <more>: See <https://satijalab.org/seurat/reference/findneighbors>
        FindClusters (ns): Arguments for [`FindClusters()`](https://satijalab.org/seurat/reference/findclusters).
            `object` is specified internally, and `-` in the key will be replaced with `.`.
            - resolution (type=float): The resolution of the clustering
            - <more>: See <https://satijalab.org/seurat/reference/findclusters>
        cache (type=auto): Whether to cache the seurat object with cluster information.
            If `True`, the seurat object will be cached in the job output directory, which will be not cleaned up when job is rerunning.
            The cached seurat object will be saved as `<signature>.cached.RDS` file, where `<signature>` is the signature determined by
            the input and envs of the process.
            See <https://github.com/satijalab/seurat/issues/7849>, <https://github.com/satijalab/seurat/issues/5358> and
            <https://github.com/satijalab/seurat/issues/6748> for more details.
            To not use the cached seurat object, you can either set `cache` to `False` or delete the cached file at
            `.pipen/<Pipeline>/SeuratClustering/0/output/<signature>.cached.RDS`.
            You can also specify the directory to save the cached seurat object by setting `cache` to the directory path.


    Requires:
        r-seurat:
            - check: {{proc.lang}} <(echo "library(Seurat)")
        r-tidyr:
            - check: {{proc.lang}} <(echo "library(tidyr)")
        r-dplyr:
            - check: {{proc.lang}} <(echo "library(dplyr)")
    """  # noqa: E501
    input = "srtobj:file"
    output = "rdsfile:file:{{in.srtobj | stem}}.RDS"
    lang = config.lang.rscript
    envs = {
        "ncores": config.misc.ncores,
        "use_sct": False,
        "SCTransform": {},
        "SelectIntegrationFeatures": {"nfeatures": 3000},
        "PrepSCTIntegration": {},
        "NormalizeData": {},
        "FindVariableFeatures": {},
        "FindIntegrationAnchors": {},
        "IntegrateData": {},
        "ScaleData": {"verbose": False},
        "ScaleData1": {"verbose": False},
        "RunPCA": {"verbose": False},
        "RunPCA1": {"verbose": False},
        "RunUMAP": {"reduction": "pca", "dims": 30},
        "FindNeighbors": {},
        "FindClusters": {"resolution": 0.8},
        "cache": True,
    }
    script = "file://../scripts/scrna/SeuratClustering.R"


class SeuratClusterStats(Proc):
    """Statistics of the clustering.

    Including the number/fraction of cells in each cluster, the gene expression values
    and dimension reduction plots. It's also possible to perform stats on
    TCR clones/clusters or other metadata for each T-cell cluster.

    Examples:
        ### Number of cells in each cluster

        ```toml
        [SeuratClusterStats.envs.stats]
        # suppose you have nothing set in `envs.stats_defaults`
        # otherwise, the settings will be inherited here
        nCells_All = { }
        ```

        ![nCells_All](https://pwwang.github.io/immunopipe/processes/images/SeuratClusterStats_nCells_All.png){: width="80%" }

        ### Number of cells in each cluster by groups

        ```toml
        [SeuratClusterStats.envs.stats]
        nCells_Sample = { group-by = "Sample" }
        ```

        ![nCells_Sample](https://pwwang.github.io/immunopipe/processes/images/SeuratClusterStats_nCells_Sample.png){: width="80%" }

        ### Violin plots for the gene expressions

        ```toml
        [SeuratClusterStats.envs.features]
        features = "CD4,CD8A"
        # Remove the dots in the violin plots
        vlnplots = { pt-size = 0, kind = "vln" }
        # Don't use the default genes
        vlnplots_1 = { features = ["FOXP3", "IL2RA"], pt-size = 0, kind = "vln" }
        ```

        ![vlnplots](https://pwwang.github.io/immunopipe/processes/images/SeuratClusterStats_vlnplots.png){: width="80%" }
        ![vlnplots_1](https://pwwang.github.io/immunopipe/processes/images/SeuratClusterStats_vlnplots_1.png){: width="80%" }

        ### Dimension reduction plot with labels

        ```toml
        [SeuratClusterStats.envs.dimplots.Idents]
        label = true
        label-box = true
        repel = true
        ```

        ![dimplots](https://pwwang.github.io/immunopipe/processes/images/SeuratClusterStats_dimplots.png){: width="80%" }

    Input:
        srtobj: The seurat object loaded by `SeuratClustering`

    Output:
        outdir: The output directory

    Envs:
        stats_defaults (ns): The default parameters for `stats`.
            The parameters from the cases can overwrite the default parameters.
            - frac (flag): Whether to output the fraction of cells instead of number.
            - pie (flag): Also output a pie chart?
            - table (flag): Whether to output a table (in tab-delimited format) and in the report.
            - ident: The column name in metadata to use as the identity.
            - group-by: The column name in metadata to group the cells.
                Does NOT support for pie charts.
            - split-by: The column name in metadata to split the cells into
                different plots.
            - subset: An expression to subset the cells, will be passed to
                `dplyr::filter()` on metadata.
            - devpars (ns): The device parameters for the plots.
                - res (type=int): The resolution of the plots.
                - height (type=int): The height of the plots.
                - width (type=int): The width of the plots.
        stats (type=json): The number/fraction of cells to plot.
            Keys are the names of the plots and values are the dicts inherited from `env.stats_defaults`.
            Here are some examples -
            >>> {
            >>>     "nCells_All": {},
            >>>     "nCells_Sample": {"kind": "num", "group-by": "Sample"},
            >>>     "fracCells_Sample": {"kind": "frac", "group-by": "Sample"},
            >>> }
        features_defaults (ns): The default parameters for `features`.
            - features: The features to plot.
                It can be either a string with comma separated features, a list of features, a file path with `file://` prefix with features
                (one per line), or an integer to use the top N features from `VariantFeatures(srtobj)`.
            - ident: The column name in metadata to use as the identity.
            - subset: An expression to subset the cells, will be passed to `tidyrseurat::filter()`.
            - devpars (ns): The device parameters for the plots. Does not work for `table`.
                - res (type=int): The resolution of the plots.
                - height (type=int): The height of the plots.
                - width (type=int): The width of the plots.
            - plus: The extra elements to add to the `ggplot` object. Does not work for `table`.
            - group-by: Group cells in different ways (for example, orig.ident). Works for `ridge`, `vln`, and `dot`.
                It also works for `feature` as `shape.by` being passed to [`Seurat::FeaturePlot`](https://satijalab.org/seurat/reference/featureplot).
            - split-by: The column name in metadata to split the cells into different plots.
                It works for `vln`, `feature`, and `dot`.
            - assay: The assay to use.
            - slot: The slot to use.
            - section: The section to put the plot in the report.
                If not specified, the case title will be used.
            - ncol (type=int): The number of columns for the plots.
            - kind (choice): The kind of the plot or table.
                - ridge: Use `Seurat::RidgePlot`.
                - ridgeplot: Same as `ridge`.
                - vln: Use `Seurat::VlnPlot`.
                - vlnplot: Same as `vln`.
                - violin: Same as `vln`.
                - violinplot: Same as `vln`.
                - feature: Use `Seurat::FeaturePlot`.
                - featureplot: Same as `feature`.
                - dot: Use `Seurat::DotPlot`.
                - dotplot: Same as `dot`.
                - heatmap: Use `Seurat::DoHeatmap`.
                    You can specify `average=True` to plot on the average of the expressions.
                - table: The table for the features, only gene expressions are supported.
                    (supported keys: ident, subset, and features).
        features (type=json): The plots for features, include gene expressions, and columns from metadata.
            Keys are the titles of the cases and values are the dicts inherited from `env.features_defaults`. It can also have other parameters from
            each Seurat function used by `kind`. Note that for argument name with `.`, you should use `-` instead.
        dimplots_defaults (ns): The default parameters for `dimplots`.
            - ident: The column name in metadata to use as the identity.
                Ignored if `group-by` is specified.
            - group-by: Same as `ident`. How the points are colored.
            - split-by: The column name in metadata to split the cells into different plots.
            - shape-by: The column name in metadata to use as the shape.
            - subset: An expression to subset the cells, will be passed to `tidyrseurat::filter()`.
            - devpars (ns): The device parameters for the plots.
                - res (type=int): The resolution of the plots.
                - height (type=int): The height of the plots.
                - width (type=int): The width of the plots.
            - reduction (choice): Which dimensionality reduction to use.
                - dim: Use `Seurat::DimPlot`.
                    First searches for `umap`, then `tsne`, then `pca`.
                - auto: Same as `dim`
                - umap: Use `Seurat::UMAPPlot`.
                - tsne: Use `Seurat::TSNEPlot`.
                - pca: Use `Seurat::PCAPlot`.
            - <more>: See <https://satijalab.org/seurat/reference/dimplot>
        dimplots (type=json): The dimensional reduction plots.
            Keys are the titles of the plots and values are the dicts inherited from `env.dimplots_defaults`. It can also have other parameters from
            [`Seurat::DimPlot`](https://satijalab.org/seurat/reference/dimplot).

    Requires:
        r-seurat:
            - check: {{proc.lang}} -e "library(Seurat)"
    """  # noqa: E501
    input = "srtobj:file"
    output = "outdir:dir:{{in.srtobj | stem}}.cluster_stats"
    lang = config.lang.rscript
    envs = {
        "stats_defaults": {
            "frac": False,
            "pie": False,
            "table": False,
            "ident": "seurat_clusters",
            "group-by": None,
            "split-by": None,
            "subset": None,
            "devpars": {"res": 100, "height": 800, "width": 1000},
        },
        "stats": {
            "Number of cells in each cluster": {
                "pie": True,
            },
            "Number of cells in each cluster by Sample": {
                "group-by": "Sample",
                "table": True,
                "frac": True,
            },
        },
        "features_defaults": {
            "features": None,
            "ident": "seurat_clusters",
            "subset": None,
            "devpars": {"res": 100},
            "plus": None,
            "group-by": None,
            "split-by": None,
            "assay": None,
            "section": None,
            "slot": None,
            "kind": None,
            "ncol": 2,
        },
        "features": {},
        "dimplots_defaults": {
            "ident": "seurat_clusters",
            "group-by": None,
            "split-by": None,
            "shape-by": None,
            "subset": None,
            "reduction": "dim",
            "devpars": {"res": 100, "height": 800, "width": 1000},
        },
        "dimplots": {
            "Dimensional reduction plot": {
                "label": True,
                "label-box": True,
                "repel": True,
            },
        },
    }
    script = "file://../scripts/scrna/SeuratClusterStats.R"
    plugin_opts = {
        "report": "file://../reports/scrna/SeuratClusterStats.svelte"
    }


class ModuleScoreCalculator(Proc):
    """Calculate the module scores for each cell

    The module scores are calculated by
    [`Seurat::AddModuleScore()`](https://satijalab.org/seurat/reference/addmodulescore)
    or [`Seurat::CellCycleScoring()`](https://satijalab.org/seurat/reference/cellcyclescoring)
    for cell cycle scores.

    The module scores are calculated as the average expression levels of each
    program on single cell level, subtracted by the aggregated expression of
    control feature sets. All analyzed features are binned based on averaged
    expression, and the control features are randomly selected from each bin.

    Input:
        srtobj: The seurat object loaded by `SeuratClustering`

    Output:
        rdsfile: The seurat object with module scores

    Envs:
        defaults (ns): The default parameters for `modules`.
            - features: The features to calculate the scores. Multiple features
                should be separated by comma.
                You can also specify `cc.genes` or `cc.genes.updated.2019` to
                use the cell cycle genes to calculate cell cycle scores.
                If so, three columns will be added to the metadata, including
                `S.Score`, `G2M.Score` and `Phase`.
                Only one type of cell cycle scores can be calculated at a time.
            - nbin (type=int): Number of bins of aggregate expression levels
                for all analyzed features.
            - ctrl (type=int): Number of control features selected from
                the same bin per analyzed feature.
            - k (flag): Use feature clusters returned from `DoKMeans`.
            - assay: The assay to use.
            - seed (type=int): Set a random seed.
            - search (flag): Search for symbol synonyms for features in
                features that don't match features in object?
            - keep (flag): Keep the scores for each feature?
                Only works for non-cell cycle scores.
            - agg (choice): The aggregation function to use.
                Only works for non-cell cycle scores.
                - mean: The mean of the expression levels
                - median: The median of the expression levels
                - sum: The sum of the expression levels
                - max: The max of the expression levels
                - min: The min of the expression levels
                - var: The variance of the expression levels
                - sd: The standard deviation of the expression levels
        modules (type=json): The modules to calculate the scores.
            Keys are the names of the expression programs and values are the
            dicts inherited from `env.defaults`.
            Here are some examples -
            >>> {
            >>>     "CellCycle": {"features": "cc.genes.updated.2019"},
            >>>     "Exhaustion": {"features": "HAVCR2,ENTPD1,LAYN,LAG3"},
            >>>     "Activation": {"features": "IFNG"},
            >>>     "Proliferation": {"features": "STMN1,TUBB"}
            >>> }
    """  # noqa: E501
    input = "srtobj:file"
    output = "rdsfile:file:{{in.srtobj | stem}}.RDS"
    lang = config.lang.rscript
    envs = {
        "defaults": {
            "features": None,
            "nbin": 24,
            "ctrl": 100,
            "k": False,
            "assay": "RNA",
            "seed": 8525,
            "search": False,
            "keep": False,
            "agg": "mean",
        },
        "modules": {
            # "CellCycle": {"features": "cc.genes.updated.2019"},
            # "Exhaustion": {"features": "HAVCR2,ENTPD1,LAYN,LAG3"},
            # "Activation": {"features": "IFNG"},
            # "Proliferation": {"features": "STMN1,TUBB"},
        },
    }
    script = "file://../scripts/scrna/ModuleScoreCalculator.R"


@format_placeholder(mutate_helpers_clonesize=MUTATE_HELPERS_CLONESIZE_INDENTED)
class CellsDistribution(Proc):
    """Distribution of cells (i.e. in a TCR clone) from different groups
    for each cluster

    This generates a set of pie charts with proportion of cells in each cluster
    Rows are the cells identities (i.e. TCR clones or TCR clusters), columns
    are groups (i.e. clinic groups).

    Examples:
        ```toml
        [CellsDistribution.envs.mutaters]
        # Add Patient1_Tumor_Expanded column with CDR3.aa that
        # expands in Tumor of patient 1
        Patient1_Tumor_Expanded = '''
          expanded(., region, "Tumor", subset = patient == "Lung1", uniq = FALSE)
        '''

        [CellsDistribution.envs.cases.Patient1_Tumor_Expanded]
        cells_by = "Patient1_Tumor_Expanded"
        cells_orderby = "desc(CloneSize)"
        group_by = "region"
        group_order = [ "Tumor", "Normal" ]
        ```

        ![CellsDistribution_example](https://pwwang.github.io/immunopipe/processes/images/CellsDistribution_example.png)

    Input:
        srtobj: The seurat object in RDS format

    Output:
        outdir: The output directory

    Envs:
        mutaters (type=json): The mutaters to mutate the metadata
            Keys are the names of the mutaters and values are the R expressions
            passed by `dplyr::mutate()` to mutate the metadata.
            %(mutate_helpers_clonesize)s
        group_by: The column name in metadata to group the cells for the columns of the plot.
        group_order (list): The order of the groups (columns) to show on the plot
        cells_by: The column name in metadata to group the cells for the rows of the plot.
            If your cell groups have overlapping cells, you can also use multiple columns, separated by comma (`,`).
            These columns will be concatenated to form the cell groups. For the overlapping cells, they will be
            counted multiple times for different groups. So make sure the cell group names in different columns
            are unique.
        cells_order (list): The order of the cells (rows) to show on the plot
        cells_orderby: An expression passed to `dplyr::arrange()` to order the cells (rows) of the plot.
            Only works when `cells-order` is not specified.
            The data frame passed to `dplyr::arrange()` is grouped by `cells_by` before ordering.
            You can have multiple expressions separated by semicolon (`;`). The expessions will be parsed by `rlang::parse_exprs()`.
            4 extra columns were added to the metadata for ordering the rows in the plot:
            * `CloneSize`: The size (number of cells) of clones (identified by `cells_by`)
            * `CloneGroupSize`: The clone size in each group (identified by `group_by`)
            * `CloneClusterSize`: The clone size in each cluster (identified by `seurat_clusters`)
            * `CloneGroupClusterSize`: The clone size in each group and cluster (identified by `group_by` and `seurat_clusters`)
        cells_n (type=int): The max number of groups to show for each cell group identity (row).
            Ignored if `cells_order` is specified.
        subset: An expression to subset the cells, will be passed to `dplyr::filter()` on metadata.
            This will be applied prior to `each`.
        descr: The description of the case, will be shown in the report.
        devpars (ns): The device parameters for the plots.
            - res (type=int): The resolution of the plots
            - height (type=int): The height of the plots
            - width (type=int): The width of the plots
        each: The column name in metadata to separate the cells into different plots.
        section: The section to show in the report. This allows different cases to be put in the same section in report.
            Only works when `each` is not specified.
        overlap (list): Plot the overlap of cells in different cases under the same section.
            The section must have at least 2 cases.
        cases (type=json;order=99): If you have multiple cases, you can specify them here.
            Keys are the names of the cases and values are the options above except `mutaters`.
            If some options are not specified, the options in `envs` will be used.
            If no cases are specified, a default case will be used with case name `DEFAULT`.

    Requires:
        r-seurat:
            - check: {{proc.lang}} -e "library(Seurat)"
        r-dplyr:
            - check: {{proc.lang}} -e "library(dplyr)"
        r-tidyr:
            - check: {{proc.lang}} -e "library(tidyr)"
    """  # noqa: E501
    input = "srtobj:file"
    output = "outdir:dir:{{in.srtobj | stem}}.cells_distribution"
    lang = config.lang.rscript
    envs = {
        "mutaters": {},
        "group_by": None,
        "group_order": [],
        "cells_by": None,
        "cells_order": [],
        "cells_orderby": None,
        "cells_n": 10,
        "subset": None,
        "descr": None,
        "devpars": {},
        "each": None,
        "section": "DEFAULT",
        "overlap": [],
        "cases": {},
    }
    script = "file://../scripts/scrna/CellsDistribution.R"
    plugin_opts = {
        "report": "file://../reports/scrna/CellsDistribution.svelte",
        "report_paging": 8,
    }


@format_placeholder(mutate_helpers_clonesize=MUTATE_HELPERS_CLONESIZE_INDENTED)
class SeuratMetadataMutater(Proc):
    """Mutate the metadata of the seurat object

    Input:
        srtobj: The seurat object loaded by SeuratPreparing
        metafile: Additional metadata
            A tab-delimited file with columns as meta columns and rows as
            cells.

    Output:
        rdsfile: The seurat object with the additional metadata

    Envs:
        mutaters (type=json): The mutaters to mutate the metadata.
            The key-value pairs will be passed the `dplyr::mutate()` to mutate the metadata.
            %(mutate_helpers_clonesize)s

    Requires:
        r-seurat:
            - check: {{proc.lang}} <(echo "library(Seurat)")
        r-tibble:
            - check: {{proc.lang}} <(echo "library(tibble)")
        r-dplyr:
            - check: {{proc.lang}} <(echo "library(dplyr)")
    """  # noqa: E501
    input = "srtobj:file, metafile:file"
    output = "rdsfile:file:{{in.srtobj | stem}}.RDS"
    lang = config.lang.rscript
    envs = {"mutaters": {}}
    script = "file://../scripts/scrna/SeuratMetadataMutater.R"


class GeneExpressionInvestigation(Proc):
    """Investigation of expressions of genes of interest

    Input:
        srtobj: The seurat object loaded by `SeuratPreparing`
        genefile: The genes to show their expressions in the plots
            Either one column or two columns.
            If one column, the column name will be used as both the gene names
            to match the expressions and the names to show in the plots
            If two columns, the first column will be used as the gene names
            to match the expressions and the second column will be used to
            show in the plots.
        configfile: The configuration file (toml). See `envs.config`
            If not provided, use `envs.config`

    Output:
        outdir: The output directory with the plots

    Envs:
        gopts: Options for `read.table()` to read `in.genefile`
        config: The configurations to do the plots
            name: The name of the job, mostly used in report
            mutaters: The mutater to mutate the metadata
            groupby: Which meta columns to group the data
            subset: Select a subset of cells, will be passed to
                `subset(obj, subset=<subset>)`
            plots: Plots to generate
                Currently supported
                `boxplot`:
                - `ncol`: Split the plot to how many columns?
                - `res`, `height` and `width` the parameters for `png()`
                `heatmap`:
                - `res`, `height` and `width` the parameters for `png()`
                - other arguments for `ComplexHeatmap::Heatmap()`
    """
    input = "srtobj:file, genefile:file, configfile:file"
    output = "outdir:dir:{{in.configfile | stem0}}.gei"
    lang = config.lang.rscript
    order = 4
    envs = {
        "config": {},
        "gopts": {
            "header": False,
            "row.names": None,
            "sep": "\t",
            "check.names": False,
        },
    }
    script = "file://../scripts/scrna/GeneExpressionInvistigation.R"
    plugin_opts = {
        "report": "file://../reports/scrna/GeneExpressionInvistigation.svelte"
    }


class DimPlots(Proc):
    """Seurat - Dimensional reduction plots

    Input:
        srtobj: The seruat object in RDS format
        configfile: A toml configuration file with "cases"
            If this is given, `envs.cases` will be overriden
        name: The name of the job, used in report

    Output:
        outdir: The output directory

    Envs:
        cases: The cases for the dim plots
            Keys are the names and values are the arguments to
            `Seurat::Dimplots`
    """
    input = "srtobj:file, configfile:file, name:var"
    output = "outdir:dir:{{in.srtobj | stem}}.dimplots"
    lang = config.lang.rscript
    script = "file://../scripts/scrna/DimPlots.R"
    envs = {"cases": {"Ident": {"group.by": "ident"}}}
    plugin_opts = {
        "report": "file://../reports/scrna/DimPlots.svelte",
        "report_toc": False,
    }


@format_placeholder(mutate_helpers_clonesize=MUTATE_HELPERS_CLONESIZE_INDENTED)
class MarkersFinder(Proc):
    """Find markers between different groups of cells

    When only `group-by` is specified as `"seurat_clusters"` in
    `envs.cases`, the markers will be found for all the clusters.

    You can also find the differentially expressed genes between
    any two groups of cells by setting `group-by` to a different
    column name in metadata. Follow `envs.cases` for more details.

    Input:
        srtobj: The seurat object loaded by `SeuratPreparing`

    Output:
        outdir: The output directory for the markers

    Envs:
        ncores (type=int): Number of cores to use for parallel computing for some `Seurat` procedures.
            * Used in `future::plan(strategy = "multicore", workers = <ncores>)` to parallelize some Seurat procedures.
            * See also: <https://satijalab.org/seurat/articles/future_vignette.html>
        mutaters (type=json): The mutaters to mutate the metadata
            %(mutate_helpers_clonesize)s
        ident-1: The first group of cells to compare
        ident-2: The second group of cells to compare
            If not provided, the rest of the cells are used for `ident-2`.
        group-by: The column name in metadata to group the cells.
            If only `group-by` is specified, and `ident-1` and `ident-2` are
            not specified, markers will be found for all groups in this column
            in the manner of "group vs rest" comparison.
            `NA` group will be ignored.
        each: The column name in metadata to separate the cells into different
            cases.
        prefix_each (flag): Whether to prefix the `each` column name to the
            value as the case/section name.
        dbs (list): The dbs to do enrichment analysis for significant
            markers See below for all libraries.
            <https://maayanlab.cloud/Enrichr/#libraries>
        sigmarkers: An expression passed to `dplyr::filter()` to filter the
            significant markers for enrichment analysis.
            Available variables are `p_val`, `avg_log2FC`, `pct.1`, `pct.2` and
            `p_val_adj`. For example, `"p_val_adj < 0.05 & abs(avg_log2FC) > 1"`
            to select markers with adjusted p-value < 0.05 and absolute log2
            fold change > 1.
        assay: The assay to use.
        volcano_genes (type=auto): The genes to label in the volcano plot if they are
            significant markers.
            If `True`, all significant markers will be labeled. If `False`, no
            genes will be labeled. Otherwise, specify the genes to label.
            It could be either a string with comma separated genes, or a list
            of genes.
        section: The section name for the report. It must not contain colon (`:`).
            Ignored when `each` is not specified and `ident-1` is specified.
            When neither `each` nor `ident-1` is specified, case name will be used
            as section name.
            If `each` is specified, the section name will be constructed from
            `each` and case name.
        subset: An expression to subset the cells for each case.
        rest (ns): Rest arguments for `Seurat::FindMarkers()`.
            Use `-` to replace `.` in the argument name. For example,
            use `min-pct` instead of `min.pct`.
            - <more>: See <https://satijalab.org/seurat/reference/findmarkers>
        dotplot (ns): Arguments for `Seurat::DotPlot()`.
            Use `-` to replace `.` in the argument name. For example,
            use `group-bar` instead of `group.bar`.
            Note that `object`, `features`, and `group-by` are already specified
            by this process. So you don't need to specify them here.
            - devpars (ns): The device parameters for the plots.
                - res (type=int): The resolution of the plots.
                - height (type=int): The height of the plots.
                - width (type=int): The width of the plots.
            - <more>: See <https://satijalab.org/seurat/reference/doheatmap>
        cases (type=json): If you have multiple cases, you can specify them
            here. The keys are the names of the cases and the values are the
            above options except `ncores` and `mutaters`. If some options are
            not specified, the default values specified above will be used.
            If no cases are specified, the default case will be added with
            the default values under `envs` with the name `DEFAULT`.
        overlap (list): The sections to do overlap analysis.
    """  # noqa: E501
    input = "srtobj:file"
    output = "outdir:dir:{{in.srtobj | stem0}}.markers"
    lang = config.lang.rscript
    envs = {
        "ncores": config.misc.ncores,
        "mutaters": {},
        "ident-1": None,
        "ident-2": None,
        "group-by": "seurat_clusters",
        "each": None,
        "prefix_each": True,
        "section": "DEFAULT",
        "assay": None,
        "subset": None,
        "rest": {},
        "dbs": [
            "GO_Biological_Process_2021",
            "GO_Cellular_Component_2021",
            "GO_Molecular_Function_2021",
            "KEGG_2021_Human",
        ],
        "sigmarkers": "p_val_adj < 0.05",
        "volcano_genes": True,
        "dotplot": {},
        "cases": {},
        "overlap": [],
    }
    order = 5
    script = "file://../scripts/scrna/MarkersFinder.R"
    plugin_opts = {
        "report": "file://../reports/scrna/MarkersFinder.svelte",
        "report_paging": 8,
    }


class TopExpressingGenes(Proc):
    """Find the top expressing genes in each cluster

    Input:
        srtobj: The seurat object in RDS format

    Output:
        outdir: The output directory for the tables and plots

    Envs:
        mutaters (type=json): The mutaters to mutate the metadata
        ident: The group of cells to find the top expressing genes.
            The cells will be selected by the `group-by` column with this
            `ident` value in metadata.
            If not provided, the top expressing genes will be found for all
            groups of cells in the `group-by` column.
        group-by: The column name in metadata to group the cells.
        each: The column name in metadata to separate the cells into different
            cases.
        prefix_each (flag): Whether to prefix the `each` column name to the
            value as the case/section name.
        section: The section name for the report.
            Worked only when `each` is not specified and `ident` is specified.
            Otherwise, the section name will be constructed from `each` and
            `group-by`.
            If `DEFAULT`, and it's the only section, it not included in the
            case/section names.
        dbs (list): The dbs to do enrichment analysis for significant
            markers See below for all libraries.
            <https://maayanlab.cloud/Enrichr/#libraries>
        n (type=int): The number of top expressing genes to find.
        cases (type=json): If you have multiple cases, you can specify them
            here. The keys are the names of the cases and the values are the
            above options except `mutaters`. If some options are
            not specified, the default values specified above will be used.
            If no cases are specified, the default case will be added with
            the default values under `envs` with the name `DEFAULT`.
    """
    input = "srtobj:file"
    output = "outdir:dir:{{in.srtobj | stem}}.top_expressing_genes"
    lang = config.lang.rscript
    script = "file://../scripts/scrna/TopExpressingGenes.R"
    envs = {
        "mutaters": {},
        "ident": None,
        "group-by": "seurat_clusters",
        "each": None,
        "prefix_each": True,
        "section": "DEFAULT",
        "dbs": [
            "GO_Biological_Process_2021",
            "GO_Cellular_Component_2021",
            "GO_Molecular_Function_2021",
            "KEGG_2021_Human",
        ],
        "n": 250,
        "cases": {},
    }
    plugin_opts = {
        "report": "file://../reports/scrna/TopExpressingGenes.svelte",
        "report_paging": 8,
    }


class ExprImpution(Proc):
    """This process imputes the dropout values in scRNA-seq data.

    It takes the Seurat object as input and outputs the Seurat object with
    imputed expression data.

    Reference:
    - [Linderman, George C., Jun Zhao, and Yuval Kluger. "Zero-preserving imputation of scRNA-seq data using low-rank approximation." BioRxiv (2018): 397588.](https://www.nature.com/articles/s41467-021-27729-z)
    - [Li, Wei Vivian, and Jingyi Jessica Li. "An accurate and robust imputation method scImpute for single-cell RNA-seq data." Nature communications 9.1 (2018): 997.](https://www.nature.com/articles/s41467-018-03405-7)
    - [Dijk, David van, et al. "MAGIC: A diffusion-based imputation method reveals gene-gene interactions in single-cell RNA-sequencing data." BioRxiv (2017): 111591.](https://www.cell.com/cell/abstract/S0092-8674(18)30724-4)

    Input:
        infile: The input file in RDS format of Seurat object

    Output:
        outfile: The output file in RDS format of Seurat object
            Note that with rmagic and alra, the original RNA assay will be
            renamed to `UNIMPUTED_RNA` and the imputed RNA assay will be
            renamed to `RNA`

    Envs:
        tool (choice): Either alra, scimpute or rmagic
            - alra: Use RunALRA() from Seurat
            - scimpute: Use scImpute() from scimpute
            - rmagic: Use magic() from Rmagic
        scimpute_args (ns): The arguments for scimpute
            - drop_thre (type=float): The dropout threshold
            - kcluster (type=int): Number of clusters to use
            - ncores (type=int): Number of cores to use
            - refgene: The reference gene file
        rmagic_args (ns): The arguments for rmagic
            - python: The python path where magic-impute is installed.
        alra_args (type=json): The arguments for `RunALRA()`

    Requires:
        r-scimpute:
            - if: {{proc.envs.tool == "scimpute"}}
            - check: {{proc.lang}} <(echo "library(scImpute)")
        r-rmagic:
            - if: {{proc.envs.tool == "rmagic"}}
            - check: |
                {{proc.lang}} <(\
                    echo "\
                        tryCatch(\
                            { setwd(dirname(Sys.getenv('CONDA_PREFIX'))) }, \
                            error = function(e) NULL \
                        ); \
                        library(Rmagic)\
                    "\
                )
        magic-impute:
            - if: {{proc.envs.tool == "rmagic"}}
            - check: {{proc.envs.rmagic_args.python}} -c "import magic")
        r-dplyr:
            - if: {{proc.envs.tool == "scimpute"}}
            - check: {{proc.lang}} <(echo "library(dplyr)")
        r-seurat:
            - check: {{proc.lang}} <(echo "library(Seurat)")
        r-seuratwrappers:
            - if: {{proc.envs.tool == "alra"}}
            - check: {{proc.lang}} <(echo "library(SeuratWrappers)")
    """  # noqa: E501
    input = "infile:file"
    output = "outfile:file:{{in.infile | stem}}.imputed.RDS"
    lang = config.lang.rscript
    envs = {
        "tool": "alra",
        "rmagic_args": {"python": config.exe.magic_python},
        "scimpute_args": {
            "drop_thre": 0.5,
            "kcluster": None,
            "ncores": config.misc.ncores,
            "refgene": config.ref.refgene,
        },
        "alra_args": {},
    }
    script = "file://../scripts/scrna/ExprImpution.R"


class SCImpute(Proc):
    """Impute the dropout values in scRNA-seq data.

    Deprecated. Use `ExprImpution` instead.

    Input:
        infile: The input file for imputation
            Either a SeuratObject or a matrix of count/TPM
        groupfile: The file to subset the matrix or label the cells
            Could be an output from ImmunarchFilter

    Output:
        outfile: The output matrix

    Envs:
        infmt: The input format.
            Either `seurat` or `matrix`
    """
    input = "infile:file, groupfile:file"
    output = [
        "outfile:file:{{in.infile | stem | replace: '.seurat', ''}}."
        "{{envs.outfmt}}"
    ]
    lang = config.lang.rscript
    envs = {
        "infmt": "seurat",  # or matrix
        "outfmt": "txt",  # or csv, rds
        "type": "count",  # or TPM
        "drop_thre": 0.5,
        "kcluster": None,  # or Kcluster
        "ncores": config.misc.ncores,
        "refgene": config.ref.refgene,
    }
    script = "file://../scripts/scrna/SCImpute.R"


class SeuratFilter(Proc):
    """Filtering cells from a seurat object

    Input:
        srtobj: The seurat object in RDS
        filters: The filters to apply. Could be a file or string in TOML, or
            a python dictionary, with following keys:
            - mutaters: Create new columns in the metadata
            - filter: A R expression that will pass to
              `subset(sobj, subset = ...)` to filter the cells

    Output:
        outfile: The filtered seurat object in RDS

    Envs:
        invert: Invert the selection?

    Requires:
        r-seurat:
            - check: {{proc.lang}} <(echo "library('Seurat')")
        r-dplyr:
            - check: {{proc.lang}} <(echo "library('dplyr')")
    """
    input = "srtobj:file, filters:var"
    output = "outfile:file:{{in.srtobj | stem}}.filtered.RDS"
    lang = config.lang.rscript
    envs = {"invert": False}
    script = "file://../scripts/scrna/SeuratFilter.R"


class SeuratSubset(Proc):
    """Subset a seurat object into multiple seruat objects

    Input:
        srtobj: The seurat object in RDS
        subsets: The subsettings to apply. Could be a file or string in TOML, or
            a python dictionary, with following keys:
            - <name>: Name of the case
                mutaters: Create new columns in the metadata
                subset: A R expression that will pass to
                    `subset(sobj, subset = ...)`
                groupby: The column to group by, each value will be a case
                    If groupby is given, subset will be ignored, each value
                    of the groupby column will be a case

    Output:
        outdir: The output directory with the subset seurat objects

    Envs:
        ignore_nas: Ignore NA values?

    Requires:
        r-seurat:
            - check: {{proc.lang}} <(echo "library('Seurat')")
        r-dplyr:
            - check: {{proc.lang}} <(echo "library('dplyr')")
    """
    input = "srtobj:file, subsets:var"
    output = "outdir:dir:{{in.srtobj | stem}}.subsets"
    envs = {"ignore_nas": True}
    lang = config.lang.rscript
    script = "file://../scripts/scrna/SeuratSubset.R"


class SeuratSplit(Proc):
    """Split a seurat object into multiple seruat objects

    Input:
        srtobj: The seurat object in RDS
        by: The metadata column to split by

    Output:
        outdir: The output directory with the subset seurat objects

    Envs:
        by: The metadata column to split by
            Ignored if `by` is given in the input
        recell: Rename the cell ids using the `by` column
            A string of R function taking the original cell ids and `by`
    """
    input = "srtobj:file, by:var"
    output = "outdir:dir:{{in.srtobj | stem}}.subsets"
    envs = {
        "by": None,
        "recell": None,  # "function(cellid, by) {}",
    }
    lang = config.lang.rscript
    script = "file://../scripts/scrna/SeuratSplit.R"


class Subset10X(Proc):
    """Subset 10X data, mostly used for testing

    Requires r-matrix to load matrix.mtx.gz

    Input:
        indir: The input directory

    Output:
        outdir: The output directory

    Envs:
        seed: The seed for random number generator
        nfeats: The number of features to keep.
            If <=1 then it will be the percentage of features to keep
        ncells: The number of cells to keep.
            If <=1 then it will be the percentage of cells to keep
        feats_to_keep: The features/genes to keep.
            The final features list will be `feats_to_keep` + `nfeats`
    """
    input = "indir:dir"
    output = "outdir:dir:{{in.indir | stem}}"
    envs = {
        "seed": 8525,
        "nfeats": 0.1,
        "ncells": 0.1,
        "feats_to_keep": [],
    }
    lang = config.lang.rscript
    script = "file://../scripts/scrna/Subset10X.R"


class Write10X(Proc):
    """Write a Seurat object to 10X format

    using `write10xCounts` from `DropletUtils`

    Input:
        srtobj: The seurat object in RDS

    Output:
        outdir: The output directory

    Envs:
        version: The version of 10X format
    """
    input = "srtobj:file"
    output = "outdir:dir:{{in.srtobj | stem}}"
    envs = {"version": "3"}
    lang = config.lang.rscript
    script = "file://../scripts/scrna/Write10X.R"


@format_placeholder(mutate_helpers_clonesize=MUTATE_HELPERS_CLONESIZE_INDENTED)
class ScFGSEA(Proc):
    """Gene set enrichment analysis for cells in different groups using `fgsea`

    This process allows us to do Gene Set Enrichment Analysis (GSEA) on the expression data,
    but based on variaties of grouping, including the from the meta data and the
    scTCR-seq data as well.

    The GSEA is done using the
    [fgsea](https://bioconductor.org/packages/release/bioc/html/fgsea.html) package,
    which allows to quickly and accurately calculate arbitrarily low GSEA P-values
    for a collection of gene sets.
    The fgsea package is based on the fast algorithm for preranked GSEA described in
    [Subramanian et al. 2005](https://www.pnas.org/content/102/43/15545).

    For each case, the process will generate a table with the enrichment scores for
    each gene set, and GSEA plots for the top gene sets.

    Input:
        srtobj: The seurat object in RDS format

    Output:
        outdir: The output directory for the results

    Envs:
        ncores (type=int): Number of cores for parallelization
            Passed to `nproc` of `fgseaMultilevel()`.
        mutaters (type=json): The mutaters to mutate the metadata.
            The key-value pairs will be passed the `dplyr::mutate()` to mutate the metadata.
            %(mutate_helpers_clonesize)s
        group-by: The column name in metadata to group the cells.
        ident-1: The first group of cells to compare
        ident-2: The second group of cells to compare, if not provided, the rest of the cells that are not `NA`s in `group-by` column are used for `ident-2`.
        each: The column name in metadata to separate the cells into different subsets to do the analysis.
        section: The section name for the report. Worked only when `each` is not specified. Otherwise, the section name will be constructed from `each` and its value.
            This allows different cases to be put into the same section in the report.
        gmtfile: The pathways in GMT format, with the gene names/ids in the same format as the seurat object
        method (choice): The method to do the preranking.
            - signal_to_noise: Signal to noise.
                The larger the differences of the means (scaled by the standard deviations);
                that is, the more distinct the gene expression is in each phenotype and the more the gene
                acts as a "class marker".
            - s2n: Alias of signal_to_noise.
            - abs_signal_to_noise: The absolute value of signal_to_noise.
            - abs_s2n: Alias of abs_signal_to_noise.
            - t_test: T test.
                Uses the difference of means scaled by the standard deviation and number of samples.
            - ratio_of_classes: Also referred to as fold change.
                Uses the ratio of class means to calculate fold change for natural scale data.
            - diff_of_classes: Difference of class means.
                Uses the difference of class means to calculate fold change for nature scale data
            - log2_ratio_of_classes: Log2 ratio of class means.
                Uses the log2 ratio of class means to calculate fold change for natural scale data.
                This is the recommended statistic for calculating fold change for log scale data.
        top (type=auto): Do gsea table and enrich plot for top N pathways.
            If it is < 1, will apply it to `padj`, selecting pathways with `padj` < `top`.
        eps (type=float): This parameter sets the boundary for calculating the p value.
            See <https://rdrr.io/bioc/fgsea/man/fgseaMultilevel.html>
        minsize (type=int): Minimal size of a gene set to test. All pathways below the threshold are excluded.
        maxsize (type=int): Maximal size of a gene set to test. All pathways above the threshold are excluded.
        rest (type=json;order=98): Rest arguments for [`fgsea()`](https://rdrr.io/bioc/fgsea/man/fgsea.html)
            See also <https://rdrr.io/bioc/fgsea/man/fgseaMultilevel.html>
        cases (type=json;order=99): If you have multiple cases, you can specify them here.
            The keys are the names of the cases and the values are the above options except `mutaters`.
            If some options are not specified, the default values specified above will be used.
            If no cases are specified, the default case will be added with the name `DEFAULT`.

    Requires:
        bioconductor-fgsea:
            - check: {{proc.lang}} -e "library(fgsea)"
        r-seurat:
            - check: {{proc.lang}} -e "library(seurat)"
    """  # noqa: E501
    input = "srtobj:file"
    output = "outdir:dir:{{(in.casefile or in.srtobj) | stem0}}.fgsea"
    lang = config.lang.rscript
    envs = {
        "mutaters": {},
        "ncores": config.misc.ncores,
        "group-by": None,
        "ident-1": None,
        "ident-2": None,
        "each": None,
        "section": "DEFAULT",
        "gmtfile": "",
        "method": "s2n",
        "top": 20,
        "minsize": 10,
        "maxsize": 100,
        "eps": 0,
        "rest": {},
        "cases": {},
    }
    script = "file://../scripts/scrna/ScFGSEA.R"
    plugin_opts = {
        "report": "file://../reports/scrna/ScFGSEA.svelte",
        "report_paging": 8,
    }


class CellTypeAnnotation(Proc):
    """Annotate the cell clusters. Currently, four ways are supported:

    1. Pass the cell type annotation directly
    2. Use [`ScType`](https://github.com/IanevskiAleksandr/sc-type)
    3. Use [`scCATCH`](https://github.com/ZJUFanLab/scCATCH)
    4. Use [`hitype`](https://github.com/pwwang/hitype)

    The annotated cell types will replace the original `seurat_clusters` column in the metadata,
    so that the downstream processes will use the annotated cell types.

    The old `seurat_clusters` column will be renamed to `seurat_clusters_old`.

    If you are using `ScType`, `scCATCH`, or `hitype`, a text file containing the mapping from
    the old `seurat_clusters` to the new cell types will be generated and saved to
    `cluster2celltype.tsv` under `<workdir>/<pipline_name>/CellTypeAnnotation/0/output/`.

    Examples:
        ```toml
        [CellTypeAnnotation.envs]
        tool = "direct"
        cell_types = ["CellType1", "CellType2", "-", "CellType4"]
        ```

        The cell types will be assigned as:

        ```
        0 -> CellType1
        1 -> CellType2
        2 -> 2
        3 -> CellType4
        ```

    Input:
        sobjfile: The seurat object

    Output:
        outfile: The rds file of seurat object with cell type annotated

    Envs:
        tool (choice): The tool to use for cell type annotation.
            - sctype: Use `scType` to annotate cell types.
                See <https://github.com/IanevskiAleksandr/sc-type>
            - hitype: Use `hitype` to annotate cell types.
                See <https://github.com/pwwang/hitype>
            - sccatch: Use `scCATCH` to annotate cell types.
                See <https://github.com/ZJUFanLab/scCATCH>
            - direct: Directly assign cell types
        sctype_tissue: The tissue to use for `sctype`.
            Avaiable tissues should be the first column (`tissueType`) of `sctype_db`.
            If not specified, all rows in `sctype_db` will be used.
        sctype_db: The database to use for sctype.
            Check examples at <https://github.com/IanevskiAleksandr/sc-type/blob/master/ScTypeDB_full.xlsx>
        hitype_tissue: The tissue to use for `hitype`.
            Avaiable tissues should be the first column (`tissueType`) of `hitype_db`.
            If not specified, all rows in `hitype_db` will be used.
        hitype_db: The database to use for hitype.
            Compatible with `sctype_db`.
            See also <https://pwwang.github.io/hitype/articles/prepare-gene-sets.html>
            You can also use built-in databases, including `hitypedb_short`, `hitypedb_full`, and `hitypedb_pbmc3k`.
        cell_types (list): The cell types to use for direct annotation.
            You can use `"-"` or `""` as the placeholder for the clusters that
            you want to keep the original cell types (`seurat_clusters`).
            If the length of `cell_types` is shorter than the number of
            clusters, the remaining clusters will be kept as the original cell
            types.
            You can also use `NA` to remove the clusters from downstream analysis. This
            only works when `envs.newcol` is not specified.

            /// Note
            If `tool` is `direct` and `cell_types` is not specified or an empty list,
            the original cell types will be kept and nothing will be changed.
            ///

        sccatch_args (ns): The arguments for `scCATCH::findmarkergene()` if `tool` is `sccatch`.
            - species (choice): The specie of cells.
                - Human: Human cells.
                - Mouse: Mouse cells.
            - cancer: If the sample is from cancer tissue, then the cancer type may be defined.
            - tissue: Tissue origin of cells must be defined.
            - <more>: Other arguments for [`scCATCH::findmarkergene()`](https://rdrr.io/cran/scCATCH/man/findmarkergene.html).
                You can pass an RDS file to `sccatch_args.marker` to work as custom marker. If so,
                `if_use_custom_marker` will be set to `TRUE` automatically.
        newcol: The new column name to store the cell types.
            If not specified, the `seurat_clusters` column will be overwritten.
            If specified, the original `seurat_clusters` column will be kept and `Idents` will be kept as the original `seurat_clusters`.

    Requires:
        r-HGNChelper:
            - if: {{proc.envs.tool == 'sctype'}}
            - check: {{proc.lang}} -e "library(HGNChelper)"
        r-seurat:
            - if: {{proc.envs.tool == 'sctype'}}
            - check: {{proc.lang}} -e "library(Seurat)"
        r-dplyr:
            - if: {{proc.envs.tool == 'sctype'}}
            - check: {{proc.lang}} -e "library(dplyr)"
        r-openxlsx:
            - if: {{proc.envs.tool == 'sctype'}}
            - check: {{proc.lang}} -e "library(openxlsx)"
    """  # noqa: E501
    input = "sobjfile:file"
    output = "outfile:file:{{in.sobjfile | stem}}.annotated.RDS"
    lang = config.lang.rscript
    envs = {
        "tool": "hitype",
        "sctype_tissue": None,
        "sctype_db": config.ref.sctype_db,
        "cell_types": [],
        "sccatch_args": {},
        "hitype_tissue": None,
        "hitype_db": None,
        "newcol": None,
    }
    script = "file://../scripts/scrna/CellTypeAnnotation.R"


class SeuratMap2Ref(Proc):
    """Map the seurat object to reference

    See: <https://satijalab.org/seurat/articles/integration_mapping.html>
    and <https://satijalab.org/seurat/articles/multimodal_reference_mapping.html>

    Input:
        sobjfile: The seurat object

    Output:
        outfile: The rds file of seurat object with cell type annotated

    Envs:
        use (choice): Which level of cell type to use for further analysis and
            being aliased to `alias`
            - predicted.celltype.l1: The first level of predicted cell type
            - predicted.celltype.l2: The second level of predicted cell type
        alias: The name of an aliasied column to `use`.
            This is helpful for the downstream analysis where the column name
            is used as the cluster.
        ref: The reference seurat object file.
            Either an RDS file or a h5seurat file that can be loaded by
            `Seurat::LoadH5Seurat()`.
            The file type is determined by the extension. `.rds` or `.RDS` for
            RDS file, `.h5seurat` or `.h5` for h5seurat file.
        SCTransform (ns): Arguments for [`SCTransform()`](https://satijalab.org/seurat/reference/sctransform)
            - do-correct-umi (flag): Place corrected UMI matrix in assay counts slot?
            - do-scale (flag): Whether to scale residuals to have unit variance?
            - do-center (flag): Whether to center residuals to have mean zero?
            - <more>: See <https://satijalab.org/seurat/reference/sctransform>.
                Note that the hyphen (`-`) will be transformed into `.` for the keys.
        FindTransferAnchors (ns): Arguments for [`FindTransferAnchors()`](https://satijalab.org/seurat/reference/findtransferanchors)
            - normalization-method (choice): Name of normalization method used.
                - LogNormalize: Log-normalize the data matrix
                - SCT: Scale data using the SCTransform method
            - reference-reduction: Name of dimensional reduction to use from the reference if running the pcaproject workflow.
                Optionally enables reuse of precomputed reference dimensional reduction.
            - <more>: See <https://satijalab.org/seurat/reference/findtransferanchors>.
                Note that the hyphen (`-`) will be transformed into `.` for the keys.
        MapQuery (ns): Arguments for [`MapQuery()`](https://satijalab.org/seurat/reference/mapquery)
            - reference-reduction: Name of reduction to use from the reference for neighbor finding
            - reduction-model: `DimReduc` object that contains the umap model
            - refdata (type=json): Data to transfer
            - <more>: See <https://satijalab.org/seurat/reference/mapquery>.
                Note that the hyphen (`-`) will be transformed into `.` for the keys.
        MappingScore (ns): Arguments for [`MappingScore()`](https://satijalab.org/seurat/reference/mappingscore)
            - <more>: See <https://satijalab.org/seurat/reference/mappingscore>.
                Note that the hyphen (`-`) will be transformed into `.` for the keys.

    Requires:
        r-seurat:
            - check: {{proc.lang}} -e "library(Seurat)"
    """  # noqa: E501
    input = "sobjfile:file"
    output = "outfile:file:{{in.sobjfile | stem}}.RDS"
    lang = config.lang.rscript
    envs = {
        "use": "predicted.celltype.l2",
        "alias": "seurat_clusters",
        "ref": None,
        "SCTransform": {
            "do-correct-umi": False,
            "do-scale": False,
            "do-center": True,
        },
        "FindTransferAnchors": {
            "normalization-method": "SCT",
            "reference-reduction": "spca",
        },
        "MapQuery": {
            "reference-reduction": "spca",
            "reduction-model": "wnn.umap",
            "refdata": {
                "celltype-l1": "celltype.l1",
                "celltype-l2": "celltype.l2",
                "predicted_ADT": "ADT",
            }
        },
        "MappingScore": {},
    }
    script = "file://../scripts/scrna/SeuratMap2Ref.R"
    plugin_opts = {"report": "file://../reports/scrna/SeuratMap2Ref.svelte"}


class RadarPlots(Proc):
    """Radar plots for cell proportion in different clusters.

    This process generates the radar plots for the clusters of T cells.
    It explores the proportion of cells in different groups (e.g. Tumor vs Blood)
    in different T-cell clusters.

    Examples:
        Let's say we have a metadata like this:

        | Cell | Source | Timepoint | seurat_clusters |
        | ---- | ------ | --------- | --------------- |
        | A    | Blood  | Pre       | 0               |
        | B    | Blood  | Pre       | 0               |
        | C    | Blood  | Post      | 1               |
        | D    | Blood  | Post      | 1               |
        | E    | Tumor  | Pre       | 2               |
        | F    | Tumor  | Pre       | 2               |
        | G    | Tumor  | Post      | 3               |
        | H    | Tumor  | Post      | 3               |

        With configurations:

        ```toml
        [RadarPlots.envs]
        by = "Source"
        ```

        Then we will have a radar plots like this:

        ![Radar plots](https://pwwang.github.io/immunopipe/processes/images/RadarPlots-default.png)

        We can use `each` to separate the cells into different cases:

        ```toml
        [RadarPlots.envs]
        by = "Source"
        each = "Timepoint"
        ```

        Then we will have two radar plots, one for `Pre` and one for `Post`:

        ![Radar plots](https://pwwang.github.io/immunopipe/processes/images/RadarPlots-each.png)

        Using `cluster_order` to change the order of the clusters and show only the first 3 clusters:

        ```toml
        [RadarPlots.envs]
        by = "Source"
        cluster_order = ["2", "0", "1"]
        breaks = [0, 50, 100]  # also change the breaks
        ```

        ![Radar plots cluster_order](https://pwwang.github.io/immunopipe/processes/images/RadarPlots-cluster_order.png)


        /// Attention
        All the plots used in the examples are just for demonstration purpose. The real plots will have different appearance.
        ///

    Input:
        srtobj: The seurat object in RDS format

    Output:
        outdir: The output directory for the plots

    Envs:
        mutaters (type=json): Mutaters to mutate the metadata of the
            seurat object. Keys are the column names and values are the
            expressions to mutate the columns. These new columns will be
            used to define your cases.
        by: Which column to use to separate the cells in different groups.
            `NA`s will be ignored. For example, If you have a column named `Source`
            that marks the source of the cells, and you want to separate the cells
            into `Tumor` and `Blood` groups, you can set `by` to `Source`.
            The there will be two curves in the radar plot, one for `Tumor` and
            one for `Blood`.
        each: A column with values to separate all cells in different cases
            When specified, the case will be expanded to multiple cases for
            each value in the column.
            If specified, `section` will be ignored, and the case name will
            be used as the section name.
        order (list): The order of the values in `by`. You can also limit
            (filter) the values we have in `by`. For example, if column `Source`
            has values `Tumor`, `Blood`, `Spleen`, and you only want to plot
            `Tumor` and `Blood`, you can set `order` to `["Tumor", "Blood"]`.
            This will also have `Tumor` as the first item in the legend and `Blood`
            as the second item.
        cluster_col: The column name of the cluster information.
        cluster_order (list): The order of the clusters.
            You may also use it to filter the clusters. If not given,
            all clusters will be used.
            If the cluster names are integers, use them directly for the order,
            even though a prefix `Cluster` is added on the plot.
        breaks (list;itype=int): breaks of the radar plots, from 0 to 100.
            If not given, the breaks will be calculated automatically.
        direction (choice): Direction to calculate the percentages.
            - inter-cluster: the percentage of the cells in all groups
                in each cluster (percentage adds up to 1 for each cluster).
            - intra-cluster: the percentage of the cells in all clusters.
                (percentage adds up to 1 for each group).
        section: If you want to put multiple cases into a same section
            in the report, you can set this option to the name of the section.
            Only used in the report.
        devpars (ns): The parameters for `png()`
            - res (type=int): The resolution of the plot
            - height (type=int): The height of the plot
            - width (type=int): The width of the plot
        cases (type=json): The cases for the multiple radar plots.
            Keys are the names of the cases and values are the arguments for
            the plots (`each`, `by`, `order`, `breaks`, `direction`,
            `cluster_col`, `cluster_order` and `devpars`).
            If not cases are given, a default case will be used, with the
            key `DEFAULT`.
            The keys must be valid string as part of the file name.
    """  # noqa: E501
    input = "srtobj:file"
    output = "outdir:dir:{{in.srtobj | stem}}.radar_plots"
    lang = config.lang.rscript
    script = "file://../scripts/scrna/RadarPlots.R"
    envs = {
        "mutaters": {},
        "by": None,
        "each": None,
        "order": None,
        "cluster_col": "seurat_clusters",
        "cluster_order": [],
        "breaks": [],
        "direction": "intra-cluster",
        "section": "DEFAULT",
        "devpars": {
            "res": 100,
            "width": 1200,
            "height": 1000,
        },
        "cases": {},
    }
    plugin_opts = {
        "report": "file://../reports/scrna/RadarPlots.svelte",
    }


@format_placeholder(mutate_helpers_clonesize=MUTATE_HELPERS_CLONESIZE_INDENTED)
class MetaMarkers(Proc):
    """Find markers between three or more groups of cells, using one-way ANOVA
    or Kruskal-Wallis test.

    Sometimes, you may want to find the markers for cells from more than 2 groups.
    In this case, you can use this process to find the markers for the groups and
    do enrichment analysis for the markers. Each marker is examined using either
    one-way ANOVA or Kruskal-Wallis test.
    The p values are adjusted using the specified method. The significant markers
    are then used for enrichment analysis using
    [enrichr](https://maayanlab.cloud/Enrichr/) api.

    Other than the markers and the enrichment analysis as outputs, this process also
    generates violin plots for the top 10 markers.

    Input:
        srtobj: The seurat object loaded by `SeuratPreparing`

    Output:
        outdir: The output directory for the markers

    Envs:
        ncores (type=int): Number of cores to use to parallelize for genes
        mutaters (type=json): The mutaters to mutate the metadata
            The key-value pairs will be passed the `dplyr::mutate()` to mutate the metadata.
            %(mutate_helpers_clonesize)s
        group-by: The column name in metadata to group the cells.
            If only `group-by` is specified, and `idents` are
            not specified, markers will be found for all groups in this column.
            `NA` group will be ignored.
        idents: The groups of cells to compare, values should be in the `group-by` column.
        each: The column name in metadata to separate the cells into different cases.
        prefix_each (flag): Whether to add the `each` value as prefix to the case name.
        dbs (list): The dbs to do enrichment analysis for significant
            markers See below for all libraries.
            <https://maayanlab.cloud/Enrichr/#libraries>
        subset: The subset of the cells to do the analysis.
            An expression passed to `dplyr::filter()`.
        p_adjust (choice): The method to adjust the p values, which can be used to filter the significant markers.
            See also <https://rdrr.io/r/stats/p.adjust.html>
            - holm: Holm-Bonferroni method
            - hochberg: Hochberg method
            - hommel: Hommel method
            - bonferroni: Bonferroni method
            - BH: Benjamini-Hochberg method
            - BY: Benjamini-Yekutieli method
            - fdr: FDR method of Benjamini-Hochberg
            - none: No adjustment
        sigmarkers: An expression passed to `dplyr::filter()` to filter the
            significant markers for enrichment analysis. The default is `p.value < 0.05`.
            If `method = 'anova'`, the variables that can be used for filtering are:
            `sumsq`, `meansq`, `statistic`, `p.value` and `p_adjust`.
            If `method = 'kruskal'`, the variables that can be used for filtering are:
            `statistic`, `p.value` and `p_adjust`.
        section: The section name for the report.
            Worked only when `each` is not specified.
            Otherwise, the section name will be constructed from `each` and `group-by`.
            If `DEFAULT`, and it's the only section, it not included in the case/section names.
        method (choice): The method for the test.
            - anova: One-way ANOVA
            - kruskal: Kruskal-Wallis test
        cases (type=json): If you have multiple cases, you can specify them
            here. The keys are the names of the cases and the values are the
            above options except `ncores` and `mutaters`. If some options are
            not specified, the default values specified above will be used.
            If no cases are specified, the default case will be added with
            the default values under `envs` with the name `DEFAULT`.
    """  # noqa: E501
    input = "srtobj:file"
    output = "outdir:dir:{{in.srtobj | stem}}.meta_markers"
    lang = config.lang.rscript
    script = "file://../scripts/scrna/MetaMarkers.R"
    envs = {
        "ncores": config.misc.ncores,
        "mutaters": {},
        "group-by": None,
        "idents": None,
        "each": None,
        "subset": None,
        "prefix_each": True,
        "p_adjust": "BH",
        "dbs": [
            "GO_Biological_Process_2021",
            "GO_Cellular_Component_2021",
            "GO_Molecular_Function_2021",
            "KEGG_2021_Human",
        ],
        "sigmarkers": "p_adjust < 0.05",
        "section": "DEFAULT",
        "method": "anova",
        "cases": {},
    }
    plugin_opts = {
        "report": "file://../reports/scrna/MetaMarkers.svelte",
        "report_paging": 8,
    }
