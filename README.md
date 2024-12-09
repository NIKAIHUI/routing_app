# Combo App for Transportation Optimization using routing algorithms

This is a modular Streamlit-based application designed to solve transportation optimization problems. It includes two main functionalities:

1. **Dijkstra's Algorithm** - Solves the single-source shortest path problem for graphs with non-negative edge weights.
2. **Clark-Wright Savings Algorithm** - Optimizes vehicle routing based on savings.

## File Structure
```
routing_app/
├── app.py                # Entry point for the Streamlit app
├── algorithms/
│   ├── dijkstra.py       # Implementation of Dijkstra's algorithm
│   ├── clark_wright.py   # Implementation of Clark-Wright savings algorithm
├── navigation/
│   ├── dijkstra_page.py  # UI logic for Dijkstra's algorithm
│   ├── clark_wright_page.py # UI logic for Clark-Wright algorithm
├── tests/
│   ├── test_clark_wright.py  # Unit tests for Clark_wright algorithm
│   ├── test_dijkstra.py  # Unit tests for Dijkstra's algorithm
│   ├── test_pages.py  # Unit tests for redenring the pages
```

## Installation
1. Clone the repository or download the ZIP file.
2. Navigate to the project directory.

- (Optional) Install [pyenv](https://github.com/pyenv/pyenv#installation)
  - pyenv helps manage locally installed versions of python, we'll be using 3.11 for this project
  - After installing, ensure the correct version of python is installed:
    - `$ pyenv install`
  - Verify:
    ```shell
    $ python --version
    Python 3.11
    ```
   - Create a [virtual environment](https://docs.python.org/3/library/venv.html#creating-virtual-environments):
   - `python3.11 -m venv ./env`
   - Activate environment:
   - `source ./env/bin/activate`
   - You will know that this is successful if you see `(env)` at the start of your shell prompt

## How to Run
   Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   Run the application:
   ```bash
   streamlit run app.py
   ```
   Run tests
   We have pytest for running tests. Remember to activate your virtual environment first!
   ```shell
   pytest
   ```
## Dependencies
The app uses the following dependencies (see `requirements.txt`):
- Streamlit: For building the web interface.
- NumPy: For numerical computations.
- Pandas: For data processing.
- Pytest: For unit testing.

## Author's Note
I developed this simple transportation optimization app, featuring Dijkstra and Clark-Wright routing algorithms, to address the challenges I encountered during my learning journey in [SC0x Supply Chain Analytics](https://www.edx.org/learn/supply-chain-design/massachusetts-institute-of-technology-supply-chain-analytics) by MITx CTL on EdX. The manual effort required for calculations, Excel interactions, and mapping made the process cumbersome and complex. Inspired by the insights gained from completing the [MicroMaster credential](https://ctl.mit.edu/education/online-education/mitx-micromastersr-program-supply-chain-management) and exposure to the [CAVE](https://sc-design.mitcave.com/) app in the [275x Advanced Supply Chain Systems Planning and Network Design](https://ctl.mit.edu/education/online-education/advanced-supply-chain-systems-planning-and-network-design-scm-275x) course, I created this app to automate calculations easily and make these algorithms more accessible. My goal is to help others overcome similar challenges and deepen their understanding of these optimization techniques. Thank you MIT CTL!
