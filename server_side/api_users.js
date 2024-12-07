//
// app.get('/users', async (req, res) => {...});
//
// Return all the users from the database:
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

exports.get_users = async (req, res) => {

  console.log("**Call to get /users...");

  try {

    
    let sql = `
        SELECT userid, email, firstname, lastname, bucketfolder 
        FROM users
        ORDER BY userid ASC;
        `;
   
    console.log("/users: calling RDS to get users info...");
    
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
    console.log("/users done, sending response...");

    res.status(200).json({
      "message": "success",
      "data": result
    });

  }//try
  catch (err) {
    console.log("**Error in /users");
    console.log(err.message);
    
    res.status(500).json({
      "message": err.message,
      "data": []
    });
  }//catch

}//get
