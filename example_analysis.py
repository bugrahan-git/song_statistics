import mysql.connector
from analysis import Analysis


db = mysql.connector.connect(
    host="localhost",
    user="root",		# MySQL username
    passwd="",			# MySQL password
    database="test"		# Database name
)


# Create analysis object

an = Analysis(db)


# Analyze an artist

an.analyze_artist("mxpx")


# Analyze a genre

an.analyze_genre("pop")
