# Book Wishlist Web Application

## Video Demo: [URL HERE]

## Description:
This web application enables users to create and manage a personalized list of books they intend to read. Users can seamlessly add new books, review their wishlist, and mark books as read or unread. The application is developed using Flask for the backend, SQLite for the database, and JavaScript for interactive frontend elements.

## Features:
- **User Authentication:**
  - Users can register for an account with a unique username and password.
  - Secure user login functionality.

- **Book Management:**
  - Add books to the wishlist with details such as title, author, genre, series name, and ISBN.
  - View a personalized dashboard displaying the user's book wishlist.

- **Book Status Tracking:**
  - Mark books as "Read" or "Unread" directly from the dashboard.
  - Interactive links to easily update the read status of each book.

- **Account Management:**
  - Delete the user account along with all associated data.
  - Logout feature to end the user's session securely.

## How to Run:
1. Install the required dependencies (if needed): `pip install Flask Werkzeug`
2. Run the application: `python app.py`
3. Open the browser and navigate to [http://localhost:5000](http://localhost:5000)

## Usage:
1. **Register:**
   - Visit the registration page by clicking "Register here" on the login page.
   - Enter a unique username and a secure password.
   - Click "Register" to create an account.

2. **Login:**
   - Enter your registered username and password on the login page.
   - Click "Login" to access your book wishlist.

3. **Dashboard:**
   - Add new books using the form at the top of the dashboard.
   - View your book wishlist with details such as title, author, genre, series name, and ISBN.
   - Mark books as "Read" or "Unread" using the provided links.

4. **Delete Account:**
   - Navigate to the bottom of the dashboard and click "Delete Account."
   - Confirm the deletion to permanently delete your account and all associated data.

5. **Logout:**
   - Click "Log Out" at the bottom of the dashboard to end your session.

## Notes:
- The application uses a SQLite database (`database.db`) to store user and book information.
- For development purposes, the secret key is set to 'your_secret_key' in the `app.py` file. For a production environment, update this key to enhance security.
- The application runs in debug mode (`app.run(debug=True)`) for development. In a production environment, set debug to `False`.
