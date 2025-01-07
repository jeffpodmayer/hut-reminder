# 1. Core Features

### User Authentication: Allow users to sign up and log in with their email/phone number.

### Reminder Setup: Allow users to set reminders for hut availability, specifying:

1. Specific huts or all huts.
2. Dates or date ranges.
3. Notification preferences (email, SMS, push notifications).

### Hut Availability Scraping: The backend will scrape hut availability data periodically.

### Notification System: Notify users when a hut they’ve selected becomes available.

1. Push notifications for mobile.
2. Email/SMS notifications for both mobile and web users.

### Dashboard: A page to show all of the user’s active reminders and hut availability in both the mobile and web versions.

1. Display hut name, reminder date range, notification method, and availability status.

### Stats Page: Page showing the the month by month stats for cancellations/reservations...

# 2. Architecture

## Mobile App (React Native):

### User Interface (UI): Designed for both iOS and Android.

- Login/Signup screens.
- Reminder management screens (selecting huts, dates, etc.).
- Dashboard for viewing reminders.
- Notification system that receives push notifications.

### API Communication:

- React Native will interact with the Django backend via RESTful APIs (using libraries like Axios or Fetch).
- Authentication, setting reminders, viewing reminders, etc., will all happen through API requests.

### Push Notifications:
- Firebase Cloud Messaging (FCM) for push notifications (for iOS and Android).
- The app will listen for changes and trigger notifications based on the user’s reminder preferences.
  
## Backend (Django):
### User Authentication:
- Django REST Framework (DRF) will manage user authentication via email/phone number.
- Implement JWT or token-based authentication to keep sessions secure.
  
### Database:
- A MySQL (or PostgreSQL) database will store user data, reminders, and hut availability info.
  
### Scraping and Data Management:
- Periodically scrape the website for hut availability.
- Store and manage the availability data for each hut.
  
### API Endpoints:
- Create DRF endpoints for creating reminders, viewing reminders, logging in, and viewing hut availability.

### Notification System:
- Email notifications can be triggered by Django's Celery and Celery Beat for periodic tasks.
- Twilio or another service can be used to send SMS notifications.
- Firebase will be used to send push notifications to the mobile app.
  
## External Services:
- Firebase for push notifications.
- Twilio (or an email service like SendGrid) for SMS/email notifications.


# 3. User Flow
Understanding the user's journey will help with both the web and mobile versions.

## User Journey Example:
### Sign Up / Login:
- User signs up with their email or phone number.
- React Native app calls Django backend API to register the user.
- If signing up, user will provide credentials and be authenticated via JWT or tokens.
Set Reminder:

### User selects a hut or multiple huts.
- User specifies dates or a date range for when they want to track availability.
- User selects how they want to be notified (email, SMS, or push notification).
- React Native app sends this data to the backend API to store the reminder.
  
### Dashboard:
- User accesses their dashboard to see active reminders.
- The dashboard will show each hut, reminder dates, notification method, and the current availability status.
- React Native will pull this data from the Django backend to display it.

### Notifications:
- The backend scrapes hut availability periodically (e.g., once a day).
- If a hut matches any user's criteria (availability), the backend sends a notification:
- Push notifications to mobile users (via Firebase).
- Email/SMS notifications to users who prefer those channels.
  
### User Interaction:
- If a user taps a push notification or interacts with the dashboard, they’re redirected to the relevant part of the app (e.g., hut availability, updating their reminder, etc.) and linked to the website to book the hut.


# 4. General Project Milestones

## Milestone 1: Set Up the Django Backend
- Set up Django and Django REST Framework.
- Implement user authentication with email/phone and token-based authentication.
- Create a models.py file for users, huts, and reminders.
- Build the first set of API endpoints:
- User sign-up/login.
- Create and view reminders.

## Milestone 2: Set Up React Native Mobile App
- Set up the React Native project with Expo or React Native CLI.
- Design and implement basic UI components (sign-up, login, reminder form, dashboard).
- Integrate Axios to connect to the Django backend.
- Implement basic screens and navigation.

## Milestone 3: Scraping and Notification System
- Implement periodic scraping logic in the Django backend using Celery or Cron.
- Set up push notifications using Firebase for mobile.
- Set up email/SMS notifications using Twilio or a similar service.

## Milestone 4: Final Testing and Polishing
- Test the React Native app for both iOS and Android devices.
- Ensure that the Django backend handles data and notifications correctly.
- Conduct end-to-end tests for creating reminders, receiving notifications, and managing user data.

## 5. Considerations and Challenges
- React Native Push Notifications: Setting up push notifications might take time, especially with platform-specific configurations (iOS vs Android). Firebase Cloud Messaging (FCM) simplifies this, but you still need to handle device tokens, notification permissions, and user interactions.

- Scraping Frequency: You'll need to determine how frequently to scrape the hut website (without overloading the server or violating terms of service). Celery is great for running tasks at scheduled intervals.
  
- User Data Privacy: Since you're handling user data, ensure you're complying with relevant data privacy regulations (GDPR, etc.), especially if you're collecting email/phone numbers.
