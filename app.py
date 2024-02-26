from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

# Load Excel file
excel_file = 'items.xlsx'
try:
    items_df = pd.read_excel(excel_file)
except FileNotFoundError:
    items_df = pd.DataFrame(columns=['Name', 'Base Price', 'Fixed Price'])
    items_df.to_excel(excel_file, index=False)

# Load participants from Excel file
participants_file = 'participants.xlsx'
try:
    participants_df = pd.read_excel(participants_file)
except FileNotFoundError:
    participants_df = pd.DataFrame(columns=['Name'])
    participants_df.to_excel(participants_file, index=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['itemName']
        base_price = float(request.form['basePrice'])
        fixed_price = float(request.form['fixedPrice'])

        # Update DataFrame
        items_df.loc[len(items_df)] = [name, base_price, fixed_price]
        items_df.to_excel(excel_file, index=False)  # Save to Excel file

        return redirect(url_for('index'))

    return render_template('index.html', items=items_df.values.tolist(), show_button=len(items_df) > 0)

@app.route('/start-auction', methods=['GET', 'POST'])
def start_auction():
    if request.method == 'POST':
        num_participants = int(request.form['numParticipants'])
        return redirect(url_for('display_items', num_participants=num_participants))

    return render_template('start_auction.html')

@app.route('/add-participant', methods=['POST'])
def add_participant():
    name = request.form['participantName']
    participants_df.loc[len(participants_df)] = [name]
    participants_df.to_excel(participants_file, index=False)  # Save to Excel file
    return redirect(url_for('start_auction'))

@app.route('/display-items/<int:num_participants>', methods=['GET', 'POST'])
def display_items(num_participants):
    # Retrieve items
    items = items_df.values.tolist()
    num_items = len(items)
    
    # Example participant names
    participant_names = ["Participant 1", "Participant 2", "Participant 3"]  # Replace with your actual participant names

    # Example current item ID
    current_item_id = 1

    return render_template('display_items.html', items=items, num_participants=num_participants, num_items=num_items, participant_names=participant_names, currentItemId=current_item_id)

    if request.method == 'POST':
        # Handle next button click
        # Logic to toggle to the next item
        pass

    return render_template('display_items.html', items=items, num_participants=num_participants)

if __name__ == '__main__':
    app.run(debug=True)
