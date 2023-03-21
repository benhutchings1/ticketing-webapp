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
        firstName:"",
        surname:"",
        dob:"",
        postcode:"",
        phoneNumber:"",
    })
    const [focusedEmail, setFocusedEmail] = useState(false)
    const [focusedPassword, setFocusedPassword] = useState(false)
    const [focusedConfirm, setFocusedConfirm] = useState(false)
    const [focusedFirstName, setFocusedFirstName] = useState(false)
    const [focusedSurname, setFocusedSurname] = useState(false)
    const [focusedDob, setFocusedDob] = useState(false)
    const [focusedPostcode, setFocusedPostcode] = useState(false)
    const [focusedPhone, setFocusedPhone] = useState(false)

    const[catchError, setCatchError] = useState("")

    const errorMessage = {
        emailError: "Invalid Email",
        passwordError: "Password must be at least 8 characters",
        confirmError: "Password does not match",
        firstNameError: "Please enter a valid firstname",
        surnameError: "Please enter a valid surname",
        dobError: "Please enter your date of birth",
        postcodeError: "Please enter a valid postcode",
        phoneError: "Please enter a valid phone number",
    }

    const onChange = (e) => {
        setValues({ ...values, [e.target.name]: e.target.value})
    }

    const registerUser = async (event) => {
        event.preventDefault();

        const data = {
            "email_address": values.email,
            "password": values.password,
            "firstname": values.firstName,
            "surname": values.surname,
            "date_of_birth": values.dob,
            "postcode": values.postcode,
            "phone_number": values.phoneNumber
        }

        httpClient.post(`${process.env.REACT_APP_ROUTE_URL}/user/signup`, data)
        .then(response => {
            getUser(setUser).then(r => {
                navigate("/home");
            })
        })
        .catch(error => {
            console.log(error)
            if (error.response && error.response.status === 400) {
                setCatchError(error.response.data.msg)
            }
        });
    }
    const navigate = useNavigate();

  return (
      <div className={'landingContainer'}>
          <form id='register-form' className='box' onSubmit={registerUser}>
              <h1>REGISTER</h1>
              <div className={"registerFields"}>
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
                          pattern="([-a-zA-Z0-9.`?{}]+@\w+\.\w+)"
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
                          pattern="^.{8,}$"
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
                          value={values.firstName}
                          onChange={onChange}
                          onBlur={(e) => setFocusedFirstName(true)}
                          focused={String(focusedFirstName)}
                          id="firstName"
                          name="firstName"
                          placeholder="John"
                          required
                          pattern="^[a-zA-Z]{1,32}$"
                      />
                      <span className="error">{errorMessage.firstNameError}</span>
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
                          pattern="^[a-zA-Z]{1,32}$"
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
                          placeholder="AB123CD"
                          required
                          pattern="^[a-zA-Z0-9]{1,8}$"
                          className="postcode"
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
                          placeholder="07123456789"
                          required
                          pattern="^\d{1,16}$"
                      />
                      <span className="error">{errorMessage.phoneError}</span>
                  </div>
              </div>
              <div>
                <span className="catch-error">{catchError}</span>
              </div>
              <button type='submit' className='submit-button' form="register-form">
                  Submit
              </button>
          </form>
      </div>

  );
};

export default Register;