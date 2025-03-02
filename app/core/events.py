# from sqlalchemy import event
# from sqlalchemy.orm import Session
# from app.database.models import User, Profile

# # Event listener that automatically creates a Profile when a User is added
# @event.listens_for(User, 'after_insert')
# def create_profile(mapper, connection, target):
#     # Create a profile only when a user is created
#     if not target.profile:  # Check if profile already exists
#         profile = Profile(user_id=target.id)
#         session = Session(bind=connection)
#         session.add(profile)
#         session.commit()