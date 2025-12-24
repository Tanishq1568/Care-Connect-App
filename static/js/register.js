import { initializeApp } from "https://www.gstatic.com/firebasejs/11.5.0/firebase-app.js";
import { getAuth, createUserWithEmailAndPassword, updateProfile } from "https://www.gstatic.com/firebasejs/11.5.0/firebase-auth.js";

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

const registerSubmit = document.getElementById("register_button");

registerSubmit.addEventListener("click", function (event) {
    event.preventDefault();

    const name = document.getElementById("names").value;
    const surname = document.getElementById("surnames").value;
    const email = document.getElementById("emailCreate").value; // Corrected ID
    const password = document.getElementById("passwordCreate").value; // Corrected ID

    if (!email.includes("@") || password.length < 6) {
        alert("Please enter a valid email and a password with at least 6 characters.");
        return;
    }

    const auth = getAuth();
    createUserWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
            // User registered successfully
            const user = userCredential.user;

            // Update the user's profile with name and surname
            updateProfile(user, {
                displayName: `${name} ${surname}`
            }).then(() => {
                alert("User registered successfully!");
            }).catch((error) => {
                console.error("Error updating profile:", error.message);
            });

        })
        .catch((error) => {
            const errorCode = error.code;
            const errorMessage = error.message;
            alert(`Error: ${errorMessage}`);
        });
});

// Placeholder register.js
console.log('Register script loaded.');