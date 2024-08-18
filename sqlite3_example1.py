import sqlite3

conn = sqlite3.connect('emaildb.sqlite')
cursor = conn.cursor()

cursor.execute('''
               DROP TABLE IF EXISTS Counts''')

cursor.execute('''
               CREATE TABLE Counts (org TEXT, count INTEGER)''')

fname = input("Enter file name: ")
if (len(fname)<1): fname = 'mbox-short.txt'
fh = open(fname)
for line in fh:
    if not line.startswith("From: "): continue
    pieces = line.split()
    email = pieces[1]
    org = email.split('@')[1]
    cursor.execute('SELECT count FROM Counts WHERE org = ? ', (org,))
    row = cursor.fetchone()
    if row is None:
        cursor.execute('INSERT INTO Counts (org, count) VALUES (?, 1)', (org,))
    # If the organization is already in the table, increment the count
    else:
        cursor.execute('UPDATE Counts SET count = count + 1 WHERE org = ?', (org,))
    
    # Commit changes to the database
    conn.commit()

# Select the top 10 organizations by count and print them
sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'

for row in cursor.execute(sqlstr):
    print(str(row[0]), row[1])

# Close the cursor and the database connection
cursor.close()