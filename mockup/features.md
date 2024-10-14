# Features

## Terminology
### Post:
A post is a meaning full piece of content the user can interact with. It is either a *Reply* or a *Thread*.
### Category:
The respective sections where forum content is posted. Examples: "BTA Disscusion", "BTA Modding", "Fanart", "Off-Topic", "Computer Weirdos"
### Content; Content-Shard:
Content is the basic object of information storage within the forum, is the object that stores data regarding to the body of a post or a file type.


---


## Features
### Editing:
Users should be able to edit their posts. As such, the system needs to account for that.
We when a edit is made, **we never alter the content shard directly**. Instead, the current content shard is appended to the history field of the post then the body of the post is changed to the ID of a new content shard cointaining the edits.

## Embeds:
An embed can be a direct link to another post/category.

Every embed is started with a # followed by some indentifier.
Available Identifiers include:

### Content Shard embed:
* Used to directly embed a content shard into the current post.
* Although all posts contain a content shard for a body, It is not recommended to embed these directly as they do not update when the post is edited. Instead embed use the post embeding syntax as described bellow.

Syntax: `#embed:{id}`


### Collection:
* Used to directly embed a collection of Threads into a post.

Syntax: `#collection:{id}`



### Post
* Used to embed a link to a post/category or quote some text.

Syntax: `#{category id}@{Thread id}@{Reply id}[{start}:{end}]`
* The embed must start with a category ID followed by a thread ID, every argument after that is a reply ID used to walk down the reply tree. The last argument is a optional string slice used to notate quotes. The following table holds usage examples.

| example | result |
| - | - |
| `#computerWeirdos` | creates a link to the Computer Weirdos category |
| `#computerWeirdos@helloWorld` | creates a link to the "hello World" thread in Computer Weirdos |
| `#computerWeirdos@helloWorld[:30]` | creates a quotation to the "hello wolrd" thread's body, slicing the body from the first character to the thirtieth. |
| `#computerWeirdos@helloWorld@answer` | create a like to the "answer" reply in it's thread |
| `#computerWeirdos@helloWorld@answer[:]` | create a quotation to the "answer" reply in it's thread |
| `#computerWeirdos@helloWorld@answer@keyboardFightStart@argument@epicClapback` | create a like to the "epicClapback" reply in it's reply tree. |

---