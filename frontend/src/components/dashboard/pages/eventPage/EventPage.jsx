import './eventPage.css';
import {useEffect, useState} from "react";
import httpClient from "../../../../httpClient";
import userEvent from "@testing-library/user-event";

const EventPage = (props) => {
    let [event, setEvent] = useState({})
    let name = event.event_name
    let datetime = event.datetime;
    let genre = event.genre;
    let description = event.description;
    let venueName = event.venue_name;
    let venueLocation = event.venue_location;
    let venuePostcode = event.venue_postcode;
    let venueCapacity = event.venue_capacity;

    let setOpen = props.setOpen;

    useEffect(() => {
        // Get event if not directed from home page
        if (event.length === undefined) {
            let eventID = window.location.href.split("/").slice(-1);
            httpClient.get(`${process.env.REACT_APP_ROUTE_URL}/event/${eventID}`)
                .then(response => {
                    setEvent(response)
                })
                .catch(error => {
                    console.log(error)
                    if (error.response && error.response.status === 401) {
                        alert(error.response.data.msg);
                    }
                });
        } else {
            setEvent(props.event);
        }
    }, [])

    return (
        <div className={'contentContainer'}>
            <h1 className={'dashboardTitle'}>{name}</h1>
            <div className={'eventDetails'}>
                <div>{description}</div>
                <br/>
                <div><b>Time:</b> {datetime}</div>
                <div><b>Genre:</b> {genre}</div>
                <div><b>Venue Name:</b> {venueName}</div>
                <div><b>Venue Location:</b> {venueLocation}</div>
                <div><b>Postcode:</b> {venuePostcode}</div>
                <div><b>Capacity:</b> {venueCapacity}</div>
            </div>
            <br/>
            <button onClick={() => {setOpen(true)}} className={'ticketsBtn'}>BUY TICKETS</button>
        </div>
    )
}

export default EventPage;