import typing_extensions

from ccf_openapi_client.paths import PathValues
from ccf_openapi_client.apis.paths.db_status import DbStatus
from ccf_openapi_client.apis.paths.sparql import Sparql
from ccf_openapi_client.apis.paths.aggregate_results import AggregateResults
from ccf_openapi_client.apis.paths.get_spatial_placement import GetSpatialPlacement
from ccf_openapi_client.apis.paths.hubmap_rui_locations_jsonld import HubmapRuiLocationsJsonld
from ccf_openapi_client.apis.paths.sennet_rui_locations_jsonld import SennetRuiLocationsJsonld
from ccf_openapi_client.apis.paths.ontology_term_occurences import OntologyTermOccurences
from ccf_openapi_client.apis.paths.cell_type_term_occurences import CellTypeTermOccurences
from ccf_openapi_client.apis.paths.biomarker_term_occurences import BiomarkerTermOccurences
from ccf_openapi_client.apis.paths.ontology_tree_model import OntologyTreeModel
from ccf_openapi_client.apis.paths.cell_type_tree_model import CellTypeTreeModel
from ccf_openapi_client.apis.paths.biomarker_tree_model import BiomarkerTreeModel
from ccf_openapi_client.apis.paths.provider_names import ProviderNames
from ccf_openapi_client.apis.paths.reference_organs import ReferenceOrgans
from ccf_openapi_client.apis.paths.reference_organ_scene import ReferenceOrganScene
from ccf_openapi_client.apis.paths.scene import Scene
from ccf_openapi_client.apis.paths.technology_names import TechnologyNames
from ccf_openapi_client.apis.paths.tissue_blocks import TissueBlocks
from ccf_openapi_client.apis.paths.gtex_rui_locations_jsonld import GtexRuiLocationsJsonld

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.DBSTATUS: DbStatus,
        PathValues.SPARQL: Sparql,
        PathValues.AGGREGATERESULTS: AggregateResults,
        PathValues.GETSPATIALPLACEMENT: GetSpatialPlacement,
        PathValues.HUBMAP_RUI_LOCATIONS_JSONLD: HubmapRuiLocationsJsonld,
        PathValues.SENNET_RUI_LOCATIONS_JSONLD: SennetRuiLocationsJsonld,
        PathValues.ONTOLOGYTERMOCCURENCES: OntologyTermOccurences,
        PathValues.CELLTYPETERMOCCURENCES: CellTypeTermOccurences,
        PathValues.BIOMARKERTERMOCCURENCES: BiomarkerTermOccurences,
        PathValues.ONTOLOGYTREEMODEL: OntologyTreeModel,
        PathValues.CELLTYPETREEMODEL: CellTypeTreeModel,
        PathValues.BIOMARKERTREEMODEL: BiomarkerTreeModel,
        PathValues.PROVIDERNAMES: ProviderNames,
        PathValues.REFERENCEORGANS: ReferenceOrgans,
        PathValues.REFERENCEORGANSCENE: ReferenceOrganScene,
        PathValues.SCENE: Scene,
        PathValues.TECHNOLOGYNAMES: TechnologyNames,
        PathValues.TISSUEBLOCKS: TissueBlocks,
        PathValues.GTEX_RUI_LOCATIONS_JSONLD: GtexRuiLocationsJsonld,
    }
)

path_to_api = PathToApi(
    {
        PathValues.DBSTATUS: DbStatus,
        PathValues.SPARQL: Sparql,
        PathValues.AGGREGATERESULTS: AggregateResults,
        PathValues.GETSPATIALPLACEMENT: GetSpatialPlacement,
        PathValues.HUBMAP_RUI_LOCATIONS_JSONLD: HubmapRuiLocationsJsonld,
        PathValues.SENNET_RUI_LOCATIONS_JSONLD: SennetRuiLocationsJsonld,
        PathValues.ONTOLOGYTERMOCCURENCES: OntologyTermOccurences,
        PathValues.CELLTYPETERMOCCURENCES: CellTypeTermOccurences,
        PathValues.BIOMARKERTERMOCCURENCES: BiomarkerTermOccurences,
        PathValues.ONTOLOGYTREEMODEL: OntologyTreeModel,
        PathValues.CELLTYPETREEMODEL: CellTypeTreeModel,
        PathValues.BIOMARKERTREEMODEL: BiomarkerTreeModel,
        PathValues.PROVIDERNAMES: ProviderNames,
        PathValues.REFERENCEORGANS: ReferenceOrgans,
        PathValues.REFERENCEORGANSCENE: ReferenceOrganScene,
        PathValues.SCENE: Scene,
        PathValues.TECHNOLOGYNAMES: TechnologyNames,
        PathValues.TISSUEBLOCKS: TissueBlocks,
        PathValues.GTEX_RUI_LOCATIONS_JSONLD: GtexRuiLocationsJsonld,
    }
)
