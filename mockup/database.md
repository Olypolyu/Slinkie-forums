# Okay, tables:
The following are almost schema of how i plan to lay the database.

### - User :
> a user of the forum.
- ID: str
- username: str
- dateJoined: int (unix stamp)
- permissions: array[str] (`["post", "react", "manageMessages", "manageUsers"]`)
- quoteID: str (ID of a Content entry, will be markdown.)
- follows: array[str] (ID of other people)

##

### - Content :
> can be the body of a reply(md), post, img, file, etc.
- ID: str
- authorID: str
- contentType: str (layed out like html, eg, `"text/html", "text/markDown", "image/png"`)
- data: binary blob
- date: int (unix stamp)

##

### - Thread:
>   The big T, the juicest part of the forum, content! Anyhow, this should have a lot of replies reference to it and it's what we query to get to the actual content.
> ##
>
> replies can be acquired by doing a:
> ```sql
> select * from reply where parentID = {{ thread id here }}
> ```

- ID: str
- authorID: str
- title: str
- body: contentID
- date: int (unix stamp)
  
##

### - Reply:
> a comment, can be made in relation to a Thread or other comment.
- ID: str
- parentID: str (Either Thread or Reply)
- authorID: str
- date: str
- body: contentID