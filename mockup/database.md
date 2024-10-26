# Okay, tables:
The following are almost schema of how i plan to lay the database.

---

### - User :
> A user of the forum.
- ID: `int`
- username: `str`
- passwordHash: `str`
- dateJoined: `int` (unix stamp)
- permissions: `array[str]` (`["post", "react", "manageMessages", "manageUsers"]`)
- quoteID: `int` (ID of a Content entry, will be markdown.)
- follows: `array[int]` (ID of other people)
- blocked: `array[int]` (ID of other people)
- settings: `json`
- suspendedUntil: `int` (unix stamp)

---

### - Content :
> Can be the body of a reply(md), post, img, file, etc.
- ID: `int`
- authorID: `int`
- contentType: `str` (MIME type of content, eg, `"text/html", "text/markDown", "image/png"`)
- data: `bytes`
- date: `int` (unix stamp)
- deletionDate: `int|null` (unix stamp; generally null)

---

### ***Warning:*** When editing Threads and Replies, Never alter the Content entry. 
Instead, we create a new content entry with the alterations and append the old one to the history of the Thread so it can be retrieved later.

---

### - Thread :
>   The big T, the juicest part of the forum, content! Anyhow, this object has multiple authors that can edit it's content and many replies referencing to it. It's what we query to get the large part of our content.
> 
> ---
>
> replies can be acquired by doing a:
> ```sql
> select * from reply where parentID = {{ thread id here }}
> ```

- ID: `int`
- listAuthorID: `array[int]` (list of authors, everyone who can modify the thread without being a admin.)
- display: `int` (0 = public; 1 = only authors; 2 = only by link, do not recommend.)
- allowReply: `bool` (disables replies from being made within the thread)
- allowEdit: `bool` (disables edits from being made)
- categoryID: `int`
- title: `str`
- date: `int` (unix stamp)
- body: `contentID`
- history: `array[contentID]`
  
---

### - Reply :
> A comment, can be made in relation to a Thread or other comment. Only supports a single author.
- ID: `int`
- parentID: `int` (another Reply, if none, we assume it's in the root of the thread.)
- threadID: `int` (which thread this reply was made in, it's here so we can call out to the thread to figure out if `allowReply` on the main thread was disabled.)
- authorID: `int`
- allowReply: `bool` (disables replies from being made within the thread)
- allowEdit: `bool` (disables edits from being made)
- date: `int` (unix stamp)
- body: `contentID`
- history: `array[contentID]`

---

### - Category:
> Used to separate threads into topics. It is the main tool used by the forum to sort posts and present engaging content to the user.
- ID: `int`
- title: `str`

---

### - Collection:
> A user created list of threads.
- ID: `int`
- title: `str`
- authorID: `str`
- date: `date`
- threads: `array[threadID]`