# Okay, tables:
The following are almost schema of how i plan to lay the database.

### - User :
> A user of the forum.
- ID: str
- username: str
- dateJoined: int (unix stamp)
- permissions: array[str] (`["post", "react", "manageMessages", "manageUsers"]`)
- quoteID: str (ID of a Content entry, will be markdown.)
- follows: array[str] (ID of other people)

##

### - Content :
> Can be the body of a reply(md), post, img, file, etc.
- ID: str
- authorID: str
- contentType: str (layed out like html, eg, `"text/html", "text/markDown", "image/png"`)
- data: binary blob
- date: int (unix stamp)
- deletionDate: int|null (unix stamp; generally null)

##

### - Thread :
>   The big T, the juicest part of the forum, content! Anyhow, this object has multiple authors that can edit it's content and many replies referencing to it. It's what we query to get the large part of our content.
> ##
>
> replies can be acquired by doing a:
> ```sql
> select * from reply where parentID = {{ thread id here }}
> ```

- ID: str
- listAuthorID: array[str] (list of authors, everyone who can modify the thread without being a admin.)
- display: int (0 = public; 1 = only authors; 2 = only by link, do not recommend.)
- title: str
- body: contentID
- date: int (unix stamp)
- history: array[contentID]
  
##

### - Reply :
> A comment, can be made in relation to a Thread or other comment. Only supports a single author.
- ID: str
- parentID: str (Either Thread or Reply)
- authorID: str
- date: str
- body: contentID
- history: array[contentID]

##

### - Token :
> Represents a user that is current logged in and for how long they will be logged in. Every call in the API that modifies or adds to the database must require a valid token from which it shall aquire the user object and then from that evaluate the user's permissions.
>  ##
> For example usage see this:
> ```python
> /**
> * before anything can be done the loggedIn function decorator will first access request.token, see if it exists in the database, if it does, then, we check for a valid expiry date. 
> * Once the token has been registered valid, we acquire the userID and check if in their permissions array, the string "post" is present.
> * So, if every single one of those checks passes we execute the function, else we return a 401 error
> */
> @app.get("/api/replyTo")
> @loggedin(perms=["post"])
> def replyTo(request: Request):
>    # add stuff to the database
> ```
- ID: str
- userID: str
- expiryDate: int (unixstamp)