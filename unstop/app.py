import streamlit as st
import pandas as pd

# Initialize seat layout with 80 seats, 7 per row and the last row with 3 seats
def initialize_seats():
    seat_numbers = list(range(1, 81))
    rows = [1]*7 + [2]*7 + [3]*7 + [4]*7 + [5]*7 + [6]*7 + [7]*7 + [8]*7 + [9]*7 + [10]*7 + [11]*7 + [12]*3
    seat_status = ['available'] * 80
    return pd.DataFrame({'Seat Number': seat_numbers, 'Row': rows, 'Status': seat_status})

# Load or initialize seat data
if 'seats' not in st.session_state:
    st.session_state.seats = initialize_seats()

# Check seat availability in one row
def check_seat_availability(required_seats):
    for row in range(1, 13):
        available_seats = st.session_state.seats[(st.session_state.seats['Row'] == row) & 
                                                 (st.session_state.seats['Status'] == 'available')]
        if len(available_seats) >= required_seats:
            return available_seats['Seat Number'].tolist()[:required_seats]
    
    # If seats are not available in one row, return nearby available seats
    all_available_seats = st.session_state.seats[st.session_state.seats['Status'] == 'available']
    return all_available_seats['Seat Number'].tolist()[:required_seats]

# Book the seats
def book_seats(seat_numbers):
    st.session_state.seats.loc[st.session_state.seats['Seat Number'].isin(seat_numbers), 'Status'] = 'booked'

# Display seat layout
def display_seat_layout():
    seat_layout = st.session_state.seats.copy()
    seat_layout['Color'] = seat_layout['Status'].apply(lambda x: '🟩' if x == 'available' else '🟥')
    layout = seat_layout.pivot(index='Row', columns='Seat Number', values='Color')
    st.table(layout.fillna(''))

# Streamlit Interface
st.title("Train Seat Booking System")
display_seat_layout()

# Input for required number of seats
required_seats = st.number_input('Enter number of seats to book (1-7):', min_value=1, max_value=7, step=1)

if st.button('Book Seats'):
    available_seats = check_seat_availability(required_seats)
    
    if available_seats:
        book_seats(available_seats)
        st.success(f"Seats {available_seats} have been successfully booked!")
    else:
        st.error("Not enough seats available to fulfill your request.")

display_seat_layout()
