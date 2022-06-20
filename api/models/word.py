from app.applications import database, serializer

class Word(database.Model):
    time = database.Column(database.Time)
    active=database.Column(database.Boolean)
    word = database.Column(database.String(150), nullable=False)
    word_translate = database.Column(database.String(150), nullable=False)
    id = database.Column(database.Integer, primary_key=True, nullable=False, autoincrement=True)
    id_user = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)

class WordSchema(serializer.SQLAlchemyAutoSchema):
    class Meta:
            model = Word
            include_fk = True

word_schema = WordSchema()
words_schema = WordSchema(many=True)