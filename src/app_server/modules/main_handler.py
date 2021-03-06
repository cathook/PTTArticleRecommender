from modules.utils import get_exception_msg


# Possible keys in the json object.
class Token(object):
    URL = 'url'
    POSITIVE = 'positive'
    NEGATIVE = 'negative'
    NEUTRAL = 'neutral'


class MainHandlerError(Exception):
    def __init__(self, *args, **kwargs):
        super(MainHandlerError, self).__init__(*args, **kwargs)


class MainHandler(object):
    '''Handler handles the query json question and return the result.

    Attributes:
        _miner: An instane of `miner.Miner`.
        _analyst: An instance of `article_analyst.ArticleAnalyst`.
        _logger: The logger.
    '''
    def __init__(self, miner, analyst, logger):
        '''Constructor.

        Args:
            miner: An instane of `miner.Miner`.
            analyst: An instance of `article_analyst.ArticleAnalyst`.
            logger: The logger.
        '''
        self._miner = miner
        self._analyst = analyst
        self._logger = logger

    def handle_json(self, json_obj):
        '''Handles the json query and returns the result.

        Args:
            json_obj: A json object.
        Returns: The return json object.
        '''
        self._logger.info('Get query.')
        url = json_obj[Token.URL]
        doc_id = self._miner.get_doc_identity_by_url(url)

        if doc_id.idid < 0:
            return {}

        rel_doc_ids = self._analyst.get_doc_rel_info(doc_id)

        f = lambda x: {Token.URL: self._miner.get_url_by_doc_identity(x)}
        filt = lambda arr: [a for a in arr if a]
        ret = {
            Token.POSITIVE: filt(f(a) for a in rel_doc_ids.pos_rel_docs),
            Token.NEGATIVE: filt(f(a) for a in rel_doc_ids.neg_rel_docs),
            Token.NEUTRAL: filt(f(a) for a in rel_doc_ids.neutral_rel_docs)
        }
        self._logger.info('Query handled.')

        return ret


class EchoMainHandler(object):
    '''Just an echo handler used to debug the client.'''
    def __init__(self, *args, **kwargs):
        pass

    def handle_json(self, json_obj):
        ret = {
            Token.POSITIVE: [json_obj],
            Token.NEGATIVE: [json_obj],
            Token.NEUTRAL: [json_obj]
        }
        return ret
