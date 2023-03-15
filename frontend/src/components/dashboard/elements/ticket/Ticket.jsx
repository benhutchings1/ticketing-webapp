import './Ticket.css';
import Card from 'react-bootstrap/Card';
import {Button} from "react-bootstrap";
import {useNavigate} from "react-router-dom";
import httpClient from '../../../../httpClient';


const SocialCard = (props) => {
   
    function buyTickets() {
        httpClient.get('/addticket')
            .then(response => {
                let data = {
                    userID: props.user.user_id,
                    eventID: props.event.event_id,
                    ticketTypeID: 1,
                    token: response.key
                }
    
                httpClient.post("/addticket", data)
                    .then(response => {
                        console.log(response);
                    })
            })
            .catch(error => {
                console.log(error)
            });
    }

    return (
        <div className="card">
            <div className="card__title">{props.item.event_name}</div>
            <div className="card__body">
                <description description={props.item.description}/>
                <genre genre={props.item.genre} type="Home"/>
            </div>
            <Button onClick={() => {buyTickets()}} className={'ticketsBtn'}>BUY TICKETS</Button>
            

        </div>
    )
};

export default SocialCard;