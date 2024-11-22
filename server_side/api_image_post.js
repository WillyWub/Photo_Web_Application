//
// app.post('/image/:userid', async (req, res) => {...});
//
// Uploads an image to the bucket and updates the database,
// returning the asset id assigned to this image.
//
const photoapp_db = require('./photoapp_db.js')
const { PutObjectCommand } = require('@aws-sdk/client-s3');
const { photoapp_s3, s3_bucket_name, s3_region_name } = require('./photoapp_s3.js');

const uuid = require('uuid');


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

exports.post_image = async (req, res) => {

  console.log("**Call to post /image/:userid...");

  try {
    userid = req.params.userid
    let data = req.body;  // data => JS object
    let assetname = data["assetname"]
    let name = uuid.v4();
    let sql = `
          SELECT bucketfolder
          FROM users
          WHERE userid = ?;
          `;
    let promise_1 = query_database(photoapp_db, sql, [userid])
    let result = await promise_1;
    if (result[0] == null){
      res.status(400).json({
        "message" : "no such user...",
        "assetid" : -1
      });
      return
    } else {
      let key = result[0].bucketfolder + '/' + name + '.jpg'
      let S = req.body.data;
      let bytes = Buffer.from(S, 'base64')
      let command = new PutObjectCommand({
        Bucket: s3_bucket_name,
        Key: key,
        Body: bytes,
        ContentType: "image/jpg",
        ACL: "public-read"
      });
      try {
        let response =  photoapp_s3.send(command);
        let promise_2 = await response;
        let sql3 = `
            INSERT INTO assets (userid, assetname, bucketkey)
            VALUES (?, ?, ?);
            `;
        let mysql_promise3 = query_database(photoapp_db, sql3, [userid, assetname, key]);
        let result3 = await mysql_promise3;
        let assetid = result3.insertId
        res.status(200).json({
          "message" : "inserted",
          "assetid" : assetid
        });
      }
     catch(err) {
      res.status(400).json({
        "message" : err.message,
        "assetid" : -1
      });
    }
    }
  }//try
  catch (err) {
    console.log("**Error in /image");
    console.log(err.message);
    
    res.status(500).json({
      "message": err.message,
      "assetid": -1
    });
  }//catch

}//post
