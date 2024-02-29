import streamlit as st
import pandas as pd

# Function to store and retrieve items state
@st.cache(allow_output_mutation=True)
def get_items():
    return []

# Function to store and retrieve participants state
@st.cache(allow_output_mutation=True)
def get_participants():
    return []

# Main function for adding items and participants
def add_items_participants():
    st.title("Add Items and Participants")

    # Add item
    st.header("Add Item")
    item_name = st.text_input("Item Name")
    base_price = st.number_input("Base Price", min_value=0)
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
    selected_item = st.selectbox("Choose Item", [item["name"] for item in items])

    # Display selected item details
    selected_item_details = [item for item in items if item["name"] == selected_item][0]
    st.subheader("Selected Item Details")
    st.write("Name:", selected_item_details["name"])
    st.write("Base Price:", selected_item_details["base_price"])

    # Initialize bidding price as the base price
    bidding_price = st.session_state.get("bidding_price", selected_item_details["base_price"])

    # Display initial bidding price
    st.subheader("Bidding Price")
    st.write(bidding_price)

    # Display buttons for participants to place bids
    st.subheader("Place Bid")

    # Display buttons for participants to place bids
    for participant in participants:
        if st.button(f"Bid by {participant} (+100)", key=participant):
            bidding_price += 100
            st.session_state.bidding_price = bidding_price
            st.success(f"Bid placed by {participant} successfully!")

    # Sell item
    if st.button("Sold"):
        winning_participant = st.selectbox("Select Winning Participant", participants)
        st.success(f"Item sold to {winning_participant}!")

# Multi-page app
def main():
    menu = ["Add Items and Participants", "Auction Bidding"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add Items and Participants":
        add_items_participants()
    elif choice == "Auction Bidding":
        auction_bidding()

if __name__ == "__main__":
    main()
