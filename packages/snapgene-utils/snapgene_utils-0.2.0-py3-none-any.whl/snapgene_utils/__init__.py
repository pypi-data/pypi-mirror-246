"""
snapgene_utils module
usage:
    from snapgene_utils import snapgene_file_to_dict
    obj = snapgene_file_to_dict(file_path='test.dna')
"""
from .snapgene_utils import (
    snapgene_file_to_dict,
    snapgene_file_to_gbk,
    snapgene_file_to_seqrecord,
)
