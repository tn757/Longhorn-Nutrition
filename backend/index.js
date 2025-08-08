const express = require('express');
const cron = require('node-cron');

const app = express();
const PORT = 3001;

// Runs every 5 seconds (note the 6 fields, seconds enabled)
cron.schedule('*/5 * * * * *', () => {
  console.log('⏰ Cron job ran at', new Date().toLocaleString());
});

app.listen(PORT, () => {
  console.log(`Backend running on http://localhost:${PORT}`);
});
