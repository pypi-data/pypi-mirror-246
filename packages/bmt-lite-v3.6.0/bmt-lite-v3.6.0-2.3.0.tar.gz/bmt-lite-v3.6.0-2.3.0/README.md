# Biolink model toolkit - lite!

_bmt-lite_ is a zero-dependency near-clone of a subset of [_bmt_](https://github.com/biolink/biolink-model-toolkit).
It is backed by a pre-populated cache of input/output pairs for many of the more commonly used _bmt_ methods.

_bmt_ alone occupies ~127 KB on disk, but with all of its dependencies it takes up ~36.2 MB. On the other hand, _bmt-lite-1.8.2_ is ~295 KB on disk, of which ~254 KB is the cached data. To initialize a Toolkit from _bmt_ takes ~2 seconds, while initializing a Toolkit from _bmt-lite_ takes ~2e-7 seconds. Because all of _bmt-lite_'s behavior is pre-cached, it does not require the internet at run time.

|   | bmt | bmt-lite (-1.8.2) |
|---|---|---|
| size | 127 KB | 295 KB |
| size w/ deps | 36.2 MB | 295 KB |
| init time | 2 sec | 2e-7 sec |

_* all measurements made on a typical laptop on a random Tuesday afternoon_

Note: _bmt-lite_ does not implement all of the functionality of _bmt_. Feature requests (or pull requests?!) are welcome. In addition, the existing functionality may differ slightly; for example, _bmt-lite_'s element-name/id format conversions are known to differ for some special cases.

# Installation

You must install a specific "flavor" of bmt-lite corresponding to the Biolink model version that you want.
Versions 1.7.0 - 2.2.5 are currently available.

For example,
```bash
pip install bmt-lite-1.8.2
```

# Usage

Use bmt-lite almost exactly like you would use bmt itself: https://github.com/biolink/biolink-model-toolkit#usage

# Development

### Building

```bash
pip install -rrequirements-build.txt
./build.sh
```

### Testing

```bash
pip install -rrequirements-test.txt
tox
```

### Publishing

```bash
pip install twine
twine upload dist/*
```
