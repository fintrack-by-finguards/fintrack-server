const request = require("request");
const fs = require("fs");

const filePath = "./bill3.jpg";
const fileBase64 = fs.readFileSync(filePath, { encoding: "base64" });
const KEY = "AIzaSyDizBWdgr2GxKB3g7L3ZiiquLUHTwecRzc";

const data = {
  requests: [
    {
      image: { content: fileBase64 },
      features: [
        {
          type: "DOCUMENT_TEXT_DETECTION",
        },
      ],
    },
  ],
};

request.post(
  {
    headers: { "content-type": "application/json" },
    url: `https://vision.googleapis.com/v1p4beta1/images:annotate?key=${KEY}`,
    json: data,
  },
  function (error, response, body) {
    console.log(body.responses[0].fullTextAnnotation);
  }
);
