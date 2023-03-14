// import Carousel from "react-multi-carousel";
// import "react-multi-carousel/lib/styles.css";
import Card from 'react-bootstrap/Card';
import react, { Component } from "react";
import {Button} from "react-bootstrap";
import './Event.css';

const Event = (props) => {
    let name = props.name
    let datetime = props.datetime;
    let genre = props.genre;
    let description = props.description;
    let venueName = props.venueName;
    let venueLocation = props.venueLocation;
    let venuePostcode = props.venuePostcode;
    let venueCapacity = props.venueCapacity;

    return (
        <div className={'eventCard'}>
            <Card style={{ width: '18rem' }}>
                {/*<Card.Img variant="top" src="holder.js/100px180" />*/}
                <Card.Body>
                    <h3>{name}</h3>
                    <Card.Text>
                        {description}
                    </Card.Text>
                    {/*<Button className={'eventButton'} onClick={() => {navigate("/event/")}} variant="primary">Go somewhere</Button>*/}
                </Card.Body>
            </Card>
        </div>
    );
}

export default Event;
