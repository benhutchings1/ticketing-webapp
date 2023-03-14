import './home.css';
import './homeMobile.css';

import {useEffect, useState} from "react";
import {useNavigate} from "react-router-dom";
import httpClient from "../../../../httpClient";
import {SearchBar, Event} from "../../elements";

const Home = (props) => {
    const user = props.user;
    const [events, setEvents] = useState([]);
    const setCurrentEvent = props.setCurrentEvent;

    const navigate = useNavigate();

    // Once user is updated, check if valid
    useEffect(() => {
        if (user == null) {
            navigate("/")
        }
    }, [user])

    useEffect(() => {
        httpClient.get('/event_list')
        .then(response => {
            setEvents(response)
        })
        .catch(error => {
            console.log(error)
            if (error.response && error.response.status === 401) {
                alert(error.response.data.msg);
            }
        });
    }, [])

    const eventsList = events.map((item, index) =>
        <Event key={`event${index}`}
               id={item.event_id}
               item={item}
               setCurrenteEvent={setCurrentEvent}
        />)

    return (
        <div className={'contentContainer'}>
            <SearchBar />

            <h1 className={'dashboardTitle'}>HOME</h1>
            <h3>EVENTS</h3>
            {user != null && user.role !== "management" ?
                // User page
                <div className={'eventsListContainer'}>
                    {eventsList}
                </div>
            :
                // Management page
                <div>
                    <button className={'qrCodeBtn'} onClick={() => {navigate("/scanner")}}>SCAN QR CODE</button>
                </div>}
        </div>
    )
}

export default Home;