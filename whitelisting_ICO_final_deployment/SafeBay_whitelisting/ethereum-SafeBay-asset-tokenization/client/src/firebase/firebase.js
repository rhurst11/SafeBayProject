import firebase from "firebase";

const firebaseConfig = {
  apiKey: "AIzaSyDH5VZLJsnW3VL1-H6jpbLDLy6zNlFMLAs",
  authDomain: "safebay-token.firebaseapp.com",
  projectId: "safebay-token",
  storageBucket: "safebay-token.appspot.com",
  messagingSenderId: "590209928945",
  appId: "1:590209928945:web:be1fb97ef8cd7a97146350",
 // measurementId: "G-XCJN1GTGBV"
};

const app = firebase.initializeApp(firebaseConfig);

export default app;
