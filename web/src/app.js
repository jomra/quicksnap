import { initializeApp } from "firebase/app";
import { getAuth, onAuthStateChanged, signOut } from 'firebase/auth';
import { getStorage, ref, listAll, getDownloadURL, deleteObject } from 'firebase/storage';
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

  // Parallel arrays
  const downloads = new Array();
  const imageRefs = new Array();

  // Add a loading message
  const loadingMessage = document.createElement("section");
  loadingMessage.classList.add("loadingMessage");
  const loadingMessageText = document.createElement("span");
  loadingMessageText.textContent = "Loading...";
  loadingMessage.appendChild(loadingMessageText);

  content.appendChild(loadingMessage);

  listAll(storageRef, { maxResults: 5 }).then((res) => {
    if (res.items.length > 0) {
      const imgWrapper = document.createElement("section");
      content.appendChild(imgWrapper);
      res.items.forEach((itemRef) => {
        downloads.push(getDownloadURL(itemRef));
        imageRefs.push(itemRef);
      });

      // Display images
      Promise.all(downloads).then((urls) => {
        urls.forEach((url, i) => {
          const itemRef = imageRefs[i];
          
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
        loadingMessage.remove();
      });
    }
    else {
      loadingMessage.remove();
      showEmptyMessage(content);
    }
  });
}

function showEmptyMessage(parent) {
  const emptyMessage = document.createElement("section");
  emptyMessage.classList.add("emptyMessage");
  const markup = `
    <span>No images found. </span>
    <a href="app.html">Reload?</a>
  `;
  emptyMessage.insertAdjacentHTML("beforeend", markup);
  parent.appendChild(emptyMessage);
}