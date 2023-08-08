# Stimulus code for 'Same but Different: The Latency of a Shared Expectation Signal Interacts with Stimulus Attributes'
Hi there and thank you for visiting this directory, which contains all code necessary to replicate our experiment (DOI LINK HERE).

We have done our best to ensure that each file is sufficiently commented so that users easily navigate our scripts, however, a general overview of what each file does is as follows:
- `stimulus_gen.py` generates stimuli used during the experiment, placing them within a `stimuli` directory. This passes information contained within `perceptually_uniform_attribute_increments.xlsx` when doing so.
- `conditions_gen.py` generates trial sequences and outputs a series of `.xlsx` files read by the main paradigm script (i.e., `contextual_trajectory_paradigm.py`) during the experiment.
- `luminance_control_functions.py` was meant to serve as a file that contained functions for maintaining equiluminance throughout the paradigm, though this requires gamma correction, which we failed to employ during the published study (see Materials and Methods). This can be tested using `testing_luminance.py`.
- `port_funcs.py` contains functions for sending event triggers.
- `contextual_trajectory_paradigm.py` contains the main paradigm code, which heavily relies on PsychoPy modules.

Our recommended run order is:
1. `stimulus_gen.py`
2. `conditions_gen.py`
3. `contextual_trajectory_paradigm.py`
