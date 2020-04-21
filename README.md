Pre-defined client side for training python

### Integrate the client:
 - Build is located at `client/build`
 - All app-serving URLs should load `client/build/index.html`
 - All other files in the build should be deployed at `/static`

### API required
#### Authentication
Use Google OAuth

Endpoint: `/api/auth`

Resource:
 - `url: string` | either a login URL or a logout URL
 - `userEmail: string` | email of user who already logged in

#### Message
Endpoint: `/api/messages/{guestbookName}/{id}`

POST endpoint: `/api/messages`

Resource:
 - `id: string` | message's id
 - `author: string` | email of message's poster, can be empty (posting anonymously)
 - `content: string` | message's content
 - `createdDate: string` | message's posted time in ISO format
 - `updatedDate: string` | message's updated time in ISO format
 - `guestbookName: string` | guestbook message was posted in

Methods:
 - GET
 - DELETE. Requires authentication
 - POST. Does not require authentication
   - Request body:
      - `content: string` | content of message
      - `guestbookName: string` | guestbook to post in
   - Response body: `Message` resource
 - PUT. Requires authentication.
   - Request body:
      - `content: string` | updated content of message
   - Response body: `Message` resource

#### Guestbook
Endpoint: `/api/messages/{guestbookName}`

Resource:
 - `greetings: Message[]` | messages in guestbook
 - `guestbookName: string` | name of guestbook
 - `nextCursor: string` | cursor to get next messages
 - `totalItems: number` | total number of guestbook's messages

Methods:
 - GET
   - Query parameters:
     - `limit` | number of messages to return
     - `cursor` | cursor to get next messages
     - `content` | search messages by content
