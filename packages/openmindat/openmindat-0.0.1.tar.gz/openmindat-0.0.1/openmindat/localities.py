from . import mindat_api
from datetime import datetime

class LocalitiesRetriever:
    """
    This module provides the LocalitiesRetriever class for querying locality data from the Mindat API. The class enables users to construct queries based on various parameters such as country, description, included/excluded elements, and more. It supports method chaining for the flexible combination of query parameters and offers functionality to save the queried data either to a specified directory or the current directory.

    Usage:
        >>> lr = LocalitiesRetriever()
        >>> lr.country("France").description("quartz").saveto("/path/to/directory")

    Attributes:
        _params (dict): A dictionary to store query parameters.

    Methods:
        country(COUNTRY_STR): Sets the country or region for the query.
        cursor(CURSOR_STR): Sets the pagination cursor for the query.
        description(DESCRIPTION_STR): Sets the description for the query.
        elements_exc(ELEMENTS_EXC): Excludes certain chemical elements from the query.
        elements_inc(ELEMENTS_INC): Includes certain chemical elements in the query.
        expand(EXPAND_FIELDS): Expands the query to include additional fields.
        fields(FIELDS): Specifies the fields to be retrieved in the query.
        id__in(ID_IN_STR): Sets specific IDs for the query.
        omit(OMIT_FIELDS): Omits certain fields from the query results.
        page_size(PAGE_SIZE): Sets the number of results per page.
        txt(TXT_STR): Sets a locality name filter for the query.
        updated_at(DATE_STR): Sets the last updated datetime for the query.
        saveto(OUTDIR): Executes the query and saves the results to the specified directory.
        save(): Executes the query and saves the results to the current directory.

    Press q to quit.
    """

    def __init__(self):
        self._params = {}
        self._init_params()

    def _init_params(self):
        self._params.clear()
        self._params = {'format': 'json'}
        self.page_size(1500)

    def country(self, COUNTRY_STR):
        '''
        Sets the country or region for the query.
        For the list of available countries/regions, please check the API documentation:
        https://api.mindat.org/schema/redoc/#tag/localities/operation/localities_list

        Args:
            COUNTRY_STR (str): The country/region name.

        Returns:
            self: The LocalitiesRetriever object.

        Example:
            >>> lr = LocalitiesRetriever()
            >>> lr.country("United States")
            >>> lr.saveto()
        '''
        self._params.update({
            'country': COUNTRY_STR
        })

        return self
    
    def cursor(self, CURSOR_STR):
        '''
        Sets the pagination cursor value for the query.

        Args:
            CURSOR_STR (str): The pagination cursor value.

        Returns:
            self: The LocalitiesRetriever object.
        '''
        self._params.update({
            'cursor': CURSOR_STR
        })

        return self

    def description(self, DESCRIPTION_STR):
        '''
        Sets the description for the query.

        Args:
            DESCRIPTION_STR (str): The description.

        Returns:
            self: The LocalitiesRetriever object.

        Example:
            >>> lr = LocalitiesRetriever()
            >>> lr.description("quartz")
            >>> lr.saveto()
        '''
        self._params.update({
            'description': DESCRIPTION_STR
        })

        return self
    
    def elements_exc(self, ELEMENTS_EXC):
        '''
        Exclude chemical elements.

        Args:
            ELEMENTS_EXC (str): Comma-separated string of chemical elements to exclude.

        Returns:
            self: The LocalitiesRetriever object.
        
        Example:
            >>> lr = LocalitiesRetriever()
            >>> lr.elements_exc("Au,Ag")
            >>> lr.save()

        '''

        elements_exc = ELEMENTS_EXC
        self._params.update({
            'elements_exc': elements_exc
        })

        return self
    
    def elements_inc(self, ELEMENTS_INC):
        '''
        Include chemical elements.

        Args:
            ELEMENTS_INC (str): Comma-separated string of chemical elements to include.

        Returns:
            self: The LocalitiesRetriever object.
        
        Example:
            >>> lr = LocalitiesRetriever()
            >>> lr.elements_inc("Fe,Cu")
            >>> lr.save()

        '''

        elements_inc = ELEMENTS_INC
        self._params.update({
            'elements_inc': elements_inc
        })

        return self

    def expand(self, EXPAND_FIELDS):
        '''
        Expand the query to include related minerals and select specific fields to expand.

        Args:
            EXPAND_FIELDS(list[str] or str): The fields to expand. Valid options are:
                - "geomaterials" 
                - "~all" 
                - "*"

        Returns:
            self: The LocalitiesRetriever object.

        Example:
            >>> lr = LocalitiesRetriever()
            >>> lr.expand(["description", "type_localities"])
            >>> lr.saveto()
        '''

        valid_options = ["geomaterials", "~all", "*"]

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
            fields=fields=id,longid,guid,txt,revtxtd,description_short,latitude,longitude,langtxt,dateadd,datemodify,elements,country,refs,coordsystem,parent,links,area,non_hierarchical,age,meteorite_type,company,company2,loc_status,loc_group,status_year,company_year,discovered_before,discovery_year,discovery_year_type,level,locsinclude,locsexclude,wikipedia,osmid,geonames,timestamp,~all,*
        Returns:
            self: The LocalitiesRetriever object.
        Example:
            >>> lr = LocalitiesRetriever()
            >>> lr.fields("id,name,ima_formula")
            >>> lr.saveto()
        '''

        self._params.update({
            'fields': FIELDS
        })

        return self
    
    def id__in(self, ID_IN_STR):
        '''
        Set the IDs for the query.

        Args:
            ID_IN_STR (str): The IDs to filter the query, separated by commas.

        Returns:
            self: The LocalitiesRetriever object.

        Example:
            >>> lr = LocalitiesRetriever()
            >>> lr.id__in("123,456,789")
            >>> lr.saveto()
        '''

        ids = str(ID_IN_STR)

        self._params.update({
            'id__in': ids
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
            self: The LocalitiesRetriever object.

        Example:
            >>> lr = LocalitiesRetriever()
            >>> lr.omit("id,longid")
            >>> lr.saveto()
        '''

        omit_fields = OMIT_FIELDS
        self._params.update({
            'omit': omit_fields
        })

        return self
    

    def page_size(self, PAGE_SIZE):
        '''
        Sets the number of results per page.

        Args:
            PAGE_SIZE (int): The number of results per page.

        Returns:
            self: The LocalitiesRetriever object.
            
        Example:
            >>> lr = LocalitiesRetriever()
            >>> lr.page_size(50)
            >>> lr.saveto()
        '''
        self._params.update({
            'page_size': PAGE_SIZE
        })

        return self
    
    def txt(self, TXT_STR):
        '''
        Sets the locality name filter.

        Args:
            TXT_STR (str): The locality name to filter by.

        Returns:
            self: The LocalitiesRetriever object.

        Example:
            >>> lr = LocalitiesRetriever()
            >>> lr.txt("example locality")
            >>> lr.saveto()
        '''
        self._params.update({
            'txt': TXT_STR
        })

        return self
    
    def updated_at(self, DATE_STR):
        '''	
            Sets the last updated datetime for the geomaterial query.

            Args:
                DATE_STR (str): The last updated datetime in the format %Y-%m-%d %H:%M:%S.

            Returns:
                self: The LocalitiesRetriever object.

            Raises:
                ValueError: If the provided DATE_STR is not a valid datetime string.

            Example:
                >>> retriever = LocalitiesRetriever()
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
                >>> lr = LocalitiesRetriever()
                >>> lr.saveto("/path/to/directory")
        '''

        print("Retrieving localities. This may take a while... ")

        params = self._params
        end_point = 'localities'
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
                >>> lr = LocalitiesRetriever()
                >>> lr.save()
        '''
        self.saveto()


if __name__ == '__main__':
    lr = LocalitiesRetriever()
    lr.country("UK").save()
