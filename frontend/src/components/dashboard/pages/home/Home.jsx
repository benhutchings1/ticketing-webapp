import './home.css';
import './homeMobile.css';

import {useEffect, useState} from "react";
import {useNavigate} from "react-router-dom";
import httpClient from "../../../../httpClient";
import {SearchBar, Event} from "../../elements";

const Home = (props) => {
    const user = props.user;
    const setUser = props.setUser;
    const [events, setEvents] = useState([]);
    const setCurrentEvent = props.setCurrentEvent;

    const navigate = useNavigate();

    // Once user is updated, check if valid
    useEffect(() => {
        if (user == null) {
            navigate("/")
        }
    }, [user])

    // Get list of events and add to array
    useEffect(() => {
        httpClient.get(`${process.env.REACT_APP_ROUTE_URL}/event/list`)
        .then(response => {
            setEvents(response)
        })
        .catch(error => {
            console.log(error);
            if (error.response && error.response.status === 401) {
                alert(error.response.data.msg);
                if (error.response.data.msg === "Token has been revoked" || error.response.data.msg === "Token has expired") {
                    setUser(null);
                }
            }
        });
    }, [])

    const eventsList = events.map((item, index) =>
        <Event key={`event${index}`}
               user={user}
               id={item.event_id}
               item={item}
               setCurrenteEvent={setCurrentEvent}
        />)

    return (
        <div className={'contentContainer'}>
            <SearchBar />

            <h1 className={'dashboardTitle'}>HOME</h1>
            <h3>EVENTS</h3>
            <div className={'eventsListContainer'}>
                {eventsList}
            </div>
        </div>
    )
}

export default Home;