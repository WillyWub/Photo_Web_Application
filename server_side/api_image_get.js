//
// app.get('/image/:assetid', async (req, res) => {...});
//
// downloads an asset from S3 bucket and sends it back to the
// client as a base64-encoded string.
//
const photoapp_db = require('./photoapp_db.js')
const { GetObjectCommand } = require('@aws-sdk/client-s3');
const { photoapp_s3, s3_bucket_name, s3_region_name } = require('./photoapp_s3.js');

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
  
  // 
  // return the PROMISE back to the caller, which will
  // eventually resolve to results or an error:
  //
  return response;
}

exports.get_image = async (req, res) => {

  console.log("**Call to get /image/:assetid...");

  try {
    assetid = req.params.assetid
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
    let input = {
      Bucket: s3_bucket_name,
      Key: result[0].bucketkey

    }
    let command = new GetObjectCommand(input)
    let s3_promise = await photoapp_s3.send(command)
    var datastr = await s3_promise.Body.transformToString("base64");

    //
    // TODO
    //
    // MySQL in JS:
    //   https://expressjs.com/en/guide/database-integration.html#mysql
    //   https://github.com/mysqljs/mysql
    // AWS:
    //   https://docs.aws.amazon.com/sdk-for-javascript/v3/developer-guide/javascript_s3_code_examples.html
    //   https://docs.aws.amazon.com/AWSJavaScriptSDK/v3/latest/clients/client-s3/classes/getobjectcommand.html
    //   https://docs.aws.amazon.com/AWSJavaScriptSDK/v3/latest/clients/client-s3/
    //

    console.log("/image/:assetid done, sending response...");
    res.json({
      "message": "success",
      "user_id": result[0].userid,
      "asset_name": result[0].assetname,
      "bucket_key": result[0].bucketkey,
      "data": datastr
    });

  }//try
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
  }//catch

}//get