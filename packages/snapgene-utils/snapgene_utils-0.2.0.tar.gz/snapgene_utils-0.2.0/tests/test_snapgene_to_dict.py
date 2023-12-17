import json
import os

from Bio import SeqIO

from snapgene_utils import snapgene_file_to_dict

TEST_DIR = os.path.join("tests", "test_samples")
SNAPSHOT_DIR = os.path.join("tests", "snapshots")

def test_snapgene_file_to_dict(tmpdir):
    test_file = os.path.join(TEST_DIR, "AcGFP1.dna")
    snapshot_file = os.path.join(SNAPSHOT_DIR, "AcGFP1.json")
    file_dict = snapgene_file_to_dict(test_file)
    with open(snapshot_file) as f:
        snapshot = json.loads(f.read())
    assert(snapshot == file_dict)

def test_snapgene_file_to_dict_complex(tmpdir):
    test_file = os.path.join(TEST_DIR, "pGEX-6P-1.dna")
    snapshot_file = os.path.join(SNAPSHOT_DIR, "pGEX-6P-1.json")
    file_dict = snapgene_file_to_dict(test_file)
    with open(snapshot_file) as f:
        snapshot = json.loads(f.read())
    assert(snapshot == file_dict)
