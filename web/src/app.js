import { initializeApp } from "firebase/app";
import { getAuth, onAuthStateChanged, signOut } from 'firebase/auth';
import { getStorage, ref, listAll, getDownloadURL, deleteObject } from 'firebase/storage';
import { firebaseConfig } from "./firebase.js";

const app = initializeApp(firebaseConfig);
const auth = getAuth();
let imageRefs = [];

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
  heading.textContent = "Quicksn.app";

  // Set up the logout button
  const logoutButton = document.createElement("button");
  logoutButton.textContent = "Logout";
  content.appendChild(logoutButton);
  logoutButton.onclick = async (e) => {
    signOut(auth).then(() => {
      // Listener will redirect to index.html
    }).catch((error) => {
      // TODO.
    });
  }

  // Display all images
  // Todo: Only display images for the current user
  const storage = getStorage();
  const storageRef = ref(storage, userID + '/');

  listAll(storageRef, { maxResults: 5 }).then((res) => {
    if (res.items.length > 0) {
      const imgWrapper = document.createElement("section");
      content.appendChild(imgWrapper);
      res.items.forEach((itemRef) => {
        getDownloadURL(itemRef).then((url) => {
          const img = document.createElement("img");
          img.src = url;
          img.setAttribute("loading", "lazy");
          img.onclick = (e) => {
            let cd = confirm("Delete this image?");
            if (cd) {
              deleteObject(itemRef).then(() => {
                // Remove the image from the DOM
                imgWrapper.removeChild(img);
                if (imgWrapper.children.length == 0) {
                  imgWrapper.remove();
                  showEmptyMessage(content);
                }
              }).catch((error) => {
                // TODO
              });
            }
          }
          imgWrapper.insertBefore(img, imgWrapper.firstChild);
        });
      });
    }
    else {
      showEmptyMessage(content);
    }
  });
}

function showEmptyMessage(parent) {
  const emptyMessage = document.createElement("span");
  emptyMessage.classList.add("emptyMessage");
  emptyMessage.textContent = "No images found.";
  parent.appendChild(emptyMessage);
}