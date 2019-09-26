# Wedding-Website
######    _Developed By Kelton Bassingthwaite_

A custom website to help facilitate invitations, registry, and photos for my wedding.

### Libraries Used
 
 * Flask
 * Flask-Login
 * Flask-wtf
 * Flask-PyMongo
 * Mailjet-Rest
 * PyTest
 
 Hosted on the Google Cloud Platform App Engine and uses a MongoDB database.
 

### Features

 * Custom Role-Based Views
   * Different users will see different content on the same page. For example, users with the "bridesmaid" role
     will see a different "/dress_code" page than users with the "groomsman" role.
 * E-Mail Functionality
    * Admins can send RSVP reminder E-mails as well as custom E-mails to any subset of users.
 * RSVP Form
    * Users can submit (and resubmit) their RSVP at any time.
    
   
### Notes

Python's Dataclasses made it easy to integrate with mongoDB using the `asdict` function. For example:

    user = User()
    user = asdict(user)
    del user['_id']  # MongoDB adds the _id value
    db.collection.insert_one(user)
    


