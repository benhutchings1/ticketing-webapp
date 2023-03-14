import React, {useEffect, useState} from 'react';
import Card from 'react-bootstrap/Card';
//import Button from 'react-bootstrap/Button';
//import Card from 'react-bootstrap/Card';

const Ticket = (props) => {
    return (
        <div>
          <Card style={{ width: '18rem' }}>
            <Card.Body>
                <Card.Title>Concert Name</Card.Title>
                <Card.Subtitle>Concert </Card.Subtitle>
                <Card.Text>
                Some quick example text about the concert
                </Card.Text>
                {/*<Button variant="primary">Go somewhere</Button>*/}
            </Card.Body>
            </Card>
        </div>
    )
}

export default Ticket;