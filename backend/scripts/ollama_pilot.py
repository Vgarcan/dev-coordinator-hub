#!/usr/bin/env python3
"""Opt-in, read-only local Ollama smoke test (no agent dispatch or file edits).

The benchmark is intentionally six synthetic diagnostics and may load a model
onto your GPU. It does not pull models, contact commercial APIs or call tools.
"""

import argparse
from pathlib import Path
import sys

# Allow running from the repository root without an editable Python install.
BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_DIR))

from dotenv import load_dotenv

from local_llm.fixtures import BENCHMARK_CASES
from local_llm.ollama import OllamaClient, OllamaConfig, OllamaError


def run(argv=None):
    """Require an explicit operation; default mode never contacts Ollama."""
    parser = argparse.ArgumentParser(description=__doc__)
    choices = parser.add_mutually_exclusive_group(required=True)
    choices.add_argument('--inventory', action='store_true',
                         help='List installed Ollama model names only.')
    choices.add_argument('--benchmark', action='store_true',
                         help='Run six synthetic classification examples.')
    args = parser.parse_args(argv)

    # Local .env values never override environment variables supplied by the OS.
    load_dotenv(dotenv_path=BACKEND_DIR / '.env', override=False)
    try:
        config = OllamaConfig.from_env()
        client = OllamaClient(config)
        if not config.enabled:
            raise OllamaError('Local Ollama pilot is disabled (DCH_OLLAMA_ENABLED=0).')
        if args.inventory:
            models = client.list_models()
            print('Installed local models (no inference executed):')
            for name in models:
                print(f'  {name}')
            return 0

        # All inputs are invented and pre-reviewed, never caller-submitted logs.
        successes = 0
        for index, (diagnostic, expected) in enumerate(BENCHMARK_CASES, 1):
            try:
                actual = client.classify_diagnostic(diagnostic)
                correct = actual == expected
                successes += int(correct)
                result = 'PASS' if correct else 'MISMATCH'
                print(f'{index}/6: {result} (expected={expected}, actual={actual})')
            except OllamaError as exc:
                # Avoid printing diagnostic text or full server/transport responses.
                print(f'{index}/6: ERROR ({exc})')
        print(f'Smoke accuracy: {successes}/6. Not a reliability certification.')
        # Incomplete evidence fails closed; do not promote the local model.
        return 0 if successes == len(BENCHMARK_CASES) else 1
    except OllamaError as exc:
        print(f'Local Ollama smoke check failed: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(run())
