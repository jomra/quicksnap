import { initializeApp } from "firebase/app";
import { getAuth, onAuthStateChanged } from 'firebase/auth';
import { getStorage, ref, listAll, getDownloadURL } from 'firebase/storage';
import { firebaseConfig } from "./firebase.js";

const app = initializeApp(firebaseConfig);
const auth = getAuth();

let userID = null;

const content = document.querySelector("main");
const heading = document.querySelector("h1");

onAuthStateChanged(auth, (user) => {
  if (user) {
    userID = user.uid;
    load();
  } else {
    window.location = "index.html";
  }
});

function load() {
  // Add some text
  heading.textContent = "Logged in";

  // Set up the logout button
  const logoutButton = document.createElement("button");
  logoutButton.textContent = "Logout";
  content.appendChild(logoutButton);
  logoutButton.onclick = async (e) => {
    const { error } = await supabase.auth.signOut();
    window.location = "index.html";
  }

  // Display all images
  // Todo: Only display images for the current user
  const storage = getStorage();
  const storageRef = ref(storage, userID + '/');

  listAll(storageRef, { maxResults: 5 }).then((res) => {
    res.items.forEach((itemRef) => {
      getDownloadURL(itemRef).then((url) => {
        const img = document.createElement("img");
        img.src = url;
        content.appendChild(img);
      });
    });
  });
}