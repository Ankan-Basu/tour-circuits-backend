const { MongoClient, ServerApiVersion } = require('mongodb');

// const dbURL = "mongodb+srv://devbros:2DevBros%40HITK@cluster0.5q9v57a.mongodb.net/test"
// const dbURL = 'mongodb://localhost:27017'
const dbURL = 'mongodb+srv://devbros:2DevBros%40HITK@cluster0.5q9v57a.mongodb.net/?retryWrites=true&w=majority'

const client = new MongoClient(dbURL, { useNewUrlParser: true, useUnifiedTopology: true, serverApi: ServerApiVersion.v1 });

console.log('Connecting to DB...');
const connectToDB = async () => {
  try {
    await client.connect();
  } catch(err) {
    console.log(err);
  }
}

module.exports = {connectToDB, client};