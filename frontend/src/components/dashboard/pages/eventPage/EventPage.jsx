import './eventPage.css';

const EventPage = (props) => {
    let event = props.event;
    let name = event.event_name
    let datetime = event.datetime;
    let genre = event.genre;
    let description = event.description;
    let venueName = event.venue_name;
    let venueLocation = event.venue_location;
    let venuePostcode = event.venue_postcode;
    let venueCapacity = event.venue_capacity;

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
            <button className={'ticketsBtn'}>BUY TICKETS</button>
        </div>
    )
}

export default EventPage;