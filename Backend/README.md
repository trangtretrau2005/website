1. Install mysql server 
2. Setup the database
- create MySQL database (website)
- update configs in .env file:
```
DATABASE_URL=mysql+mysqlconnector://<username>:<password>@<host>:<port>/<database>
```

2. Install python3 (3.9)
3. Install depedencies
```
pip install -r requirements.txt
```

4. Start the Server:
```
python app/server.py
```
