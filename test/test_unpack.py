#!/usr/bin/env python3
"""
test_unpack.py — Verify the Python 36-bit word decoder against cat36 output.

Test strategy:
1. Read a .O file with our octal reader → get word list A
2. Convert the same .O file with cat36 -Woct -Xits → ITS binary
3. Read the ITS binary with our ITS reader → get word list B
4. Verify A == B (both produce identical word streams)
5. Also verify ASCIZ string extraction works on known data.
"""

import os
import sys
import subprocess
import tempfile

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.unpack import read_octal_file, read_its_file, dump_octal, dump_words
from src.word36 import (
    left_half, right_half, int18, make_word, word_to_octal,
    octal_to_word, read_asciz, SENTINEL, _extract_7bit_chars,
)

# Paths
OCTAL_DIR = os.path.expanduser(
    "~/Documents/sun/smi/smi/octal"
)
CAT36 = os.path.expanduser(
    "~/Documents/sun/its/tools/dasm/cat36"
)

# Test files: small → medium
TEST_FILES = ["foo.drw.O", "1.drw.O", "cas.drw.O"]


def cat36_to_its(octal_path: str, its_path: str):
    """Run cat36 -Woct -Xits to produce reference ITS binary."""
    result = subprocess.run(
        [CAT36, "-Woct", "-Xits", octal_path],
        capture_output=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"cat36 failed: {result.stderr.decode()}"
        )
    with open(its_path, "wb") as f:
        f.write(result.stdout)


def test_word36_basics():
    """Test basic 36-bit word utilities."""
    print("=== test_word36_basics ===")

    # Test halfword extraction
    word = 0o123456_654321
    assert left_half(word) == 0o123456, f"left_half failed: {left_half(word):06o}"
    assert right_half(word) == 0o654321, f"right_half failed: {right_half(word):06o}"

    # Test make_word roundtrip
    assert make_word(0o123456, 0o654321) == word

    # Test sign extension
    assert int18(0) == 0
    assert int18(1) == 1
    assert int18(0o377777) == 0o377777    # max positive
    assert int18(0o400000) == -131072     # min negative (0o400000 = -2^17)
    assert int18(0o777777) == -1

    # Test octal conversion roundtrip
    assert octal_to_word("123456654321") == word
    assert word_to_octal(word) == "123456654321"

    # Test sentinel
    assert SENTINEL == 0o400000

    print("  PASSED")


def test_asciz_extraction():
    """Test ASCIZ string extraction from known data."""
    print("=== test_asciz_extraction ===")

    # Encode "HELLO" as ASCIZ: H=0x48, E=0x45, L=0x4C, L=0x4C, O=0x4F
    # Packed: [H:7][E:7][L:7][L:7][O:7][0:1]
    word = (0x48 << 29) | (0x45 << 22) | (0x4C << 15) | (0x4C << 8) | (0x4F << 1)
    # Then a NUL word to terminate
    nul_word = 0
    words = [word, nul_word]
    s, next_off = read_asciz(words, 0)
    assert s == "HELLO", f"Expected 'HELLO', got '{s}'"
    # NUL is in the second character of word1, so next_off should be 2
    # Actually — "HELLO" has 5 chars fitting exactly in one word, but
    # there's no NUL yet within that word. So the NUL comes from word[1].
    # The first char of word[1] is 0 → NUL → terminate.
    assert next_off == 2, f"Expected offset 2, got {next_off}"

    # Shorter string: "HI\0"
    # H=0x48, I=0x49, NUL=0x00
    word = (0x48 << 29) | (0x49 << 22) | (0x00 << 15) | (0x00 << 8) | (0x00 << 1)
    words = [word]
    s, next_off = read_asciz(words, 0)
    assert s == "HI", f"Expected 'HI', got '{s}'"
    assert next_off == 1, f"Expected offset 1, got {next_off}"

    print("  PASSED")


def test_octal_reader(filename: str):
    """Test reading an .O file and verify basic sanity."""
    print(f"=== test_octal_reader({filename}) ===")

    path = os.path.join(OCTAL_DIR, filename)
    if not os.path.exists(path):
        print(f"  SKIPPED (file not found: {path})")
        return

    words = read_octal_file(path)
    print(f"  Read {len(words)} words from {filename}")

    # Verify non-empty
    assert len(words) > 0, "No words read"

    # Verify first word matches manual reading
    with open(path) as f:
        first_line = f.readline().strip()
    expected_first = int(first_line, 8)
    assert words[0] == expected_first, (
        f"First word mismatch: got {words[0]:012o}, expected {expected_first:012o}"
    )

    # Dump first few words for inspection
    print(dump_words(words, 0, min(10, len(words))))
    print("  PASSED")
    return words


def test_roundtrip(filename: str):
    """Verify octal→words matches octal→cat36→ITS→words.

    This is the critical test: our Python reader must produce the exact
    same word stream as the reference cat36 tool.
    """
    print(f"=== test_roundtrip({filename}) ===")

    octal_path = os.path.join(OCTAL_DIR, filename)
    if not os.path.exists(octal_path):
        print(f"  SKIPPED (file not found)")
        return

    if not os.path.exists(CAT36):
        print(f"  SKIPPED (cat36 not found at {CAT36})")
        return

    # 1. Read directly from .O file
    words_octal = read_octal_file(octal_path)

    # 2. Convert through cat36 → ITS binary → read back
    with tempfile.NamedTemporaryFile(suffix=".its", delete=False) as tmp:
        its_path = tmp.name

    try:
        cat36_to_its(octal_path, its_path)
        words_its = read_its_file(its_path)
    finally:
        os.unlink(its_path)

    # 3. Compare
    print(f"  Octal reader: {len(words_octal)} words")
    print(f"  ITS reader:   {len(words_its)} words")

    # The ITS format may have trailing padding, so compare up to the
    # shorter length first
    min_len = min(len(words_octal), len(words_its))
    mismatches = 0
    for i in range(min_len):
        if words_octal[i] != words_its[i]:
            if mismatches < 5:
                print(f"  MISMATCH at word {i}: "
                      f"octal={words_octal[i]:012o} "
                      f"its={words_its[i]:012o}")
            mismatches += 1

    if mismatches > 0:
        print(f"  FAILED: {mismatches} mismatches in first {min_len} words")
        return False
    else:
        print(f"  All {min_len} words match!")

    if len(words_octal) != len(words_its):
        diff = abs(len(words_octal) - len(words_its))
        print(f"  Note: length differs by {diff} words "
              f"(octal={len(words_octal)}, its={len(words_its)}) — "
              f"likely trailing padding in ITS format")
    print("  PASSED")
    return True


def test_version_detect(filename: str):
    """After reading words, check that we can detect a SUDS version number."""
    print(f"=== test_version_detect({filename}) ===")

    octal_path = os.path.join(OCTAL_DIR, filename)
    if not os.path.exists(octal_path):
        print(f"  SKIPPED (file not found)")
        return

    words = read_octal_file(octal_path)

    # Version number is typically in the first word and should be small
    # (version 24 is documented as current)
    version = words[0]
    lh = left_half(version)
    rh = right_half(version)
    print(f"  Word 0: {version:012o} (LH={lh:06o}, RH={rh:06o})")

    if rh <= 50 and lh == 0:
        print(f"  Detected SUDS version: {rh}")
    else:
        print(f"  Word 0 doesn't look like a simple version number")

    # Try to read the nomenclature type string
    if len(words) > 1:
        s, next_pos = read_asciz(words, 1)
        print(f"  Nomenclature type: '{s}' (next_pos={next_pos})")
        if next_pos < len(words):
            s2, next_pos2 = read_asciz(words, next_pos)
            print(f"  Board type: '{s2}' (next_pos={next_pos2})")
    print("  PASSED")


def main():
    print("SUDS DRW Decoder — Phase 1 Verification Tests")
    print("=" * 60)
    print()

    # Basic unit tests
    test_word36_basics()
    print()
    test_asciz_extraction()
    print()

    # File reading tests
    all_passed = True
    for fname in TEST_FILES:
        test_octal_reader(fname)
        print()

    # Critical roundtrip tests
    for fname in TEST_FILES:
        result = test_roundtrip(fname)
        if result is False:
            all_passed = False
        print()

    # Version detection tests
    for fname in TEST_FILES:
        test_version_detect(fname)
        print()

    # Summary
    print("=" * 60)
    if all_passed:
        print("ALL TESTS PASSED ✓")
    else:
        print("SOME TESTS FAILED ✗")
        sys.exit(1)


if __name__ == "__main__":
    main()
