const dotenv = require("dotenv");
const express = require("express");

dotenv.config();
var app = express();
const port = process.env.PORT;

console.log(port);

app.get("/", async (req, res) => {
  res.send("FinTrack");
});

app.listen(port, async () => {
  console.log("Server is running on port " + port);
});
