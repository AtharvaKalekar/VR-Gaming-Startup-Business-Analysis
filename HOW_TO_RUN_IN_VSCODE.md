# How to Run the VR Games Notebooks in VS Code

Because your Mac runs a protected Python environment (PEP-668), it is best to use the built-in Virtual Environment (`venv`) to run Jupyter Notebooks with all required libraries.

### Method 1: Use the Setup Provided (Quickest)

1. Open one of the `.ipynb` files in this folder using VS Code.
2. In the top right corner of the notebook pane, look for the **Kernel Selection** button. It might be labeled with a Python version (e.g., `Python 3.1x.x`) or say `Select Kernel`.
3. Click that button.
4. From the dropdown, select **Select Another Kernel...**
5. Select **Jupyter Kernel**.
6. Select **VR Games (venv)**. 
*(If you do not see it, try reloading the VS Code window by pressing `Cmd+Shift+P` -> typing "Developer: Reload Window").*
7. Once selected, you can click the **Run All** button to execute the code.

---

### Method 2: Manually Recreating the Virtual Environment

If you want to install everything from scratch using the `requirements.txt` file, follow these steps in up the VS Code Terminal:

1. Open the Integrated Terminal in VS Code (`Cmd` + `\`` or go to `Terminal` > `New Terminal`).
2. Ensure you are in the project folder:
   ```bash
   cd "/Users/atharvakalekar/Desktop/bus/Business-Case-Study---NextGen-VR-Games-Pvt.-Ltd-VR-Gaming-Platform"
   ```
3. Create a fresh virtual environment named "myenv":
   ```bash
   python3 -m venv myenv
   ```
4. Activate the virtual environment:
   ```bash
   source myenv/bin/activate
   ```
   *(Your terminal prompt should now be prefixed with `(myenv)`)*
5. Install all libraries from the provided `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
6. Register the newly created environment so VS Code can see it:
   ```bash
   python -m ipykernel install --user --name=myenv --display-name="myenv"
   ```
7. Open any `.ipynb` file, click the **Kernel Selection** button in the top right, and choose **myenv**. Click **Run All**.
