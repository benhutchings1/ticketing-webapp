import './search.css';

import {useEffect, useState} from "react";
import {useLocation, useNavigate} from "react-router-dom";
import {SearchBar, Event} from "../../elements";
import httpClient from "../../../../httpClient";
import {getCookie} from "../../../../helpers";

const SearchPage = (props) => {
    const user = props.user;
    const setUser = props.setUser;
    const [events, setEvents] = useState([]);
    const setCurrentEvent = props.setCurrentEvent;

    const navigate = useNavigate();
    
    let query = new URLSearchParams(useLocation().search);
    const searchValue = query.get("searchParams")

    const searchData = {
        "event_name" : searchValue
    }

    useEffect(() => {
        if (user == null) {
            navigate("/")
        }
    }, [user])


    useEffect(() => {
        httpClient.post(`${process.env.REACT_APP_ROUTE_URL}/event/search`, searchData, {
            headers: {
                "Content-Type": "application/json",
                "X-CSRF-TOKEN": getCookie("csrf_access_token"),
            }
        })
        .then(response => {
            setEvents(response)
        })
        .catch(error => {
            console.log(error);
            if (error.response && error.response.status === 401) {
                alert(error.response.data.msg);
                if (error.response.data.msg === "Token has been revoked") {
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

            <h1 className={'dashboardTitle'}>SEARCH RESULTS</h1>
            <h1 className={'searchHeader'}>Search value: {searchValue}</h1>
            <div className={'eventsListContainer'}>
                {eventsList}
            </div>
            
        </div>
    )

}

export default SearchPage;