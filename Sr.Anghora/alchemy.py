#!/usr/bin/env python

# Copyright 2013 AlchemyAPI
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from __future__ import print_function

import requests

try:
    from urllib.request import urlopen
    from urllib.parse import urlparse
    from urllib.parse import urlencode
except ImportError:
    from urlparse import urlparse
    from urllib2 import urlopen
    from urllib import urlencode

try:
    import json
except ImportError:
    # Older versions of Python (i.e. 2.4) require simplejson instead of json
    import simplejson as json


class APIKeyException(Exception):
    pass


class AlchemyAPIException(Exception):
    pass


class AlchemyAPI:
    # Setup the endpoints
    ENDPOINTS = {
        'sentiment': {
            'url': '/url/URLGetTextSentiment',
            'text': '/text/TextGetTextSentiment',
            'html': '/html/HTMLGetTextSentiment',
        },
        'sentiment_targeted': {
            'url': '/url/URLGetTargetedSentiment',
            'text': '/text/TextGetTargetedSentiment',
            'html': '/html/HTMLGetTargetedSentiment',
        },
        'author': {
            'url': '/url/URLGetAuthor',
            'html': '/html/HTMLGetAuthor',
        },
        'keywords': {
            'url': '/url/URLGetRankedKeywords',
            'text': '/text/TextGetRankedKeywords',
            'html': '/html/HTMLGetRankedKeywords',
        },
        'concepts': {
            'url': '/url/URLGetRankedConcepts',
            'text': '/text/TextGetRankedConcepts',
            'html': '/html/HTMLGetRankedConcepts',
        },
        'entities': {
            'url': '/url/URLGetRankedNamedEntities',
            'text': '/text/TextGetRankedNamedEntities',
            'html': '/html/HTMLGetRankedNamedEntities',
        },
        'category': {
            'url': '/url/URLGetCategory',
            'text': '/text/TextGetCategory',
            'html': '/html/HTMLGetCategory',
        },
        'relations': {
            'url': '/url/URLGetRelations',
            'text': '/text/TextGetRelations',
            'html': '/html/HTMLGetRelations',
        },
        'language': {
            'url': '/url/URLGetLanguage',
            'text': '/text/TextGetLanguage',
            'html': '/html/HTMLGetLanguage',
        },
        'text': {
            'url': '/url/URLGetText',
            'html': '/html/HTMLGetText',
        },
        'text_raw': {
            'url': '/url/URLGetRawText',
            'html': '/html/HTMLGetRawText',
        },
        'title': {
            'url': '/url/URLGetTitle',
            'html': '/html/HTMLGetTitle',
        },
        'feeds': {
            'url': '/url/URLGetFeedLinks',
            'html': '/html/HTMLGetFeedLinks',
        },
        'microformats': {
            'url': '/url/URLGetMicroformatData',
            'html': '/html/HTMLGetMicroformatData',
        },
        'combined': {
            'url': '/url/URLGetCombinedData',
            'text': '/text/TextGetCombinedData',
        },
        'image': {
            'url': '/url/URLGetImage'
        },
        'imagetagging': {
            'url': '/url/URLGetRankedImageKeywords',
            'image': '/image/ImageGetRankedImageKeywords',
        },
        'facetagging': {
            'url': '/url/URLGetRankedImageFaceTags',
            'image': '/image/ImageGetRankedImageFaceTags',
        },
        'taxonomy': {
            'url': '/url/URLGetRankedTaxonomy',
            'html': '/html/HTMLGetRankedTaxonomy',
            'text': '/text/TextGetRankedTaxonomy',
        }
    }

    # The base URL for all endpoints
    BASE_URL = 'http://access.alchemyapi.com/calls'

    s = requests.Session()

    def __init__(self, api_key=None):
        """
        Initializes the SDK so it can send requests to AlchemyAPI for analysis.
        If the api_key is not supplied, is is loaded from api_key.txt.
        """
        if not api_key:
            raise APIKeyException('No apikey key found')
        elif len(api_key) != 40:
            raise APIKeyException(
                'It appears that the api key is invalid. It should be exactly '
                '40 characters in length')
        self.api_key = api_key

    def entities(self, flavor, data, options=None):
        """
        Extracts the entities for text, a URL or HTML.
        For an overview, please refer to:
                http://www.alchemyapi.com/products/features/entity-extraction/
        For the docs, please refer to:
                http://www.alchemyapi.com/api/entity-extraction/

        Args:
            flavor (str): which version of the call, i.e. text, url or html.
            data (str): the data to analyze, either the text, the url
                        or html code.
            options (dict): various parameters that can be used to adjust
                            how the API works, see below for more info on
                            the available options.

            Available Options:
                disambiguate: disambiguate entities (i.e. Apple the company
                              vs. apple the fruit).
                              0: disabled, 1: enabled (default)
                linkedData: include linked data on disambiguated entities.
                            0: disabled, 1: enabled (default)
                coreference: resolve coreferences (i.e. the pronouns that
                             correspond to named entities).
                             0: disabled, 1: enabled (default)
                quotations: extract quotations by entities.
                            0: disabled (default), 1: enabled.
                sentiment: analyze sentiment for each entity.
                           0: disabled (default), 1: enabled.
                           Requires 1 additional API transaction if enabled.
                showSourceText: 0 - disabled (default), 1 - enabled
                maxRetrieve: the maximum number of entities to
                             retrieve (default: 50)

        Returns
            The response, already converted from JSON to a Python object.

        Raises:
            ValueError: If received flavor is not in allowed flavors list

        """
        options = options or {}
        # Make sure this request supports this flavor
        if flavor not in AlchemyAPI.ENDPOINTS['entities'].keys():
            raise ValueError({'status': 'ERROR',
                              'statusInfo': 'entity extraction for %s not '
                                            'available' % flavor})

        # add the data to the options and analyze
        options[flavor] = data
        return self._analyze(AlchemyAPI.ENDPOINTS['entities'][flavor], {},
                             options or {})

    def keywords(self, flavor, data, options=None):
        """
        Extracts the keywords from text, a URL or HTML.
        For an overview, please refer to:
                http://www.alchemyapi.com/products/features/keyword-extraction/
        For the docs, please refer to:
                http://www.alchemyapi.com/api/keyword-extraction/

        Args:
            flavor (str): which version of the call, i.e. text, url or html.
            data (str): the data to analyze, either the text, the url
                        or html code.
            options (dict): various parameters that can be used to adjust
                            how the API works, see below for more info on
                            the available options.

        Available Options:
        keywordExtractMode -> normal (default), strict
        sentiment -> analyze sentiment for each keyword.
                     0: disabled (default), 1: enabled.
                     Requires 1 additional API transaction if enabled.
        showSourceText -> 0: disabled (default), 1: enabled.
        maxRetrieve -> the max number of keywords returned (default: 50)

        OUTPUT:
        The response, already converted from JSON to a Python object.
        """
        options = options or {}
        # Make sure this request supports this flavor
        if flavor not in AlchemyAPI.ENDPOINTS['keywords']:
            raise ValueError({'status': 'ERROR',
                              'statusInfo': 'keyword extraction for %s not '
                                            'available' % flavor})

        # add the data to the options and analyze
        options[flavor] = data
        return self._analyze(AlchemyAPI.ENDPOINTS['keywords'][flavor], {},
                             options)

    def concepts(self, flavor, data, options=None):
        """
        Tags the concepts for text, a URL or HTML.
        For an overview, please refer to:
                http://www.alchemyapi.com/products/features/concept-tagging/
        For the docs, please refer to:
                http://www.alchemyapi.com/api/concept-tagging/

        Args:
            flavor (str): which version of the call, i.e. text, url or html.
            data (str): the data to analyze, either the text, the url
                        or html code.
            options (dict): various parameters that can be used to adjust
                            how the API works, see below for more info on
                            the available options.

        Available Options:
        maxRetrieve -> the maximum number of concepts to retrieve (default: 8)
        linkedData -> include linked data, 0: disabled, 1: enabled (default)
        showSourceText -> 0:disabled (default), 1: enabled

        OUTPUT:
        The response, already converted from JSON to a Python object.
        """
        options = options or {}
        # Make sure this request supports this flavor
        if flavor not in AlchemyAPI.ENDPOINTS['concepts']:
            raise ValueError({'status': 'ERROR',
                              'statusInfo': 'concept tagging for %s not '
                                            'available' % flavor})

        # add the data to the options and analyze
        options[flavor] = data
        return self._analyze(AlchemyAPI.ENDPOINTS['concepts'][flavor], {},
                             options)

    def sentiment(self, flavor, data, options=None):
        """
        Calculates the sentiment for text, a URL or HTML.
        For an overview, please refer to:
                http://www.alchemyapi.com/products/features/sentiment-analysis/
        For the docs, please refer to:
                http://www.alchemyapi.com/api/sentiment-analysis/

        Args:
            flavor (str): which version of the call, i.e. text, url or html.
            data (str): the data to analyze, either the text, the url
                        or html code.
            options (dict): various parameters that can be used to adjust
                            how the API works, see below for more info on
                            the available options.

        Available Options:
        showSourceText -> 0: disabled (default), 1: enabled

        OUTPUT:
        The response, already converted from JSON to a Python object.
        """
        options = options or {}
        # Make sure this request supports this flavor
        if flavor not in AlchemyAPI.ENDPOINTS['sentiment']:
            raise ValueError({'status': 'ERROR',
                              'statusInfo': 'sentiment analysis for %s not '
                                            'available' % flavor})

        # add the data to the options and analyze
        options[flavor] = data
        return self._analyze(AlchemyAPI.ENDPOINTS['sentiment'][flavor], {},
                             options)

    def sentiment_targeted(self, flavor, data, target, options=None):
        """
        Calculates the targeted sentiment for text, a URL or HTML.
        For an overview, please refer to:
                http://www.alchemyapi.com/products/features/sentiment-analysis/
        For the docs, please refer to:
                http://www.alchemyapi.com/api/sentiment-analysis/

        Args:
            flavor (str): which version of the call, i.e. text, url or html.
            data (str): the data to analyze, either the text,
                        the url or html code.
            options (dict): various parameters that can be used to adjust
                            how the API works, see below for more info on
                            the available options.

        Available Options:
        showSourceText	-> 0: disabled, 1: enabled

        OUTPUT:
        The response, already converted from JSON to a Python object.
        """
        options = options or {}
        # Make sure the target is valid
        if target is None or target == '':
            raise ValueError({'status': 'ERROR',
                              'statusInfo': 'targeted sentiment requires '
                                            'a non-null target'})

        # Make sure this request supports this flavor
        if flavor not in AlchemyAPI.ENDPOINTS['sentiment_targeted']:
            return {'status': 'ERROR',
                    'statusInfo': 'targeted sentiment analysis for %s not '
                                  'available' % flavor}

        # add the URL encoded data and target to the options and analyze
        options[flavor] = data
        options['target'] = target
        return self._analyze(
            AlchemyAPI.ENDPOINTS['sentiment_targeted'][flavor], {}, options)

    def text(self, flavor, data, options=None):
        """
        Extracts the cleaned text (removes ads, navigation, etc.) for text,
        a URL or HTML.
        For an overview, please refer to:
                http://www.alchemyapi.com/products/features/text-extraction/
        For the docs, please refer to:
                http://www.alchemyapi.com/api/text-extraction/

        Args:
            flavor (str): which version of the call, i.e. text, url or html.
            data (str): the data to analyze, either the text,
                        the url or html code.
            options (dict): various parameters that can be used to
                            adjust how the API works, see below for more
                            info on the available options.

        Available Options:
        useMetadata -> utilize meta description data, 0: disabled,
                                                      1: enabled (default)
        extractLinks -> include links, 0: disabled (default), 1: enabled.

        OUTPUT:
        The response, already converted from JSON to a Python object.
        """
        options = options or {}
        # Make sure this request supports this flavor
        if flavor not in AlchemyAPI.ENDPOINTS['text']:
            raise ValueError({'status': 'ERROR',
                              'statusInfo': 'clean text extraction for %s not '
                                            'available' % flavor})

        # add the data to the options and analyze
        options[flavor] = data
        return self._analyze(AlchemyAPI.ENDPOINTS['text'][flavor], options)

    def text_raw(self, flavor, data, options=None):
        """
        Extracts the raw text (includes ads, navigation, etc.)
        for a URL or HTML.
        For an overview, please refer to:
                http://www.alchemyapi.com/products/features/text-extraction/
        For the docs, please refer to:
                http://www.alchemyapi.com/api/text-extraction/

        Args:
            flavor (str): which version of the call, i.e. text, url or html.
            data (str): the data to analyze, either the text, the url or
                        html code.
            options (dict): various parameters that can be used to adjust
                            how the API works, see below for more info on
                            the available options.

        Available Options:
        none

        OUTPUT:
        The response, already converted from JSON to a Python object.
        """
        options = options or {}
        # Make sure this request supports this flavor
        if flavor not in AlchemyAPI.ENDPOINTS['text_raw']:
            raise ValueError({'status': 'ERROR',
                              'statusInfo': 'raw text extraction for %s not '
                                            'available' % flavor})

        # add the data to the options and analyze
        options[flavor] = data
        return self._analyze(AlchemyAPI.ENDPOINTS['text_raw'][flavor], {},
                             options)

    def author(self, flavor, data, options=None):
        """
        Extracts the author from a URL or HTML.
        For an overview, please refer to:
                http://www.alchemyapi.com/products/features/author-extraction/
        For the docs, please refer to:
                http://www.alchemyapi.com/api/author-extraction/

        Args:
            flavor (str): which version of the call, i.e. text, url or html.
            data (str): the data to analyze, either the text, the url
                        or html code.
            options (dict): various parameters that can be used to adjust
                            how the API works, see below for more info on
                            the available options.

        Available Options:
        none

        OUTPUT:
        The response, already converted from JSON to a Python object.
        """
        options = options or {}
        # Make sure this request supports this flavor
        if flavor not in AlchemyAPI.ENDPOINTS['author']:
            raise ValueError({'status': 'ERROR',
                              'statusInfo': 'author extraction for %s not '
                                            'available' % flavor})

        # add the data to the options and analyze
        options[flavor] = data
        return self._analyze(AlchemyAPI.ENDPOINTS['author'][flavor], {},
                             options)

    def language(self, flavor, data, options=None):
        """
        Detects the language for text, a URL or HTML.
        For an overview, please refer to:
                http://www.alchemyapi.com/api/language-detection/
        For the docs, please refer to:
                http://www.alchemyapi.com/products/features/language-detection/

        Args:
            flavor (str): which version of the call, i.e. text, url or html.
            data (str): the data to analyze, either the text, the url
                        or html code.
            options (dict): various parameters that can be used to adjust how
                            the API works, see below for more info on the
                            available options.

        Available Options:
        none

        OUTPUT:
        The response, already converted from JSON to a Python object.
        """
        options = options or {}
        # Make sure this request supports this flavor
        if flavor not in AlchemyAPI.ENDPOINTS['language']:
            raise ValueError({'status': 'ERROR',
                              'statusInfo': 'language detection for %s not '
                                            'available' % flavor})

        # add the data to the options and analyze
        options[flavor] = data
        return self._analyze(AlchemyAPI.ENDPOINTS['language'][flavor], {},
                             options)

    def title(self, flavor, data, options=None):
        """
        Extracts the title for a URL or HTML.
        For an overview, please refer to:
                http://www.alchemyapi.com/products/features/text-extraction/
        For the docs, please refer to:
                http://www.alchemyapi.com/api/text-extraction/

        Args:
            flavor (str): which version of the call, i.e. text, url or html.
            data (str): the data to analyze, either the text, the url
                        or html code.
            options (dict): various parameters that can be used to adjust
                            how the API works, see below for more info on
                            the available options.

        Available Options:
        useMetadata -> utilize title info embedded in meta data, 0: disabled,
                                                        1: enabled (default)

        OUTPUT:
        The response, already converted from JSON to a Python object.
        """
        options = options or {}
        # Make sure this request supports this flavor
        if flavor not in AlchemyAPI.ENDPOINTS['title']:
            raise ValueError({'status': 'ERROR',
                              'statusInfo': 'title extraction for %s not '
                                            'available' % flavor})

        # add the data to the options and analyze
        options[flavor] = data
        return self._analyze(AlchemyAPI.ENDPOINTS['title'][flavor], {},
                             options)

    def relations(self, flavor, data, options=None):
        """
        Extracts the relations for text, a URL or HTML.
        For an overview, please refer to:
            http://www.alchemyapi.com/products/features/relation-extraction/
        For the docs, please refer to:
            http://www.alchemyapi.com/api/relation-extraction/

        Args:
            flavor (str): which version of the call, i.e. text, url or html.
            data (str): the data to analyze, either the text, the url
                        or html code.
            options (dict): various parameters that can be used to adjust
                            how the API works, see below for more info on
                            the available options.

        Available Options:
        sentiment -> 0: disabled (default), 1: enabled. Requires one
                    additional API transaction if enabled.
        keywords -> extract keywords from the subject and object.
                    0: disabled (default), 1: enabled.
                    Requires one additional API transaction if enabled.
        entities -> extract entities from the subject and object.
                    0: disabled (default), 1: enabled.
                    Requires one additional API transaction if enabled.
        requireEntities -> only extract relations that have entities.
                           0: disabled (default), 1: enabled.
        sentimentExcludeEntities -> exclude full entity name in sentiment
                                    analysis. 0: disabled, 1: enabled (default)
        disambiguate -> disambiguate entities (i.e. Apple the company vs.
                        apple the fruit).
                        0: disabled, 1: enabled (default)
        linkedData -> include linked data with disambiguated entities.
                      0: disabled, 1: enabled (default).
        coreference -> resolve entity coreferences.
                       0: disabled, 1: enabled (default)
        showSourceText -> 0: disabled (default), 1: enabled.
        maxRetrieve -> the maximum number of relations to
                       extract (default: 50, max: 100)

        OUTPUT:
        The response, already converted from JSON to a Python object.
        """
        options = options or {}
        # Make sure this request supports this flavor
        if flavor not in AlchemyAPI.ENDPOINTS['relations']:
            raise ValueError({'status': 'ERROR',
                              'statusInfo': 'relation extraction for %s not '
                                            'available' % flavor})

        # add the data to the options and analyze
        options[flavor] = data
        return self._analyze(AlchemyAPI.ENDPOINTS['relations'][flavor], {},
                             options)

    def category(self, flavor, data, options=None):
        """
        Categorizes the text for text, a URL or HTML.
        For an overview, please refer to:
            http://www.alchemyapi.com/products/features/text-categorization/
        For the docs, please refer to:
            http://www.alchemyapi.com/api/text-categorization/

        Args:
            flavor (str): which version of the call, i.e. text, url or html.
            data (str): the data to analyze, either the text, the url
                        or html code.
            options (dict): various parameters that can be used to adjust
                            how the API works, see below for more info on
                            the available options.

        Available Options:
        showSourceText -> 0: disabled (default), 1: enabled

        OUTPUT:
        The response, already converted from JSON to a Python object.
        """
        options = options or {}
        # Make sure this request supports this flavor
        if flavor not in AlchemyAPI.ENDPOINTS['category']:
            raise ValueError({'status': 'ERROR',
                              'statusInfo': 'text categorization for %s not '
                                            'available' % flavor})

        # add the data to the options and analyze
        options[flavor] = data

        return self._analyze(AlchemyAPI.ENDPOINTS['category'][flavor], {},
                             options)

    def feeds(self, flavor, data, options=None):
        """
        Detects the RSS/ATOM feeds for a URL or HTML.
        For an overview, please refer to:
            http://www.alchemyapi.com/products/features/feed-detection/
        For the docs, please refer to:
            http://www.alchemyapi.com/api/feed-detection/

        INPUT:
        flavor -> which version of the call, i.e.  url or html.
        data -> the data to analyze, either the the url or html code.
        options -> various parameters that can be used to adjust
                   how the API works, see below for more info on the
                   available options.

        Available Options:
        none

        OUTPUT:
        The response, already converted from JSON to a Python object.
        """
        options = options or {}
        # Make sure this request supports this flavor
        if flavor not in AlchemyAPI.ENDPOINTS['feeds']:
            raise ValueError({'status': 'ERROR',
                              'statusInfo': 'feed detection for %s not '
                                            'available' % flavor})

        # add the data to the options and analyze
        options[flavor] = data
        return self._analyze(AlchemyAPI.ENDPOINTS['feeds'][flavor], {},
                             options)

    def microformats(self, flavor, data, options=None):
        """
        Parses the microformats for a URL or HTML.
        For an overview, please refer to:
                http://www.alchemyapi.com/products/features/microformats-parsing/
        For the docs, please refer to:
                http://www.alchemyapi.com/api/microformats-parsing/

        Args:
            flavor (str): which version of the call, i.e. url or html.
            data (str): the data to analyze, either the url or html code.
            options (dict): various parameters that can be used to adjust
                            how the API works, see below for more info on
                            the available options.

        Available Options:
        none

        OUTPUT:
        The response, already converted from JSON to a Python object.
        """
        options = options or {}
        # Make sure this request supports this flavor
        if flavor not in AlchemyAPI.ENDPOINTS['microformats']:
            raise ValueError({'status': 'ERROR',
                              'statusInfo': 'microformat extraction for %s '
                                            'not available' % flavor})

        # add the data to the options and analyze
        options[flavor] = data
        return self._analyze(AlchemyAPI.ENDPOINTS['microformats'][flavor], {},
                             options)

    def image_extraction(self, flavor, data, options=None):
        """
        Extracts main image from a URL

        INPUT:
        flavor -> which version of the call (url only currently).
        data -> URL to analyze
        options -> various parameters that can be used to adjust
                   how the API works, see below for more info on the
                   available options.

        Available Options:
        extractMode ->
             trust-metadata  :  (less CPU intensive, less accurate)
             always-infer    :  (more CPU intensive, more accurate)
        OUTPUT:
        The response, already converted from JSON to a Python object.
         """
        options = options or {}
        if flavor not in AlchemyAPI.ENDPOINTS['image']:
            raise ValueError({'status': 'ERROR',
                              'statusInfo': 'image extraction for %s not '
                                            'available' % flavor})

        options[flavor] = data
        return self._analyze(AlchemyAPI.ENDPOINTS['image'][flavor], {},
                             options)

    def taxonomy(self, flavor, data, options=None):
        """
        Taxonomy classification operations.

        Args:
            flavor (str): which version of the call, i.e. url or html.
            data (str): the data to analyze, either the url or html code.
            options (dict): various parameters that can be used to adjust
                            how the API works, see below for more info on
                            the available options.


        Available Options:
        showSourceText  ->
            include the original 'source text' the taxonomy categories
            were extracted from within the API response
            Possible values:
                1 - enabled
            0 - disabled (default)

        sourceText ->
            where to obtain the text that will be processed by this API call.

            AlchemyAPI supports multiple modes of text extraction:
                web page cleaning (removes ads, navigation links, etc.),
                raw text extraction
            (processes all web page text, including ads / nav links),
            visual constraint queries, and XPath queries.

            Possible values:
                cleaned_or_raw  : cleaning enabled, fallback to raw when
                                  cleaning produces no text (default)
            cleaned   : operate on 'cleaned' web page text
                        (web page cleaning enabled)
            raw       : operate on raw web page text
                        (web page cleaning disabled)
            cquery    : operate on the results of a visual constraints query
                                Note: The 'cquery' http argument must also be
                                set to a valid visual constraints query.
            xpath     : operate on the results of an XPath query
                                Note: The 'xpath' http argument must also be
                                set to a valid XPath query.

        cquery ->
            a visual constraints query to apply to the web page.

        xpath ->
            an XPath query to apply to the web page.

        baseUrl ->
            rel-tag output base http url (must be uri-argument encoded)

        OUTPUT:
        The response, already converted from JSON to a Python object.

        """
        options = options or {}
        if flavor not in AlchemyAPI.ENDPOINTS['taxonomy']:
            raise ValueError({'status': 'ERROR',
                              'statusInfo': 'taxonomy for %s not available'
                                            % flavor})

        options[flavor] = data
        return self._analyze(AlchemyAPI.ENDPOINTS['taxonomy'][flavor], {},
                             options)

    def combined(self, flavor, data, options=None):
        """
        Combined call for page-image, entity, keyword, title,
        author, taxonomy, concept.

        Args:
            flavor (str): which version of the call, i.e. url or html.
            data (str): the data to analyze, either the url or html code.
            options (dict): various parameters that can be used to adjust
                            how the API works, see below for more info on
                            the available options.
        Available Options:
        extract ->
            Possible values: page-image, entity, keyword, title,
                             author, taxonomy, concept
            default        : entity, keyword, taxonomy, concept

        disambiguate ->
            disambiguate detected entities
            Possible values:
                1 : enabled (default)
                        0 : disabled

        linkedData ->
            include Linked Data content links with disambiguated entities
            Possible values :
                1 : enabled (default)
                        0 : disabled

        coreference ->
            resolve he/she/etc coreferences into detected entities
            Possible values:
                1 : enabled (default)
                        0 : disabled

        quotations ->
            enable quotations extraction
            Possible values:
                1 : enabled
                        0 : disabled (default)

        sentiment ->
            enable entity-level sentiment analysis
            Possible values:
                1 : enabled
                        0 : disabled (default)

        showSourceText ->
            include the original 'source text' the entities were extracted
            from within the API response
            Possible values:
                1 : enabled
                        0 : disabled (default)

        maxRetrieve ->
            maximum number of named entities to extract
            default : 50

        baseUrl ->
            rel-tag output base http url


        OUTPUT:
        The response, already converted from JSON to a Python object.
        """
        options = options or {}
        if flavor not in AlchemyAPI.ENDPOINTS['combined']:
            raise ValueError({'status': 'ERROR',
                              'statusInfo': 'combined for %s not available'
                                            % flavor})

        options[flavor] = data
        return self._analyze(AlchemyAPI.ENDPOINTS['combined'][flavor], {},
                             options)

    def image_tagging(self, flavor, data, options=None):
        """

        INPUT:
        flavor -> which version of the call only url or image.
        data -> the data to analyze, either the the url or path to image.
        options -> various parameters that can be used to adjust
                   how the API works, see below for more info on the
                   available options.
        """
        options = options or {}
        if flavor not in AlchemyAPI.ENDPOINTS['imagetagging']:
            raise ValueError({'status': 'ERROR',
                              'statusInfo': 'imagetagging for %s not '
                                            'available' % flavor})
        elif flavor == 'image':
            image = open(data, 'rb').read()
            options['imagePostMode'] = 'raw'
            return self._analyze(AlchemyAPI.ENDPOINTS['imagetagging'][flavor],
                                 options, image)

        options[flavor] = data
        return self._analyze(AlchemyAPI.ENDPOINTS['imagetagging'][flavor], {},
                             options)

    def face_tagging(self, flavor, data, options=None):
        """
        INPUT:
        flavor -> which version of the call only url or image.
        data -> the data to analyze, either the the url or path to image.
        options -> various parameters that can be used to adjust
                   how the API works, see below for more info on the
                   available options.
        """
        options = options or {}
        if flavor not in AlchemyAPI.ENDPOINTS['facetagging']:
            return {'status': 'ERROR',
                    'statusInfo': 'facetagging for %s not available' % flavor}
        elif flavor == 'image':
            image = open(data, 'rb').read()
            options['imagePostMode'] = 'raw'
            return self._analyze(AlchemyAPI.ENDPOINTS['facetagging'][flavor],
                                 options, image)

        options[flavor] = data
        return self._analyze(AlchemyAPI.ENDPOINTS['facetagging'][flavor], {},
                             options)

    def _analyze(self, endpoint, params, post_data=None):
        """
        HTTP Request wrapper that is called by the endpoint functions.
        This function is not intended to be called through
        an external interface.
        It makes the call, then converts the returned JSON
        string into a Python object.

        INPUT:
        url -> the full URI encoded url

        OUTPUT:
        The response, already converted from JSON to a Python object.
        """

        # Add the API Key and set the output mode to JSON
        params['apikey'] = self.api_key
        params['outputMode'] = 'json'

        # Insert the base url
        post_url = AlchemyAPI.BASE_URL + endpoint + '?' + urlencode(
            params)#.encode('utf-8')

        try:
            results = requests.post(url=post_url, data=post_data or {})
            res = results.json()
            if res['status'] == 'ERROR':
                raise AlchemyAPIException(results.json())
            else:
                return results.json()
        except requests.HTTPError as e:
            raise AlchemyAPIException(
                {'status': 'ERROR', 'statusInfo': 'network-error',
                 'error_description': e})
