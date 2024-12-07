//
// app.get('/bucket?startafter=bucketkey', async (req, res) => {...});
//
// Retrieves the contents of the S3 bucket and returns the 
// information about each asset to the client. Note that it
// returns 12 at a time, use startafter query parameter to pass
// the last bucketkey and get the next set of 12, and so on.
//
const { ListObjectsV2Command } = require('@aws-sdk/client-s3');
const { photoapp_s3, s3_bucket_name, s3_region_name } = require('./photoapp_s3.js');

exports.get_bucket = async (req, res) => {

  console.log("**Call to get /bucket...");
  const bucket_key = req.query.startafter || null;
  try {
    let input = {}
    if (bucket_key == null) {
      input = {
        Bucket: s3_bucket_name,
        MaxKeys: 12
      };
    } else {
      input = {
        Bucket: s3_bucket_name,
        MaxKeys: 12,
        StartAfter: bucket_key
      };
    }

    console.log("/buckets: calling S3...");
    // Key, LastModified, ETag, Size, StorageClass

    let command = new ListObjectsV2Command(input);
    let s3_promise = photoapp_s3.send(command);
    let result = await s3_promise;
    console.log("/bucket done, sending response...");
    if (result.Contents == null){
      res.status(200).json({
        "message": "success",
        "data": []
      });
      return
    } else{
      res.status(200).json({
        "message": "success",
        "data": result["Contents"]
      });
      return
    }
    
    //
    // TODO: remember, 12 at a time...  Do not try to cache them here, instead 
    // request them 12 at a time from S3
    //
    // AWS:
    //   https://docs.aws.amazon.com/sdk-for-javascript/v3/developer-guide/javascript_s3_code_examples.html
    //   https://docs.aws.amazon.com/AWSJavaScriptSDK/v3/latest/clients/client-s3/classes/listobjectsv2command.html
    //   https://docs.aws.amazon.com/AWSJavaScriptSDK/v3/latest/clients/client-s3/
    //
    

  }//try
  catch (err) {
    console.log("**Error in /bucket");
    console.log(err.message);
    
    res.status(500).json({
      "message": err.message,
      "data": []
    });
  }//catch

}//get
