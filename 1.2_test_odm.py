from mongoengine import connect, Document, StringField, IntField

# Verbindung zur MongoDB
connect(
    db="testdb",
    host="mongodb://localhost:27017/testdb"
)

# Klasse / Modell
class Person(Document):
    name = StringField(required=True)
    age = IntField(required=True)

# Objekt erstellen
person = Person(name="Dmytro", age=19)

# In Datenbank speichern
person.save()

# Aus Datenbank lesen
found_person = Person.objects(name="Dmytro").first()

print("Verbindung erfolgreich!")
print(f"Name: {found_person.name}, Alter: {found_person.age}")