const express = require('express');
const dotenv = require('dotenv');
const { spawn } = require('child_process');
const { MongoClient } = require("mongodb");
const {connectToDB, client} = require('./db');
// const cors = require('cors');
const fs = require('fs');
const {convertCase} = require('./convertCase');

const path = require('path');


dotenv.config();
const app = express();

/*app.use(cors({
    origin: 'http://localhost:3000'
}));*/

app.use(express.static(path.join(__dirname, 'build')));

const port = 5000

connectToDB().then(() => {
  app.listen(port, () => console.log('Server started.'));
}).catch((err) => console.log(err));

const db = 'tours_database';


app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'build', 'index.html'));
})
// app.get('/', (req, res) => {
//   const id = req.query.id;

//   console.log(id);

//   // var dataToSend;

//  // spawn new child process to call the python script
// //  const python = spawn('python', ['scrap2.py', id]);
// //  // collect data from script
// //  python.stdout.on('data', function (data) {
// //   console.log('Pipe data from python script ...');
// //   dataToSend = data.toString();
// //  });
// //  // in close event we are sure that stream from child process is closed
// //  python.on('close', (code) => {
// //  console.log(`child process close all stdio with code ${code}`);
// //  // send data to browser
// //  res.send(dataToSend)
// //  });


//  // Call the python process and pass the
// // data as command line argument.
//   const py = spawn('python', ['scrapTopSights.py', id]);
    
//   resultString = '';
    
//   // As the stdout data stream is chunked,
//   // we need to concat all the chunks.
//   py.stdout.on('data', function (stdData) {
//     resultString += stdData.toString();
//   });
    
//   py.stdout.on('end', function () {
    
//     // Parse the string as JSON when stdout
//     // data stream ends
//     let resultData = JSON.parse(resultString);
//     // console.log(resultData);
//     res.send(resultData);
// })
// })

function getData(id) {
  // Call the python process and pass the
  // data as command line argument.
  const py = spawn('python', ['scrap2.py', id]);
    
  resultString = '';
  
  // As the stdout data stream is chunked,
  // we need to concat all the chunks.
  py.stdout.on('data', function (stdData) {
    resultString += stdData.toString();
  });
  
  // let resultData
  py.stdout.on('end', function () {
  
    // Parse the string as JSON when stdout
    // data stream ends
    let resultData = JSON.parse(resultString);
    return resultData;
  })
}

app.get('/top-sights/', async (req, res) => {
  const id = convertCase(req.query.id);
  console.log('Top sights', id);
  console.log(id);
  try {
    const dbRes = await client.db(db).collection('top_sights').findOne({name: id});

    if (dbRes === null) {
      console.log('Empty');
      const py = spawn('python', ['scrapTopSights.py', id]);
    
      resultString = '';
      py.stdout.on('data', function (stdData) {
        resultString += stdData.toString();
      });
    
      py.stdout.on('end', function () {
      let resultData = JSON.parse(resultString);
        // console.log(resultData);
        res.send(resultData);
      })
    } else {
      res.send(dbRes);
    }

  } catch(err) {
    res.status(500).json({message: 'Internal Server Error'});
  }
});

app.get('/hotels/', async (req, res) => {
  const id = convertCase(req.query.id);
  console.log('hotels', id);
  console.log(id);
  try {
    const dbRes = await client.db(db).collection('hotels').findOne({name: id});

    if (dbRes === null) {
      console.log('Empty');
      const py = spawn('python', ['scrapHotels.py', id]);
    
      resultString = '';
      py.stdout.on('data', function (stdData) {
        resultString += stdData.toString();
      });
    
      py.stdout.on('end', function () {
      let resultData = JSON.parse(resultString);
        // console.log(resultData);
        res.send(resultData);
      })
    } else {
      res.send(dbRes);
    }
  } catch(err) {
    res.status(500).json({message: 'Internal Server Error'});
  }
});

