# SeisBench
SeisBench - The Seismology Benchmark collection

## Example dataset loading
To load the example dataset, run the following commands in a python shell in the repository root directory.
```python
import seisbench.data

# When requesting the dataset the first time, this will download the dataset.
# Afterwards it will load the cached version from ~/.seisbench/dummydataset.
# The SeisBench path can be set with the environment variable SEISBENCH_CACHE_ROOT
dummy = seisbench.data.DummyDataset()

print(len(dummy))
print(dummy.metadata)

dummy.filter(dummy["source_magnitude"] > 2)
waveforms = dummy.get_waveforms()
print(waveforms.shape)
```

## Code formatting
SeisBench currently uses the [black code formatter](https://github.com/psf/black) (subject to change).
The formatter can be installed using pre-commit hooks.
To do so, run the following commands inside the repository:
```
pip install pre-commit
pre-commit install
```
Note that the black code style can be imposed later as well,
so if you are experiencing issues with installing black, just ignore the style.