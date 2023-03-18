import React, {useEffect, useState} from 'react';
import Card from 'react-bootstrap/Card';
import Button from "react-bootstrap/Button";
import httpClient from "../../../../httpClient";
import {getCookie, getUser} from "../../../../helpers";
//import Button from 'react-bootstrap/Button';
//import Card from 'react-bootstrap/Card';

const Ticket = (props) => {
    let setQRData = props.setQRData;
    let setQROpen = props.setQROpen;
    let id = props.id;
    let item = props.item;
    let name = item.event_name;
    let datetime = item.event_datetime;
    let venueName = item.venue_name;
    let venueLocation = item.venue_location;
    let venuePostcode = item.venue_postcode;
    let venueCapacity = item.venue_capacity;

    return (
        <div className={'eventCard'}>
            <Card style={{ width: '18rem' }}>
                <Card.Body>
                    <h3>{name}</h3>
                    <Card.Text>
                        <b>Time:</b> {datetime}
                    </Card.Text>
                    <Card.Text>
                        <b>Venue:</b> {venueName}
                    </Card.Text>
                    <Card.Text>
                        <b>Location:</b> {venueLocation}
                    </Card.Text>
                    <Card.Text>
                        <b>Postcode:</b> {venuePostcode}
                    </Card.Text>
                    <Card.Text>
                        <b>Capacity:</b> {venueCapacity}
                    </Card.Text>
                    <Button className={'eventButton'} onClick={() => {
                        const data = {
                            ticket_id: id
                        }

                        httpClient.post('https://192.168.0.159:5000/ticket/request_qr_data', data, {
                            headers: {
                                "Content-Type": "application/json",
                                "X-CSRF-TOKEN": getCookie("csrf_access_token"),
                            }
                        })
                        .then(response => {
                            let qrData = response.qr_data;
                            console.log(qrData);
                            setQRData(qrData);
                            setQROpen(true);
                        })
                        .catch(error => {
                            console.log(error);
                        });
                    }} variant="primary">VIEW QR CODE</Button>
                </Card.Body>
            </Card>
        </div>
    )
}

export default Ticket;