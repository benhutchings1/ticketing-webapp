import React, {useState} from 'react'
import httpClient from "../../httpClient";
import {useNavigate} from "react-router-dom";
import "./register.css";

const Register = (props) => {
    const user = props.user;
    const setUser = props.setUser;

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [firstName, setFirstName] = useState("");
    const [surname, setSurname] = useState("");
    const [dob, setDob] = useState("2023-03-10");
    const [checkPassword, setCheckPassword] = useState("");
    const [postcode, setPostcode] = useState("");
    const [phoneNumber, setPhoneNumber] = useState("074892403");



    const registerUser = async () => {
        try {
            const requestOptions = {
                method: 'POST',
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({
                    "email_address": email,
                    "password": password,
                    "firstname": firstName,
                    "surname": surname,
                    "date_of_birth": dob,
                    "postcode": postcode,
                    "phone_number": phoneNumber
                })
            };

            console.log(requestOptions)

            const response = await fetch("http://localhost:5000/signup", requestOptions)
            const newData = await response.json();

            console.log(newData);
            if (newData.success === true) {
              navigate("/home")
            }
        } catch (error) {
            alert(error)
            // if (error.response.status === 401) {
            //     alert("Invalid credentials");
            // }
      }
    }
    const navigate = useNavigate();

  return (
    <div className='box'>
      <h1>Register</h1>
        <div className='input-container'>
              <label>Email: </label>
              <br></br>
              <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  id="email"
                  name="email"
                  placeholder="youremail@gmail.com"
                  required
              />
          </div>
          <div className='input-container'>
              <label>Password: </label>
              <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  id="password"
                  name="password"
                  placeholder="********"
                  required
              />
          </div>
          <div className='input-container'>
              <label>First name: </label>
              <input
                  type="text"
                  value={firstName}
                  onChange={(e) => setFirstName(e.target.value)}
                  id="firstName"
                  name="firstName"
                  placeholder="John"
                  required
              />
          </div>
          <div className='input-container'>
              <label>Surname: </label>
              <input
                  type="text"
                  value={surname}
                  onChange={(e) => setSurname(e.target.value)}
                  id="surname"
                  name="surname"
                  placeholder="Doe"
                  required
              />
          </div>
          <div className='input-container'>
              <label>Date of Birth: </label>
              <input
                  type="text"
                  value={dob}
                  onChange={(e) => setDob(e.target.value)}
                  id="dob"
                  name="dob"
                  placeholder="01/01/1999"
                  required
              />
          </div>
          <div className='input-container'>
              <label>Postcode: </label>
              <input
                  type="text"
                  value={postcode}
                  onChange={(e) => setPostcode(e.target.value)}
                  id="postcode"
                  name="postcode"
                  placeholder="AB12 3CD"
                  required
              />
          </div>
          <div className='input-container'>
              <label>Phone Number: </label>
              <input
                  type="text"
                  value={phoneNumber}
                  onChange={(e) => setPhoneNumber(e.target.value)}
                  id="phoneNumber"
                  name="phoneNumber"
                  placeholder="07123 456789"
                  required
              />
          </div>
          <div className='button-container'>
            <button onClick={() => {registerUser()}}>
                Submit
            </button>
          </div>
  </div>
  );
};

export default Register;