import React from 'react';
import Card from 'react-bootstrap/Card';
import Button from "react-bootstrap/Button";
import httpClient from "../../../../httpClient";
import {getCookie} from "../../../../helpers";

const ShopCard = (props) => {
    let id = props.id;
    let item = props.item;
    let name = item.event_name;
    let datetime = item.event_datetime;
    let description = item.description;
    let setCurrentEvent = props.setCurrenteEvent;
    let venueName = item.venue_name;
    let venueLocation = item.venue_location;
    let venuePostcode = item.venue_postcode;

    let setOpen = props.setOpen;

    return (
        <div className={'ShopCard'}>
          <Card>
            <Card.Body style={{ width: '18rem' }}>
              <h3>{name}</h3>
              <Card.Text>
              <h3>{name}</h3>
            <p>{venueName}</p>
            <p>{datetime}</p>
            <p>{description}</p>
            <p>{venueLocation} {venuePostcode}</p>
              </Card.Text>
              <Button onClick={() => {setOpen(true)}} className={'ticketsBtn'}>Buy Ticket</Button>
            </Card.Body>
          </Card>
        </div>
      )

}

