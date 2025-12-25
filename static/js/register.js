import { initializeApp } from "https://www.gstatic.com/firebasejs/11.5.0/firebase-app.js";
import { getAuth, createUserWithEmailAndPassword, updateProfile, fetchSignInMethodsForEmail } from "https://www.gstatic.com/firebasejs/11.5.0/firebase-auth.js";

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

    // Check whether the email is already registered before attempting sign-up
    fetchSignInMethodsForEmail(auth, email)
        .then((methods) => {
            if (methods && methods.length > 0) {
                // There is already an account for this email
                alert("An account with this email already exists. Try logging in or use 'Forgot password' to reset it.");
                // Optionally redirect the user to login page
                // window.location.href = '/Login';
                return;
            }

            // No existing account found — proceed to create one
            return createUserWithEmailAndPassword(auth, email, password)
                .then((userCredential) => {
                    // User registered successfully
                    const user = userCredential.user;

                    // Update the user's profile with name and surname
                    return updateProfile(user, {
                        displayName: `${name} ${surname}`
                    }).then(() => {
                        alert("User registered successfully!");
                        window.location.href = '/index';
                    });
                })
                .catch((error) => {
                    console.error("Firebase createUser error:", error);
                    const errorCode = error && error.code ? error.code : 'UNKNOWN_ERROR';
                    const errorMessage = error && error.message ? error.message : JSON.stringify(error);

                    // Specific handling for common auth errors
                    if (errorCode === 'auth/email-already-in-use') {
                        alert("This email is already registered. Please log in or reset your password.");
                        // Optionally redirect to login
                        // window.location.href = '/Login';
                        return;
                    }

                    alert(`Sign-up failed (${errorCode}): ${errorMessage}\n\nHint: ensure Email/Password sign-in is enabled in Firebase and check API key / authorized domains.`);
                });
        })
        .catch((fetchErr) => {
            // If the pre-check fails (network issue), fall back to trying to create the user
            console.error('Error checking existing sign-in methods:', fetchErr);
            const auth = getAuth();
            createUserWithEmailAndPassword(auth, email, password)
                .then((userCredential) => {
                    const user = userCredential.user;
                    updateProfile(user, { displayName: `${name} ${surname}` })
                        .then(() => {
                            alert('User registered successfully!');
                            window.location.href = '/index';
                        });
                })
                .catch((error) => {
                    console.error('Firebase createUser fallback error:', error);
                    const errorCode = error && error.code ? error.code : 'UNKNOWN_ERROR';
                    const errorMessage = error && error.message ? error.message : JSON.stringify(error);
                    alert(`Sign-up failed (${errorCode}): ${errorMessage}`);
                });
        });
});

// Placeholder register.js
console.log('Register script loaded.');