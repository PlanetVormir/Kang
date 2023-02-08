from form_data import form_data, params_query_map
from params import RequestParams, ParamIterator


class BruteForcer:
    BASE_URL = "https://resultsarchives.nic.in/cbseresults/cbseresults"

    def __init__(self, params: RequestParams):
        self.params = params
