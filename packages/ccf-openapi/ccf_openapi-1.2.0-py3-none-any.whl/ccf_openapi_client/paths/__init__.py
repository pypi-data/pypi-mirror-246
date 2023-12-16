# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from ccf_openapi_client.apis.path_to_api import path_to_api

import enum


class PathValues(str, enum.Enum):
    DBSTATUS = "/db-status"
    SPARQL = "/sparql"
    AGGREGATERESULTS = "/aggregate-results"
    GETSPATIALPLACEMENT = "/get-spatial-placement"
    HUBMAP_RUI_LOCATIONS_JSONLD = "/hubmap/rui_locations.jsonld"
    SENNET_RUI_LOCATIONS_JSONLD = "/sennet/rui_locations.jsonld"
    ONTOLOGYTERMOCCURENCES = "/ontology-term-occurences"
    CELLTYPETERMOCCURENCES = "/cell-type-term-occurences"
    BIOMARKERTERMOCCURENCES = "/biomarker-term-occurences"
    ONTOLOGYTREEMODEL = "/ontology-tree-model"
    CELLTYPETREEMODEL = "/cell-type-tree-model"
    BIOMARKERTREEMODEL = "/biomarker-tree-model"
    PROVIDERNAMES = "/provider-names"
    REFERENCEORGANS = "/reference-organs"
    REFERENCEORGANSCENE = "/reference-organ-scene"
    SCENE = "/scene"
    TECHNOLOGYNAMES = "/technology-names"
    TISSUEBLOCKS = "/tissue-blocks"
    GTEX_RUI_LOCATIONS_JSONLD = "/gtex/rui_locations.jsonld"
