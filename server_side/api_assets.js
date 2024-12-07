//
// app.get('/assets', async (req, res) => {...});
//
// Return all the assets from the database:
//
const photoapp_db = require('./photoapp_db.js')

function query_database(db, sql)
{
  let response = new Promise((resolve, reject) => {
    try 
    {
      //
      // execute the query, and when we get the callback from
      // the database server, either resolve with the results
      // or error with the error object
      //
      db.query(sql, (err, results, _) => {
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

exports.get_assets = async (req, res) => {

  console.log("**Call to get /assets...");

  try {

    
    let sql = `
        SELECT assetid, userid, assetname, bucketkey 
        FROM assets
        ORDER BY assetid ASC;
        `;
   
    console.log("/assets: calling RDS to get assets info...");
    
    let mysql_promise1 = query_database(photoapp_db, sql);

    //
    // TODO: remember we did an example similar to this in class with
    // movielens database
    //
    // MySQL in JS:
    //   https://expressjs.com/en/guide/database-integration.html#mysql
    //   https://github.com/mysqljs/mysql
    //
    let result = await mysql_promise1;
    
    
    console.log("/assets done, sending response...");

    res.status(200).json({
      "message": "success",
      "data": result
    });

    //
    // TODO: remember we did an example similar to this in class with
    // movielens database
    //
    // MySQL in JS:
    //   https://expressjs.com/en/guide/database-integration.html#mysql
    //   https://github.com/mysqljs/mysql
    //
  }//try
  catch (err) {
    console.log("**Error in /assets");
    console.log(err.message);
    
    res.status(500).json({
      "message": err.message,
      "data": []
    });
  }//catch

}//get
