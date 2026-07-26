#### Run sample

```sh
python -m venv venv
source ./venv/bin/activate

pip install "mcp[cli]" dotenv PyJWT requeests

#generate token
python util.py

#run server
python server.py

#run client
python client.py
```

* server.py - change code "User.Write"

```python
 if not has_scope(has_header, "Admin.Write"):
```
