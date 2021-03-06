from datetime import datetime

from mock import patch
from nose.tools import eq_

from snippets.base.encoders import ActiveSnippetsEncoder, JSONSnippetEncoder
from snippets.base.tests import JSONSnippetFactory, SnippetFactory, TestCase


class JSONSnippetEncoderTests(TestCase):
    def test_encode_jsonsnippet(self):
        encoder = JSONSnippetEncoder()
        data = {'id': 99, 'text': 'test-text',
                'icon': 'test-icon', 'url': 'test-url',
                'countries': ['US', 'GR'], 'weight': 100}
        snippet = JSONSnippetFactory.create(**data)
        result = encoder.default(snippet)
        eq_(result.pop('target_geo'), result.get('countries')[0])
        eq_(set(result.pop('countries')), set(data.pop('countries')))
        eq_(result, data)

    def test_encode_without_country(self):
        encoder = JSONSnippetEncoder()
        data = {'id': 99, 'text': 'test-text',
                'icon': 'test-icon', 'url': 'test-url',
                'weight': 100}
        snippet = JSONSnippetFactory.build(**data)
        result = encoder.default(snippet)
        eq_(result, data)

    @patch('snippets.base.encoders.json.JSONEncoder.default')
    def test_encode_other(self, default_mock):
        encoder = JSONSnippetEncoder()
        data = {'id': 3}
        encoder.default(data)
        default_mock.assert_called_with(data)


class ActiveSnippetsEncoderTests(TestCase):
    def test_encode_jsonsnippet(self):
        encoder = ActiveSnippetsEncoder()
        now = datetime.now()
        data = {'id': 99, 'text': 'test-text', 'publish_start': now,
                'name': 'Foo bar', 'countries': ['us']}
        snippet = JSONSnippetFactory.create(**data)
        result = encoder.default(snippet)
        eq_(result, {'id': 99,
                     'name': 'Foo bar',
                     'type': 'JSON Snippet',
                     'template': 'default',
                     'publish_start': now,
                     'publish_end': None,
                     'on_release': True,
                     'on_beta': False,
                     'on_aurora': False,
                     'on_nightly': False,
                     'locales': ['en-us'],
                     'countries': ['us'],
                     'weight': 100
                     })

    def test_encode_snippet(self):
        encoder = ActiveSnippetsEncoder()
        now = datetime.now()
        data = {'id': 99, 'publish_start': now, 'name': 'Foo bar', 'countries': ['us', 'gr']}
        snippet = SnippetFactory.create(**data)
        result = encoder.default(snippet)
        eq_(result, {'id': 99,
                     'name': 'Foo bar',
                     'type': 'Desktop Snippet',
                     'template': snippet.template.name,
                     'publish_start': now,
                     'publish_end': None,
                     'on_release': True,
                     'on_beta': False,
                     'on_aurora': False,
                     'on_nightly': False,
                     'locales': ['en-us'],
                     'countries': ['gr', 'us'],
                     'weight': 100
                     })

    @patch('snippets.base.encoders.json.JSONEncoder.default')
    def test_encode_other(self, default_mock):
        encoder = ActiveSnippetsEncoder()
        data = {'id': 3}
        encoder.default(data)
        default_mock.assert_called_with(data)
