"""Offline tests for the opt-in Ollama adapter; never call a real model."""

import json
import unittest
from unittest.mock import Mock

from local_llm.ollama import (
    MAX_DIAGNOSTIC_CHARS, OllamaClient, OllamaConfig, OllamaError,
    checked_url,
)
from local_llm.fixtures import BENCHMARK_CASES


class FakeResponse:
    """Fake HTTP stream to exercise response parsing without network access."""

    def __init__(self, payload):
        self.raw = json.dumps(payload).encode('utf-8')

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self, limit):
        return self.raw[:limit]


class FakeOpener:
    def __init__(self, *responses):
        self.responses = list(responses)
        self.requests = []

    def open(self, request, timeout):
        self.requests.append((request, timeout))
        return FakeResponse(self.responses.pop(0))


class OllamaAdapterTests(unittest.TestCase):
    """Validate the local-only network gate and strict output boundary."""

    def make_client(self, *responses):
        config = OllamaConfig(
            enabled=True, origin='http://127.0.0.1:11434',
            model='small-demo:4b', timeout_seconds=5,
        )
        transport = FakeOpener(*responses)
        return OllamaClient(config, opener=transport), transport

    def test_disabled_by_default(self):
        config = OllamaConfig.from_env({})
        self.assertFalse(config.enabled)
        with self.assertRaisesRegex(OllamaError, 'disabled'):
            OllamaClient(config).list_models()

    def test_local_url_accepted(self):
        self.assertEqual(
            checked_url('http://localhost:11434'),
            'http://localhost:11434',
        )

    def test_public_hostname_rejected(self):
        for host in (
            'https://127.0.0.1:11434', 'http://example.com:11434',
            'http://8.8.8.8:11434', 'http://user:pass@localhost:11434',
            'http://localhost:11434/another/path',
        ):
            with self.subTest(host=host), self.assertRaises(OllamaError):
                checked_url(host)

    def test_lan_requires_exact_allowlist(self):
        with self.assertRaises(OllamaError):
            checked_url('http://192.168.1.50:11434')
        self.assertEqual(
            checked_url('http://192.168.1.50:11434', '192.168.1.50'),
            'http://192.168.1.50:11434',
        )
        with self.assertRaises(OllamaError):
            checked_url('http://192.168.1.51:11434', '192.168.1.50')

    def test_bad_configuration_rejected(self):
        for kwargs in (
            {'DCH_OLLAMA_ENABLED': 'maybe'},
            {'DCH_OLLAMA_TIMEOUT_SECONDS': '300'},
            {'DCH_OLLAMA_MODEL': 'remote:cloud'},
        ):
            with self.subTest(kwargs=kwargs), self.assertRaises(OllamaError):
                OllamaConfig.from_env(kwargs)

    def test_inventory_deduplicated_without_inference(self):
        client, transport = self.make_client({
            'models': [{'name': 'small-demo:4b'}, {'name': 'small-demo:4b'}],
        })
        self.assertEqual(client.list_models(), ['small-demo:4b'])
        self.assertEqual(len(transport.requests), 1)
        self.assertEqual(transport.requests[0][0].get_method(), 'GET')

    def test_classification_is_bounded_and_no_tools(self):
        client, transport = self.make_client(
            {'models': [{'name': 'small-demo:4b'}]},
            {'done': True, 'response': 'dependency'},
        )
        label = client.classify_diagnostic('ModuleNotFoundError: demo')
        self.assertEqual(label, 'dependency')
        req, timeout = transport.requests[-1]
        self.assertEqual(req.get_method(), 'POST')
        self.assertEqual(timeout, 5)
        sent = json.loads(req.data)
        self.assertEqual(sent['stream'], False)
        self.assertEqual(sent['options']['num_predict'], 24)
        self.assertNotIn('tools', sent)
        self.assertNotIn('messages', sent)
        self.assertNotIn('format', sent)

    def test_free_form_response_rejected(self):
        client, _ = self.make_client(
            {'models': [{'name': 'small-demo:4b'}]},
            {'done': True, 'response': 'dependency; run this shell command'},
        )
        with self.assertRaisesRegex(OllamaError, 'strict label'):
            client.classify_diagnostic('Example diagnostic')

    def test_unfinished_response_rejected(self):
        client, _ = self.make_client(
            {'models': [{'name': 'small-demo:4b'}]},
            {'done': False, 'response': 'dependency'},
        )
        with self.assertRaisesRegex(OllamaError, 'did not finish'):
            client.classify_diagnostic('Example diagnostic')

    def test_missing_local_model_rejected_without_generation(self):
        client, transport = self.make_client({'models': []})
        with self.assertRaisesRegex(OllamaError, 'not installed'):
            client.classify_diagnostic('Some error')
        self.assertEqual(len(transport.requests), 1)

    def test_input_too_large_rejected_without_network(self):
        client, transport = self.make_client()
        with self.assertRaises(OllamaError):
            client.classify_diagnostic('x' * (MAX_DIAGNOSTIC_CHARS + 1))
        self.assertEqual(transport.requests, [])

    def test_fixtures_are_six_fictional_cases(self):
        self.assertEqual(len(BENCHMARK_CASES), 6)
        self.assertTrue(all(label in {
            'configuration', 'dependency', 'test_failure', 'unknown',
        } for _, label in BENCHMARK_CASES))


if __name__ == '__main__':
    unittest.main()
