from flaskblog import bcrypt
hashed_password = bcrypt.generate_password_hash("Nomzamoasavela@1909").decode("utf-8")

print(hashed_password)