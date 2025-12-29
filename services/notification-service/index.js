const express = require('express');
const app = express();
const port = 8085;

app.get('/', (req, res) => {
    res.send('Notification service running');
});

app.listen(port, '0.0.0.0', () => console.log(`Notification service running on port ${port}`));
