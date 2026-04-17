# DEER-Debt-Recorder
## **Overview**

The DEER Debt Tracker is a mobile-first application designed to solve the problem of manual debt recording for small business owners. It provides a lightweight, offline-capable solution to manage customer profiles, track transaction histories, and monitor unpaid balances directly from an Android device. 
<br><br>
## **System Features**
   * **Offline Data Persistence**: Operates without internet using a local JSON-based storage system.
   * **Customer Management**: Create profiles with names, phone numbers, and addresses.
   * **Debt Recording**: Link multiple transaction entries to a single customer profile.
   * **Native Integration**: Includes a direct dialer feature to call customers from their profile.
   * **Search & Filter**: Real-time filtering to quickly find specific customer records.
<br><br>
## **Project Directory Structure**
<br><br>
The repository is organized to be modular and easy to navigate:

   `assets/`: Contains app icons and visual resources.

   `kv_files/`: Stores the Kivy design language files for the UI layout.

   `database.py`: Manages the serialization and local storage of data.

   `main.py`: The entry point of the application, handling window lifecycles.

   `models.py`: Defines the data schema for Customers and Orders.

   `screens.py`: Contains the logic for screen transitions and user interactions.

   `requirements.txt`: Lists all Python dependencies needed to run the app.

   `buildozer.spec`: Configuration file for packaging the app into an Android APK.
<br><br>         
## **Getting Started**
To get a local copy up and running, follow these steps:

**Clone the Repository:**

   git clone https://github.com/angelotine/DEER-Debt-Recorder

**Install Dependencies:**

   pip install -r `requirements.txt`

**Run the Application:**

   `python main.py`
