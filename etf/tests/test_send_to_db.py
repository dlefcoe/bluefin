import pandas as pd


# Create an in-memory SQLite database.
from sqlalchemy import create_engine
engine = create_engine('sqlite://', echo=False)


# Create a table from scratch with 3 rows.
df = pd.DataFrame({'name' : ['User 1', 'User 2', 'User 3']})

df.to_sql('users', con=engine)
engine.execute("SELECT * FROM users").fetchall()


# An sqlalchemy.engine.Connection can also be passed to con:
with engine.begin() as connection:
    df1 = pd.DataFrame({'name' : ['User 4', 'User 5']})
    df1.to_sql('users', con=connection, if_exists='append')

# create a second dataframe 
df2 = pd.DataFrame({'name' : ['User 6', 'User 7']})
df2.to_sql('users', con=engine, if_exists='append')


x = engine.execute("SELECT * FROM users").fetchall()
df3 = pd.DataFrame(x)
print(df3)


print('example data is written')


