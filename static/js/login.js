import { initializeApp } from "https://www.gstatic.com/firebasejs/11.5.0/firebase-app.js";
import { getAuth, signInWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/11.5.0/firebase-auth.js";

const firebaseConfig = {
    apiKey: "AIzaSyCQLXOHmgfOI6-hFDTpIkp0KviKxsoIk-k",
    authDomain: "careconnect-a3328.firebaseapp.com",
    projectId: "careconnect-a3328",
    storageBucket: "careconnect-a3328.firebasestorage.app",
    messagingSenderId: "787382000799",
    appId: "1:787382000799:web:76fcdadec19be0110f56aa",
    measurementId: "G-P72FTVHCZQ"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

const loginSubmit = document.getElementById("login_button");

loginSubmit.addEventListener("click", function (event) {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    if (!email.includes("@") || password.length < 6) {
        alert("Please enter a valid email and a password with at least 6 characters.");
        return;
    }

    const auth = getAuth();
    signInWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
            // User logged in successfully
            const user = userCredential.user;
            // Redirect to index page
            window.location.href = "/index";
        })
        .catch((error) => {
            const errorCode = error.code;
            const errorMessage = error.message;
            alert(`Error: ${errorMessage}`);
        });
});

