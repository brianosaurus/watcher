#!/usr/bin/env python3
"""Synthetic verifier experiment, not an agent run or production approval.
Usage: python3 verify_demo.py /path/to/uncle > results.json
Requires Python 3, Git, ssh-keygen. Reads pinned code from Uncle without changing it.
Creates disposable repositories and an ephemeral test key. Never publishes.
"""
import base64
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import types

REV = 'b27e23c235e01d1da42498a1a149ae406a7c6f08'
GOOD = '''def charge(ledger, request_id, amount):
    if request_id not in ledger:
        ledger[request_id] = amount
    return sum(ledger.values())
'''
BAD = '''def charge(ledger, request_id, amount):
    ledger[request_id] = ledger.get(request_id, 0) + amount
    return sum(ledger.values())
'''
WEAK_TEST = '''from payments import charge
assert charge({}, "request-1", 10) == 10
print("single-charge test: PASS")
'''
RETRY_TEST = '''from payments import charge
ledger = {}
charge(ledger, "request-1", 10)
assert charge(ledger, "request-1", 10) == 10, "retry duplicated the charge"
print("retry invariant: PASS")
'''


def run(args, cwd, env, check=True):
    return subprocess.run(args, cwd=cwd, env=env, text=True,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=check)


def main():
    upstream = Path(sys.argv[1]).resolve()
    raw = subprocess.check_output(['git', '-C', str(upstream), 'show',
                                   REV + ':scripts/uncle-verify.py'])
    results = {'uncle_commit': REV, 'verifier_sha256': hashlib.sha256(raw).hexdigest(),
               'scope': 'Synthetic single-change fixtures; the harness controls keys, trust files and claims. No agent, real approval, publication, predecessor chain or merge tested.',
               'expectation_basis': 'Implementation-derived consistency checks, not an independent correctness oracle.',
               'cases': []}
    with tempfile.TemporaryDirectory(prefix='watcher-provenance-') as temp:
        root = Path(temp)
        verifier = root / 'uncle-verify.py'
        verifier.write_bytes(raw)
        module = types.ModuleType('fixture_verifier')
        exec(compile(raw, str(verifier), 'exec'), module.__dict__)
        env = dict(os.environ, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull,
                   GIT_CONFIG_NOSYSTEM='1', PYTHONDONTWRITEBYTECODE='1',
                   GIT_AUTHOR_NAME='Fixture', GIT_AUTHOR_EMAIL='fixture@example.invalid',
                   GIT_COMMITTER_NAME='Fixture', GIT_COMMITTER_EMAIL='fixture@example.invalid')
        for name in list(env):
            if name in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE', 'GIT_CONFIG_COUNT') or name.startswith(('GIT_CONFIG_KEY_', 'GIT_CONFIG_VALUE_')):
                env.pop(name)
        key = root / 'fixture-key'
        run(['ssh-keygen', '-q', '-t', 'ed25519', '-N', '', '-f', str(key)], root, env)
        trust = root / 'allowed_signers'
        trust.write_text('fixture@example.invalid ' + key.with_suffix('.pub').read_text())
        attacker = root / 'attacker-key'
        run(['ssh-keygen', '-q', '-t', 'ed25519', '-N', '', '-f', str(attacker)], root, env)
        scenarios = [('baseline', 0), ('source-after-review', 1), ('missing-approval', 1),
                     ('unavailable-verification', 1), ('unattended-approval', 3),
                     ('failed-outcomes-procedure', 0), ('semantic-regression', 0),
                     ('unsigned', 3), ('tampered-payload', 1),
                     ('replaced-repo-trust', 0), ('replaced-repo-trust-external-root', 1),
                     ('different-repository-label', 0), ('different-subject-tree', 1),
                     ('excluded-workflow-document', 0), ('excluded-state', 0)]
        for name, expected in scenarios:
            repo = root / name
            repo.mkdir()
            run(['git', 'init', '-q', '-b', 'main'], repo, env)
            (repo / 'payments.py').write_text(BAD if name == 'semantic-regression' else GOOD)
            (repo / 'test_single.py').write_text(WEAK_TEST)
            docs = repo / '.uncle/docs'
            docs.mkdir(parents=True)
            (repo / 'IMPLEMENTATION_NOTES.md').write_text('Original unreferenced workflow document.\n')
            (repo / '.uncle/config').write_text('Original unreferenced state.\n')
            (repo / '.uncle/allowed_signers').write_text(trust.read_text())
            spec = docs / 'CHANGE_SPEC.md'
            spec.write_text('Retries of a payment request must not duplicate a charge.\n')
            run(['git', 'add', '.'], repo, env)
            run(['git', '-c', 'commit.gpgsign=false', 'commit', '-qm', 'fixture source'], repo, env)
            # artifact_of uses Git in the current directory and its own temporary index.
            old_cwd = Path.cwd()
            try:
                os.chdir(repo)
                artifact = module.artifact_of('HEAD')
            finally:
                os.chdir(old_cwd)
            node = {'digest': {'gitTree': artifact}}
            envelopes = {s: {'result': 'pass'} for s in
                         ('review', 'plan', 'implementation', 'verification', 'audit')}
            envelopes['implementation']['artifact'] = node
            for stage in ('verification', 'audit'):
                envelopes[stage]['inputs'] = {'artifact': node}
            approval = {'gate': 'CHANGE_SPEC', 'required': True,
                        'digest': hashlib.sha256(spec.read_bytes()).hexdigest(),
                        'approved_by': 'Fixture human (synthetic)', 'delegated_by': ''}
            predicate = {'schema_version': '1', 'authentication': 'ssh',
                         'envelopes': envelopes, 'approvals': [approval],
                         'release': {'artifact': node}}
            if name == 'missing-approval':
                approval['approved_by'] = ''
            if name == 'unattended-approval':
                approval.update(approved_by='', delegated_by='unattended')
            if name == 'unavailable-verification':
                envelopes['verification'].update(result='unavailable', reason='synthetic missing check')
            if name == 'failed-outcomes-procedure':
                envelopes['verification']['result'] = 'fail'
                envelopes['audit']['result'] = 'fail'
                predicate.update(procedure={'result': 'pass'},
                                 outcomes={'verdict': 'NOT_READY', 'override': True})
            statement = {'_type': module.STATEMENT_TYPE, 'predicateType': module.PREDICATE_TYPE,
                         'subject': [{'name': name, **node}], 'predicate': predicate}
            if name == 'unsigned':
                predicate['authentication'] = 'none'
            if name == 'different-repository-label':
                statement['subject'][0]['name'] = 'unrelated-owner/other-repository'
                predicate['source'] = {'repository': 'unrelated-owner/other-repository'}
            if name == 'different-subject-tree':
                statement['subject'][0] = {'name': name, 'digest': {'gitTree': '0' * 40}}
            payload = module.canonical(statement)
            att = repo / '.uncle/attestation.json'
            att.write_bytes(payload)
            pae = root / (name + '.pae')
            pae.write_bytes(module.pae(module.PAYLOAD_TYPE, payload))
            signing_key = attacker if name.startswith('replaced-repo-trust') else key
            run(['ssh-keygen', '-Y', 'sign', '-f', str(signing_key), '-n', module.SSH_NAMESPACE, str(pae)], root, env)
            sig = {'payloadType': module.PAYLOAD_TYPE,
                   'payload': base64.b64encode(payload).decode(),
                   'signatures': [{'keyid': '', 'signer': 'ssh',
                                   'sig': base64.b64encode(Path(str(pae) + '.sig').read_bytes()).decode()}]}
            if name == 'tampered-payload':
                sig['payload'] = base64.b64encode(payload + b' ').decode()
            if name != 'unsigned':
                att.with_suffix('.sig').write_text(json.dumps(sig))
            if name.startswith('replaced-repo-trust'):
                (repo / '.uncle/allowed_signers').write_text(
                    'fixture@example.invalid ' + attacker.with_suffix('.pub').read_text())
            if name == 'excluded-workflow-document':
                (repo / 'IMPLEMENTATION_NOTES.md').write_text('Changed after attestation; not referenced as evidence.\n')
            if name == 'excluded-state':
                (repo / '.uncle/config').write_text('Changed after attestation; not referenced as evidence.\n')
            if name == 'source-after-review':
                (repo / 'payments.py').write_text(BAD)
            run(['git', 'add', '.'], repo, env)
            run(['git', '-c', 'commit.gpgsign=false', 'commit', '-qm', 'fixture evidence'], repo, env)
            command = [sys.executable, str(verifier), '--tree', 'HEAD',
                       '--allowed-signers', str(trust)]
            if name == 'replaced-repo-trust':
                command = command[:-2]  # Use the repository's editable default trust root.
            result = run(command, repo, env, check=False)
            item = {'scenario': name, 'expected_exit': expected, 'actual_exit': result.returncode,
                    'command': 'python3 uncle-verify.py --tree HEAD' + ('' if name == 'replaced-repo-trust' else ' --allowed-signers /temporary/allowed_signers'),
                    'stdout': result.stdout.replace(str(root), '/temporary')}
            assert result.returncode == expected, item
            if name == 'semantic-regression':
                weak = run([sys.executable, 'test_single.py'], repo, env, check=False)
                retry = run([sys.executable, '-c', RETRY_TEST], repo, env, check=False)
                item['single_charge_test'] = {'exit': weak.returncode, 'stdout': weak.stdout}
                item['retry_test'] = {'exit': retry.returncode, 'stdout': retry.stdout}
                assert weak.returncode == 0 and retry.returncode == 1
            results['cases'].append(item)
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
