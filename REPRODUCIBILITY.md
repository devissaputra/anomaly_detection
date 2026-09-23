# Reproducibility

This repository uses a single executable entry point: `python src/run_experiment.py`.

## Reproduction checklist
1. Create an isolated Python environment.
2. Install `requirements.txt`.
3. Acquire the dataset exactly as documented in `DATA.md`.
4. Run the experiment from the repository root.
5. Confirm generated artifacts under `results/` and `assets/`.
6. Record the Python/package versions if using results in an application or manuscript.

Random seeds are fixed where the underlying library supports them. Data splits and target definitions are declared in code. No metric should be copied into academic material unless it was generated from the stated dataset and configuration.
