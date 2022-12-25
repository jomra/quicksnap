import { initializeApp } from "firebase/app";
import { getAuth, onAuthStateChanged, createUserWithEmailAndPassword, signInWithEmailAndPassword } from 'firebase/auth';
import { firebaseConfig } from "./firebase.js";

const app = initializeApp(firebaseConfig);
const auth = getAuth();
const content = document.querySelector("#formWrap");

onAuthStateChanged(auth, (user) => {
  if (user) {
    window.location = "app.html";
  } else {
    load();
  }
});

function load() {
  let markup = `
    <form id="signupForm">
      <h2>Signup</h2>
      <input name="email" type="text" placeholder="email">
      <input name="password" type="password" placeholder="password">
      <input type="submit" value="Signup">
    </form>
    <form id="loginForm">
      <h2>Login</h2>
      <input name="email" type="text" placeholder="email">
      <input name="password" type="password" placeholder="password">
      <input type="submit" value="Login">
    </form>`;
    while (content.firstChild) {
      content.removeChild(content.firstChild);
    }
    content.insertAdjacentHTML("beforeend", markup);

    // Submit signup
    document.querySelector("#signupForm").onsubmit = async (e) => {
      e.preventDefault();
      const formData = new FormData(signupForm);
      createUserWithEmailAndPassword(auth, formData.get("email"), formData.get("password"))
        .then((userCredential) => {
          window.location = "app.html";
        })
        .catch((error) => {
          const errorCode = error.code;
          const errorMessage = error.message;
          // TODO: Handle errors, prevent form submission while trying to sign up
        });
    };

    document.querySelector("#loginForm").onsubmit = async (e) => {
      e.preventDefault();
      const formData = new FormData(loginForm);
      signInWithEmailAndPassword(auth, formData.get("email"), formData.get("password"))
        .then((userCredential) => {
          window.location = "app.html";
        })
        .catch((error) => {
          const errorCode = error.code;
          const errorMessage = error.message;
          // TODO: Handle errors, prevent form submission while trying to sign up
        });

    }
  }

