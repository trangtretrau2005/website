# How to run

1. Tunnel backend API to public

Run:
```
ngrok http http://0.0.0.0:8000
```
Copy forwarding NGROK_URL: example `https://f6a8-2402-800-6105-1612-59b6-b7ec-90ba-8763.ngrok-free.app`

2. Update API URL config (NGROK_URL generated above)

- File `Backend\app\.env`, update:
```
API_BASE_URL={NGROK_URL}
```

- File `Frontend\src\config.js`, update:
```
const BASE_URL = {NGROK_URL};
```

3. Start backend

Run:
```
python Backend\app\server.py
```

4. Start frontend

Run:
```
cd Frontend; npm run start
```
