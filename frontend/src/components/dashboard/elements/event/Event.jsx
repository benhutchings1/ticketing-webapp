import './Event.css';

import Card from 'react-bootstrap/Card';
import Button from "react-bootstrap/Button";
import {useNavigate} from "react-router-dom";

const Event = (props) => {
    let user = props.user;
    let id = props.id;
    let item = props.item;
    let name = item.event_name
    let description = item.description;
    let setCurrentEvent = props.setCurrenteEvent;

    let navigate = useNavigate();

    return (
        <div className={'eventCard'}>
            <Card style={{ width: '18rem' }}>
                <Card.Body>
                    <h3>{name}</h3>
                    <Card.Text>
                        {description}
                    </Card.Text>
                    {user != null && user.role !== "management" ?
                        // Customer
                        <Button className={'eventButton'} onClick={() => {
                            setCurrentEvent(item)
                            navigate(`/event/${id}`)
                        }} variant="primary">VIEW EVENT</Button>
                    :
                        // Management
                        <Button className={'eventButton'} onClick={() => {
                            setCurrentEvent(item)
                            navigate(`/scanner`)
                        }} variant="primary">SCAN QR FOR EVENT</Button>
                    }

                </Card.Body>
            </Card>
        </div>
    );
}

export default Event;
