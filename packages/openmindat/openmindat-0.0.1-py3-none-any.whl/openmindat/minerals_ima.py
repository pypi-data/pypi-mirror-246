from . import mindat_api
from datetime import datetime

class MineralsIMARetriever:
    '''
    A class for querying mineral data from the Mindat API. It supports various query parameters such as mineral IDs, IMA status, fields selection, and pagination. The class enables method chaining for building complex queries and provides functionalities to save the queried data either to a specified directory or the current directory.

    Usage:
        >>> mir = MineralsIMARetriever()
        >>> mir.ima(1).fields("id,name,ima_formula").saveto("/path/to/directory")

    Press q to quit.
    '''
    def __init__(self):
        self._params = {}

    def _init_params(self):
        self._params.clear()
        self._params = {'format': 'json'}

    def expand(self, EXPAND_FIELDS):
        '''
        Expand the query to include related minerals and select specific fields to expand.

        Args:
            EXPAND_FIELDS(list[str] or str): The fields to expand. Valid options are:
                - "description"
                - "type_localities"
                - "locality"
                - "relations"
                - "minstats"
                - "~all" (expand all fields)
                - "*" (expand all fields)

        Returns:
            self: The MineralsIMARetriever object.

        Example:
            >>> mir = MineralsIMARetriever()
            >>> mir.expand(["description", "type_localities"])
            >>> mir.saveto()
        '''

        valid_options = ["description", "type_localities", "locality", "relations", "minstats", "~all", "*"]

        if isinstance(EXPAND_FIELDS, str):
            EXPAND_FIELDS = [EXPAND_FIELDS]

        invalid_options = [field for field in EXPAND_FIELDS if field not in valid_options]

        if invalid_options:
            raise ValueError(f"Invalid EXPAND_FIELDS: {', '.join(invalid_options)}\nEXPAND_FIELDS must be one or more of the following: {', '.join(valid_options)}")

        expand_fields = EXPAND_FIELDS
        self._params.update({
            'expand': expand_fields
        })

        return self
    
    def fields(self, FIELDS):
        '''
        Specify the selected fields to be retrieved for each geomaterial.
        Please check the API documentation for the list of available fields.
        https://api.mindat.org/schema/redoc/#tag/minerals_ima/operation/minerals_ima_list

        Args:
            FIELDS (str): The selected fields to be retrieved. Multiple fields should be separated by commas.

        Example Input:
            fields=id,name,ima_formula,ima_symbol,ima_year,discovery_year,ima_status,ima_notes,type_specimen_store,mindat_longid,mindat_guid,type_localities,description_short,mindat_formula,mindat_formula_note,~all,*
        Returns:
            self: The MineralsIMARetriever object.
        Example:
            >>> mir = MineralsIMARetriever()
            >>> mir.fields("id,name,ima_formula")
            >>> mir.saveto()
        '''

        self._params.update({
            'fields': FIELDS
        })

        return self
    
    def id__in(self, ID_IN_LIST):
        '''
        Set the IDs for the query.

        Args:
            ID_IN_LIST (str): The IDs to filter the query, separated by commas.

        Returns:
            self: The MineralsIMARetriever object.

        Example:
            >>> mir = MineralsIMARetriever()
            >>> mir.id__in("123,456,789")
            >>> mir.saveto()
        '''

        ids = str(ID_IN_LIST)

        self._params.update({
            'id__in': ids
        })

        return self

    def ima(self, IS_IMA):
        '''
            Include IMA-approved names only (1) / to be determined(0)

            Args:
                IS_IMA (int): The IMA status to filter the query. 1 for IMA-approved names only, 0 is not clear.

            Returns:
                self: The MineralsIMARetriever object.

            Example:
            >>> mir = MineralsIMARetriever()
            >>> mir.ima(1)
            >>> mir.saveto()
        '''

        if int(IS_IMA) not in [0, 1]:
            raise ValueError(f"Invalid IS_IMA: {IS_IMA}\nIS_IMA must be either 0 or 1.")

        ima = int(IS_IMA)
        self._params.update({
            'ima': ima
        })

        return self
    
    def omit(self, OMIT_FIELDS):
        '''
        Set the fields to omit from the query.

        Args:
            OMIT_FIELDS (str): The fields to omit, separated by commas. 
            Please check the API documentation for the list of available fields.
            https://api.mindat.org/schema/redoc/#tag/minerals_ima/operation/minerals_ima_list
        Returns:
            self: The MineralsIMARetriever object.

        Example:
            >>> mir = MineralsIMARetriever()
            >>> mir.omit("id,name")
            >>> mir.saveto()
        '''

        omit_fields = OMIT_FIELDS
        self._params.update({
            'omit': omit_fields
        })

        return self
    
    def page(self, PAGE):
        '''
        Sets the page number within the paginated result set.

        Args:
            PAGE (int): The page number.

        Returns:
            self: The MineralsIMARetriever object.
        
        Example:
            >>> mir = MineralsIMARetriever()
            >>> mir.page(2)
            >>> mir.saveto()
        '''
        self._params.update({
            'page': PAGE
        })

        return self

    def page_size(self, PAGE_SIZE):
        '''
        Sets the number of results per page.

        Args:
            PAGE_SIZE (int): The number of results per page.

        Returns:
            self: The MineralsIMARetriever object.
            
        Example:
            >>> mir = MineralsIMARetriever()
            >>> mir.page_size(50)
            >>> mir.saveto()
        '''
        self._params.update({
            'page_size': PAGE_SIZE
        })

        return self
    
    def q(self, SEARCHING_KEYWORDS):
        '''
        Sets the keywords to search for.

        Args:
            SEARCHING_KEYWORDS (str): The keywords to search for.

        Returns:
            self: The MineralsIMARetriever object.

        Example:
            >>> mir = MineralsIMARetriever()
            >>> mir.q("quartz")
            >>> mir.saveto()
        '''
        self._params.update({
            'q': SEARCHING_KEYWORDS
        })

        return self
    
    def updated_at(self, DATE_STR):
        '''	
            Sets the last updated datetime for the geomaterial query.

            Args:
                DATE_STR (str): The last updated datetime in the format %Y-%m-%d %H:%M:%S.

            Returns:
                self: The MineralsIMARetriever object.

            Raises:
                ValueError: If the provided DATE_STR is not a valid datetime string.

            Example:
                >>> retriever = GeomaterialRetriever()
                >>> retriever.updated_at('2022-01-01 12:00:00')
                >>> retriever.save()
        '''
        try:
            datetime.strptime(DATE_STR, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            raise ValueError("Invalid datetime format. Please provide the datetime in the format %Y-%m-%d %H:%M:%S.")

        self._params.update({
            'updated_at': DATE_STR
        })

        return self
    
    def saveto(self, OUTDIR=''):
        '''
            Executes the query to retrieve the geomaterials with keywords and saves the results to a specified directory.

            Args:
                OUTDIR (str): The directory path where the retrieved geomaterials will be saved. If not provided, the current directory will be used.

            Returns:
                None

            Example:
                >>> mir = MineralsIMARetriever()
                >>> mir.saveto("/path/to/directory")
        '''

        print("Retrieving geomaterials. This may take a while... ")

        params = self._params
        end_point = 'minerals_ima'
        outdir = OUTDIR

        ma = mindat_api.MindatApi()
        ma.get_mindat_list(params, end_point, outdir)

        # reset the query parameters in case the user wants to make another query
        self._init_params()
    
    def save(self):
        '''
            Executes the query to retrieve the list of geomaterials and saves the results to the current directory.

            Returns:
                None

            Example:
                >>> mir = MineralsIMARetriever()
                >>> mir.save()
        '''
        self.saveto()


if __name__ == '__main__':
    mir = MineralsIMARetriever()
    mir.ima('1').saveto()
