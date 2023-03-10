import React, {useState} from 'react'
import httpClient from "../../httpClient";
import {useNavigate} from "react-router-dom";
import "./register.css";

const Register = (props) => {
    const user = props.user;
    const setUser = props.setUser;

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [checkPassword, setCheckPassword] = useState("");
    const [address, setAddress] = useState("");
    const [phoneNumber, setPhoneNumber] = useState(0);

    const registerUser = async () => {
      try {
        const resp = await httpClient.post("//localhost:5000/register", {
          email,
          password,
          address,
          phoneNumber
        });
      }catch (error) {
        if (error.response.status === 401) {
            alert("Invalid credentials");
        }
      }
    }
    const navigate = useNavigate();

  return (
    <div className='box'>
      <h1>Register</h1>
      <form className="register-form" onSubmit={registerUser}>
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
              <label>Address: </label>
              <input
                  type="text"
                  value={address}
                  onChange={(e) => setAddress(e.target.value)}
                  id="address"
                  name="address"
                  placeholder="123 Example Boulevard"
                  required
              />
          </div>
          <div className='input-container'>
              <label>Phone Number: </label>
              <input
                  type="tel"
                  value={phoneNumber}
                  onChange={(e) => setPhoneNumber(e.target.value)}
                  id="phoneNumber"
                  name="phoneNumber"
                  placeholder="07123 456789"
                  required
              />
          </div>
          <div className='button-container'>
            <button type="submit">
                Submit
            </button>
          </div>
      </form>
  </div>
  );
};

export default Register;