import React, {useEffect, useState} from 'react';
import {Card, CardImg, CardText, CardBody, 
    CardTitle, CardSubtitle, Button} from 'reactstrap';
//import Button from 'react-bootstrap/Button';
//import Card from 'react-bootstrap/Card';

const Ticket = (props) => {
    return (
        <div>
          <Card style={{ width: '18rem' }}>
            <CardImg variant="top" src="holder.js/100px180" />
            <CardBody>
                <CardTitle>Concert Name</CardTitle>
                <CardSubtitle>Concert </CardSubtitle>
                <CardText>
                Some quick example text about the concert
                </CardText>
                <Button variant="primary">Go somewhere</Button>
            </CardBody>
            </Card>
        </div>
    )
}

export default Ticket;