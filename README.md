## Hyperion: A Highly Effective PC and Page based Delta prefetcher

### **Brief Introduction:**

This is the repository for a highly effective delta prefetcher. We provide the prefetcher Hyperion, the simulator ChampSim and all the benchmarks used for this project.

### Tested Requirements

- Linux OS 
- Python 3.6.9
- Bash 4.4.20
- GCC 7.5.0

### Download the benchmark traces

We use four benchmark suites to evaluate Hyperion and we provide the links to download the traces.

[SPEC 2006 traces](https://dpc3.compas.cs.stonybrook.edu/champsim-traces/speccpu/)

[SPEC 2017 traces](https://dpc3.compas.cs.stonybrook.edu/champsim-traces/speccpu/)

[GAP](https://utexas.app.box.com/s/2k54kp8zvrqdfaa8cdhfquvcxwh7yn85/folder/132804668078)

[Ligra](https://github.com/CMU-SAFARI/Pythia/blob/master/scripts/artifact_traces.csv) (We use the traces provided by [Pythia](https://dl.acm.org/doi/10.1145/3466752.3480114))

### How to run this project?

##### Step 1

Use the scripts in ./scripts/single_core to evaluate single L1D prefetcher in a single core system:

```
./scripts/single_core/E1_single_core_single_prefetcher.sh
```

##### Step 2

Use the scripts in ./scripts/single_core/ to evaluate  L1D prefetcher with L2C prefetcher in a single core system:

```
./scripts/single_core/E1_single_core_multi_pref.sh
```

##### Step 3

Use the scripts in ./scripts/multi_cores/ to evaluate  single  L1D prefetcher in a 4 cores system:

```
./scripts/single_core/E1_4core_single_prefetcher.sh
```

##### Step 4

Use the scripts in ./scripts/multi_cores/ to evaluate  L1D prefetcher with L2C prefetcher in a 4 cores system:

```
./scripts/single_core/E1_4core_multi_pref.sh
```

##### Step 5

All the evaluation results will be output into a directory named outputsum. Then you can use the Python scripts in analysis_py to statistic the results for a csv file. Next, you could also use the scripts in the same directory to generate figures. 

##### Step 6

Scripts for parameter exploring are included in  ./scripts/parameter_explorations/. You can run Hyperion with different parameter for further research.

## Citation

Please cite our paper if you find the repo helpful for you:

```
@article{10.1145/3675398,
author = {Cui, Yujie and Chen, Wei and Cheng, Xu and Yi, Jiangfang},
title = {Hyperion: A Highly Effective Page and PC Based Delta Prefetcher},
year = {2024},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
issn = {1544-3566},
url = {https://doi.org/10.1145/3675398},
doi = {10.1145/3675398},
note = {Just Accepted},
journal = {ACM Trans. Archit. Code Optim.},
month = {jul},
keywords = {Hardware prefetch, L1D prefetcher, high accuracy, high coverage}
}
```

