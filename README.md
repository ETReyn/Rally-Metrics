# Rally-Metrics

# Setup
This project uses a postgres database<br>
-Host: localhost<br>
-Port: 5432<br>
-Database: postgres<br>
-Username: myuser<br>
There is a Database Seed folder to seed the database with a few years of iteration data<br>

# Running the server
  
Use the command line to navigate to the Python folder and enter<br>
`uvicorn main:app --reload` <br>
This will run the server on localhost port 8000<br>

# Running the UI

Navigate to the my-app folder and enter<br>
`npm run start`<br>
If that doesn't work, you might have to build the project <br>
`npm run build` <br>
This will open a web page on localhost:3000
