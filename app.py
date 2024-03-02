import streamlit as st
import pandas as pd
import os

# Function to check if the user exists in the Excel file
def check_user(username, password, df):
    user_row = df[(df['Username'] == username) & (df['Password'].str.strip() == password.strip())]
    if user_row.empty:
        return False
    else:
        return True

# Function to create a new Excel file if it doesn't exist
def create_excel():
    if not os.path.exists('credentials.xlsx'):
        df = pd.DataFrame(columns=['Username', 'Password'])
        df.to_excel('credentials.xlsx', index=False)

# Function to sign up new users
def sign_up(username, password, df):
    create_excel()  # Ensure file exists
    if df is None:
        df = pd.DataFrame(columns=['Username', 'Password'])
    new_user = pd.DataFrame({'Username': [username], 'Password': [password]})
    df = df.append(new_user, ignore_index=True)
    df.to_excel('credentials.xlsx', index=False)
    return df

# Function to load existing user credentials from Excel
def load_credentials():
    create_excel()  # Ensure file exists
    return pd.read_excel('credentials.xlsx')

# Function to store and retrieve items state
@st.cache(allow_output_mutation=True)
def get_items():
    if 'items' not in st.session_state:
        st.session_state['items'] = []
    return st.session_state['items']

# Function to store and retrieve participants state
@st.cache(allow_output_mutation=True)
def get_participants():
    if 'participants' not in st.session_state:
        st.session_state['participants'] = []
    return st.session_state['participants']

# Main function for adding items and participants
def add_items_participants():
    st.title("Add Items and Participants")

    # Add item
    st.header("Add Item")
    item_name = st.text_input("Item Name")
    base_price = st.number_input("Base Price", min_value=0)
    print(base_price)
    if st.button("Add Item"):
        items = get_items()
        items.append({"name": item_name, "base_price": base_price})
        st.success("Item added successfully!")

    # Display added items in a table
    items = get_items()
    if items:
        st.header("Items Added")
        item_data = {"Name": [item["name"] for item in items],
                     "Base Price": [item["base_price"] for item in items]}
        item_df = pd.DataFrame(item_data)
        st.table(item_df)

    # Add participant
    st.header("Add Participant")
    participant_name = st.text_input("Participant Name")
    if st.button("Add Participant"):
        participants = get_participants()
        participants.append(participant_name)
        st.success("Participant added successfully!")

    # Display participants list
    participants = get_participants()
    if participants:
        st.subheader("Participants")
        for participant in participants:
            st.write(participant)

# Main function for auction bidding
def auction_bidding():
    st.title("Auction Bidding")

    # Get items and participants
    items = get_items()
    participants = get_participants()

    # Select item for bidding
    st.header("Select Item for Bidding")
    selected_item_name = st.selectbox("Choose Item", [item["name"] for item in items])

    # Fetch selected item details
    selected_item_details = next((item for item in items if item["name"] == selected_item_name), None)
    if selected_item_details is None:
        st.error("No item selected!")
        return

    # Display selected item details
    st.subheader("Selected Item Details")
    st.write("Name:", selected_item_details["name"])
    st.write("Base Price:", selected_item_details["base_price"])

    # Initialize bidding price as the base price of the selected item
    bidding_price = st.session_state.get(selected_item_name, selected_item_details["base_price"])

    # Display initial bidding price
    st.subheader("Bidding Price")
    st.write(bidding_price)

    # Display form to input bid amount
    bid_amount = st.number_input("Bid Amount", min_value=0, value=100)
    print(bid_amount)
    # Display buttons for participants to place bids
    st.subheader("Place Bid")

    last_bidder = st.session_state.get("last_bidder")

    # Display buttons for participants to place bids
    for participant in participants:
        if st.button(f"Bid by {participant}", key=participant):
            last_bidder = participant
            st.session_state.last_bidder = last_bidder
            bidding_price += bid_amount
            st.session_state[selected_item_name] = bidding_price
            st.success(f"Bid placed by {participant} successfully!")

    # Sell item
    if st.button("Sold"):
        winning_participant = st.session_state.last_bidder
        st.success(f"Item sold to {winning_participant}!")
        # Remove sold item from the list
        items[:] = [item for item in items if item["name"] != selected_item_name]
        # Update session state to reflect the change
        st.session_state['items'] = items
        # Reset bidding price to base price of the current item
        st.session_state[selected_item_name] = selected_item_details["base_price"]

# Multi-page app
def main():
    st.title("Login/Signup App")

    # Check if the user is logged in
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if st.session_state['logged_in']:
        # Display other functions/pages
        add_items_participants()
        auction_bidding()
    else:
        # Toggle between login and signup
        option = st.radio("Choose an option:", ("Login", "Sign Up"))
        if option == "Login":
            st.subheader("Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.button("Login"):
                df = load_credentials()
                if check_user(username, password, df):
                    st.session_state['logged_in'] = True
                    st.success(f"Hi, {username}!")
                    # Display other functions/pages
                    add_items_participants()
                    auction_bidding()
                else:
                    st.error("Invalid username or password.")
        elif option == "Sign Up":
            st.subheader("Sign Up")
            new_username = st.text_input("Create Username")
            new_password = st.text_input("Create Password", type="password")
            if st.button("Sign Up"):
                df = load_credentials()
                if new_username in df['Username'].values:
                    st.error("Username already exists. Please choose a different one.")
                else:
                    df = sign_up(new_username, new_password, df)
                    st.success("You have successfully signed up! Please login.")

if __name__ == "__main__":
    main()
