# online-bidding-system


Run git clone [https://github.com/xx-sharvesh/online-bidding-system](https://github.com/xx-sharvesh/volunteer-management-system.).git in your terminal to clone the repository. 
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
Creating a Virtual Environment:

To create a virtual environment, which helps in managing dependencies for different projects, you can use the following command:

python3 -m venv venv

This command creates a virtual environment named `venv` in the current directory.
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
Installing Requirements:

After creating the virtual environment, activate it and then use `pip` to install the required dependencies consecutively:

# Activate the virtual environment
source venv/bin/activate

# Install streanlit
pip install streamlit

# Install Pandas
pip install pandas

These commands will install Flask and Pandas within the virtual environment, ensuring that your project's dependencies are isolated from other Python installations on your system.
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
To Run the Flask application
streamlit run app.py
This command starts the Flask development server, and you can access the application in your web browser at http://localhost: