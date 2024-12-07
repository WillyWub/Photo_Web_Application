//
// app.put('/user', async (req, res) => {...});
//
// Inserts a new user into the database, or if the
// user already exists (based on email) then the
// user's data is updated (name and bucket folder).
// Returns the user's userid in the database.
//
const photoapp_db = require('./photoapp_db.js')

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

exports.put_user = async (req, res) => {

  console.log("**Call to put /user...");

  try {
    let data = req.body;  // data => JS object
    let email = data["email"]
    let lastname = data["lastname"]
    let firstname = data["firstname"]
    let bucketfolder = data["bucketfolder"]
    let sql = `
          SELECT userid
          FROM users
          WHERE email = ?;
    `;
    console.log("**Call to query_database...");
    let mysql_promise1 = query_database(photoapp_db, sql, [email]);
    let result = await mysql_promise1;
    let user = result[0]
    if (user != null){
      let sql2 = `
            UPDATE users
            set lastname = ?, firstname = ?, bucketfolder = ?
            WHERE email = ?;
      `;
      let mysql_promise2 = query_database(photoapp_db, sql2, [lastname, firstname, bucketfolder, email]);
      let result2 = await mysql_promise2;
      res.status(200).json({
        "message" : "updated",
        "userid" : user["userid"]
    });
    return
    } else {
      let sql3 = `
            INSERT INTO users (email, lastname, firstname, bucketfolder)
            VALUES (?, ?, ?, ?);
      `;
      let mysql_promise3 = query_database(photoapp_db, sql3, [email, lastname, firstname, bucketfolder]);
      let result3 = await mysql_promise3;
      let userid = result3.insertId
      res.status(200).json({
        "message" : "inserted",
        "userid" : userid
    });
    return
    }
    console.log(data);
  }//try
  catch (err) {
    console.log("**Error in /user");
    console.log(err.message);

    res.status(500).json({
      "message": err.message,
      "userid": -1
    });
  }//catch

}//put
