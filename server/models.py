from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if (
            not isinstance(phone_number, str) or
            not phone_number.isdigit() or
            len(phone_number) != 10
        ):
            raise ValueError("Phone number must be exactly 10 digits")
        
    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name.strip()) == 0:
            raise ValueError("Name cannot be empty")
        
        existing_author = Author.query.filter_by(name=name).first()
        if existing_author:
            raise ValueError("Author name must be unique")
        return name
        

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Content must be at least 250 characters long")
        
    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError("Summary must be at most 250 characters long")
        
    @validates('category')
    def validate_category(self, key, category):
        allowed_categories = ['Fiction', 'Non-Fiction']
        if category not in allowed_categories:
            raise ValueError(f"Category must be one of {allowed_categories}")
        
    @validates('title')
    def validate_title(self, key, title):
        clickbait_phrases = [
            "Won't Believe", "Secret", "Top", "Guess"]
        if not any(phrase in title for phrase in clickbait_phrases):
            raise ValueError("Title must contain clickbait phrases")


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
