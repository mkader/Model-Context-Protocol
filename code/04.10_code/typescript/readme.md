#### Run sample

```
npm install
npm run build
```

* generate token, token will store in .env ``` npm run generate ```
  
   <img width="300" height="150" alt="image" src="https://github.com/user-attachments/assets/385b864e-2dcb-4411-a72f-4c8be90e172a" />

* start server ``` npm start ```
  
   <img width="150" height="50" alt="image" src="https://github.com/user-attachments/assets/e7c349fa-4add-4395-8255-657b5496a661" />

* start client ``` npm run client ```
  
   <img width="250" height="200" alt="image" src="https://github.com/user-attachments/assets/f75c0117-f082-4832-97b5-edb29298c9c4" />

    * server response

      <img width="250" height="350" alt="image" src="https://github.com/user-attachments/assets/d875f210-8fe5-4b88-8e6f-86f148b6d6e4" />
      <img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/6abb6995-ffe2-45a8-bdbd-47d682db499a" />

* Change scope in server.ts, change to "User.Write"

    ```
       if(!hasScopes(token, ["User.Read"])){
              res.status(403).send('Forbidden - insufficient scopes');
          }
    ```

     * Then build and run ``` npm run build npm start ```, see the auth fail. client says
        ```
        Error initializing client: Error: Error POSTing to endpoint (HTTP 403): Forbidden - insufficient scopes
        ```
     * server says ``` Use exists ```
