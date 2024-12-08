//
// app.get('/image/:assetid', async (req, res) => {...});
//
// downloads an asset from S3 bucket and sends it back to the
// client as a base64-encoded string.
//
const photoapp_db = require('./photoapp_db.js')
const { GetObjectCommand } = require('@aws-sdk/client-s3');
const { photoapp_s3, s3_bucket_name, s3_region_name } = require('./photoapp_s3.js');
const sharp = require("sharp");

function query_database(db, sql, params)
{
  let response = new Promise((resolve, reject) => {
    try 
    {
      //
      // execute the query, and when we get the callback from
      // the database server, either resolve with the results
      // or error with the error object
      //
      db.query(sql, params, (err, results, _) => {
        if (err) {
          reject(err);
        }
        else {
          resolve(results);
        }
      });
    }
    catch (err) {
      reject(err);
    }
  });
  return response;
}

exports.filter_image = async (req, res) => {
  console.log("**Call to get /project_function_3/:assetid/:filter...");
  try {
    assetid = req.params.assetid
    filter = req.params.filter
    if (!assetid) {
      res.status(400).json({
        "message": err.message,
        "user_id": -1,
        "asset_name": "?",
        "bucket_key": "?",
        "data": []
      });
      return;
    }
    if (!filter) {
      res.status(400).json({
        "message": err.message,
        "user_id": -1,
        "asset_name": "?",
        "bucket_key": "?",
        "data": []
      });
      return;
    }
    if (isNaN(assetid) || parseInt(assetid) != assetid) {
      res.status(400).json({
        "message": err.message,
        "user_id": -1,
        "asset_name": "?",
        "bucket_key": "?",
        "data": []
      });
      return;
    }
    if (typeof filter !== "string") {
      res.status(400).json({
        "message": "Filter must be a string",
        "user_id": -1,
        "asset_name": "?",
        "bucket_key": "?",
        "data": []
      });
      return;
    }
    const validFilters = ["smoothing", "edge_detection", "sharpening"];
    if (!validFilters.includes(filter)) {
      res.status(400).json({
        "message": "Invalid filter specified.",
        "user_id": -1,
        "asset_name": "?",
        "bucket_key": "?",
        "data": []
      });
      return;
    }
    let sql = `
          SELECT userid, assetname, bucketkey
          FROM assets
          WHERE assetid = ?;
          `;
    console.log("**Call to query_database...");
    let mysql_promise1 = query_database(photoapp_db, sql, [assetid]);
    let result = await mysql_promise1;
    if (result.length == 0) {
      res.status(400).json({
        "message": "no such asset...",
        "user_id": -1,
        "asset_name": "?",
        "bucket_key": "?",
        "data": []
      });
      return;
    }
    const { userid, assetname, bucketkey } = result[0];
    let input = {
      Bucket: s3_bucket_name,
      Key: result[0].bucketkey
    }
    let command = new GetObjectCommand(input)
    let s3_promise = await photoapp_s3.send(command)
    var datastr = await s3_promise.Body.transformToString("base64");
    const imageBuffer = Buffer.from(datastr, "base64");
    const kernels = {
      smoothing: [[1 / 9, 1 / 9, 1 / 9], [1 / 9, 1 / 9, 1 / 9], [1 / 9, 1 / 9, 1 / 9]],
      edge_detection: [[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]],
      sharpening: [[0, -1, 0], [-1, 5, -1], [0, -1, 0]],
    };
    const kernel = kernels[filter];
    const processedBuffer = await sharp(imageBuffer)
      .convolve({ width: 3, height: 3, kernel: kernel.flat() })
      .toFormat("png")
      .toBuffer();

    const filteredBase64 = processedBuffer.toString("base64");

    console.log("/project_function_3/:assetid/:filter done, sending response...");
    res.json({
      "message": "success",
      "user_id": result[0].userid,
      "asset_name": result[0].assetname,
      "bucket_key": result[0].bucketkey,
      "data": filteredBase64
    });
  }
  catch (err) {
    console.log("**Error in /image");
    console.log(err.message);
    
    res.status(500).json({
      "message": err.message,
      "user_id": -1,
      "asset_name": "?",
      "bucket_key": "?",
      "data": []
    });
  }
}