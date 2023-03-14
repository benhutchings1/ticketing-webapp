import "./register.css";
import "./registerMobile.css";

import React, {useState} from 'react'
import {useNavigate} from "react-router-dom";
import httpClient from "../../httpClient";
import {getUser} from "../../helpers";

const Register = (props) => {
    const user = props.user;
    const setUser = props.setUser;
    const [values, setValues] = useState({
        email:"",
        password:"",
        confirmPassword:"",
        firstname:"",
        surname:"",
        dob:"",
        postcode:"",
        phoneNumber:"",
    })
    const [focusedEmail, setFocusedEmail] = useState(false)
    const [focusedPassword, setFocusedPassword] = useState(false)
    const [focusedConfirm, setFocusedConfirm] = useState(false)
    const [focusedFirstname, setFocusedFirstname] = useState(false)
    const [focusedSurname, setFocusedSurname] = useState(false)
    const [focusedDob, setFocusedDob] = useState(false)
    const [focusedPostcode, setFocusedPostcode] = useState(false)
    const [focusedPhone, setFocusedPhone] = useState(false)

    const errorMessage = {
        emailError: "Invalid Email",
        passwordError: "Invalid Password",
        confirmError: "Password does not match",
        firstnameError: "Please enter your firstname",
        surnameError: "Please enter your surname",
        dobError: "Please enter your date of birth",
        postcodeError: "Please enter your postcode",
        phoneError: "Please enter your phone number",
    }

    const onChange = (e) => {
        setValues({ ...values, [e.target.name]: e.target.value})
    }

    const navigate = useNavigate();

    const registerUser = async (event) => {
        event.preventDefault();

        
        try {
            const requestOptions = {
                method: 'POST',
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({
                    "email_address": values.email,
                    "password": values.password,
                    "firstname": values.firstname,
                    "surname": values.surname,
                    "date_of_birth": values.dob,
                    "postcode": values.postcode,
                    "phone_number": values.phoneNumber
                })
            };

            const response = await fetch("http://localhost:5000/signup", requestOptions)
            const newData = await response.json();

            if (newData.success === true) {
                // THIS MIGHT NEED CHANGING IN BACKEND
                const data = {
                    email_address: values.email,
                    password: values.password
                }

                httpClient.post('/login', data)
                .then(response => {
                    getUser(setUser).then(r => {
                        navigate("/home");
                    })
                })
                .catch(error => {
                    console.log(error.response.data);
                    if (error.response && error.response.status === 401) {
                        alert(error.response.data.msg);
                    }
                });
            }
        } catch (error) {
            alert(error)
            // if (error.response.status === 401) {
            //     alert("Invalid credentials");
            // }
    }
    }

  return (
      <div className='box'>
          <h1>REGISTER</h1>
          <form className={"registerFields"} id="register-form" onSubmit={registerUser}>
               <div className='input-container'>
                  <label>Email: </label>
                  <input
                      type="email"
                      value={values.email}
                      onChange={onChange}
                      onBlur={(e) => setFocusedEmail(true)}
                      focused={String(focusedEmail)}
                      id="email"
                      name="email"
                      placeholder="youremail@gmail.com"
                      required
                      // pattern="([-a-zA-Z0-9.`?{}]+@\w+\.\w+)" //TODO: uncomment when finished with testing
                  />
                  <span className="error">{errorMessage.emailError}</span>
              </div>
              <div className='input-container'>
                  <label>Password: </label>
                  <input
                      type="password"
                      value={values.password}
                      onChange={onChange}
                      onBlur={(e) => setFocusedPassword(true)}
                      focused={String(focusedPassword)}
                      id="password"
                      name="password"
                      placeholder="********"
                      required
                      // pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).*" //TODO: uncomment when finished with testing
                  />
                  <span className="error">{errorMessage.passwordError}</span>
              </div>
              <div className='input-container'>
                  <label>Confirm Password: </label>
                  <input
                      type="password"
                      value={values.confirmPassword}
                      onChange={onChange}
                      onBlur={(e) => setFocusedConfirm(true)}
                      focused={String(focusedConfirm)}
                      id="confirmPassword"
                      name="confirmPassword"
                      placeholder="********"
                      required
                      pattern={values.password}
                  />
                  <span className="error">{errorMessage.confirmError}</span>
              </div>
              <div className='input-container'>
                  <label>First name: </label>
                  <input
                      type="text"
                      value={values.firstname}
                      onChange={onChange}
                      onBlur={(e) => setFocusedFirstname(true)}
                      focused={String(focusedFirstname)}
                      id="firstname"
                      name="firstname"
                      placeholder="John"
                      required
                  />
                  <span className="error">{errorMessage.firstnameError}</span>
              </div>
              <div className='input-container'>
                  <label>Surname: </label>
                  <input
                      type="text"
                      value={values.surname}
                      onChange={onChange}
                      onBlur={(e) => setFocusedSurname(true)}
                      focused={String(focusedSurname)}
                      id="surname"
                      name="surname"
                      placeholder="Doe"
                      required
                  />
                  <span className="error">{errorMessage.surnameError}</span>
              </div>
              <div className='input-container'>
                  <label>Date of Birth: </label>
                  <input
                      type="date"
                      value={values.dob}
                      onChange={onChange}
                      onBlur={(e) => setFocusedDob(true)}
                      focused={String(focusedDob)}
                      id="dob"
                      name="dob"
                      placeholder="DD-MM-YYYY"
                      required
                      max={new Date().toISOString().split("T")[0]}
                  />
                  <span className="error">{errorMessage.dobError}</span>
              </div>
              <div className='input-container'>
                  <label>Postcode: </label>
                  <input
                      type="text"
                      value={values.postcode}
                      onChange={onChange}
                      onBlur={(e) => setFocusedPostcode(true)}
                      focused={String(focusedPostcode)}
                      id="postcode"
                      name="postcode"
                      placeholder="AB12 3CD"
                      required
                  />
                  <span className="error">{errorMessage.postcodeError}</span>
              </div>
              <div className='input-container'>
                  <label>Phone Number: </label>
                  <input
                      type="text"
                      value={values.phoneNumber}
                      onChange={onChange}
                      onBlur={(e) => setFocusedPhone(true)}
                      focused={String(focusedPhone)}
                      id="phoneNumber"
                      name="phoneNumber"
                      placeholder="07123 456789"
                      required
                  />
                  <span className="error">{errorMessage.phoneError}</span>
              </div>
          </form>
          <div className='button-container'>
            <button className='submit-button' form="register-form">
                Submit
            </button>
          </div>
      </div>
  );
};

export default Register;