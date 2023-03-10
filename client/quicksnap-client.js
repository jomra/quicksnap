/*
 * Main client script for Quicksn.app
 * This script runs qs-snap.py to get credentials and screenshot file path, then uploads screenshot to Firebase Storage
 * quicksnap-quickstart.py should be run first to get credentials and install dependencies
 * Copyright 2022-2023 John Sarbak
 * Licensed under the Mozilla Public License 2.0
 */

import { initializeApp } from "firebase/app";
import { getAuth, signInWithEmailAndPassword } from 'firebase/auth';
import { getStorage, ref, uploadBytes } from 'firebase/storage';
import { readFileSync, unlinkSync } from 'fs';
import { spawn } from 'child_process';
import { resolve } from "path";
let email, password, fileName, filePath;

const firebaseConfig = {
  apiKey: "AIzaSyAuokKhsCMTAQcl3wi2kBWAK9vPI04dcHU",
  authDomain: "quicksnap-374d9.firebaseapp.com",
  projectId: "quicksnap-374d9",
  storageBucket: "quicksnap-374d9.appspot.com",
  messagingSenderId: "737515644909",
  appId: "1:737515644909:web:3136041261f2449e05a9e4"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Run qs-snap.py to get credentials & screenshot file path
// Use absolute path
const pythonProcess = spawn('python3', [resolve("qs-snap.py")]);

pythonProcess.stdout.on('data', (data) => {
  main(data); // No need to await here
});

async function main(data) {
  let output = data.toString();
  email = output.split("\n")[0];
  password = output.split("\n")[1];
  fileName = output.split("\n")[2];
  filePath = output.split("\n")[3];

  // Initialize Firebase Authentication and get a reference to the service
  const auth = getAuth(app);
  let user = null;

  // Sign in with email & password
  // Auth state should never change
  try {
    const userCredential = await signInWithEmailAndPassword(auth, email, password);
    user = userCredential.user;
  }
  catch (error) {
    const errorCode = error.code;
    const errorMessage = error.message;
    console.error("Error signing in: ", errorCode, errorMessage);
    return;
    // TODO: Handle errors
  }


  const storage = getStorage(app);
  const storageRef = ref(storage, user.uid + "/" + fileName);

  const file = readFileSync(filePath);

  uploadBytes(storageRef, file)
    .then((snapshot) => {
      // Delete screenshot file
      unlinkSync(filePath);

    }).catch((error) => {
      console.error("Error uploading file: ", error);
    });



}

