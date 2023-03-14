import './ticketModal.css';
import './ticketModalMobile.css';
import {useEffect, useState} from "react";
import httpClient from "../../../../httpClient";

const TicketModal = (props) => {
    let open = props.open;
    let setOpen = props.setOpen;
    let event = props.event;
    let user = props.user;
    let [count, setCount] = useState(1);

    const [displayStyle, setDisplayStyle] = useState("none");

    useEffect(() => {
        if (open) {
            setDisplayStyle("flex");
        } else {
            setDisplayStyle( "none");
        }
    }, [open]);

    function buyTickets() {
        httpClient.get('/addticket')
            .then(response => {
                let data = {
                    userID: user.user_id,
                    eventID: event.event_id,
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
        <div onClick={() => {setOpen(false)}} style={{display: displayStyle}} className='ticketModalContainer noSelect'>
            <div onClick={(e) => {e.stopPropagation();}} className='ticketModalBoxContainer'>
                <h2>Buy Tickets for {event.event_name}</h2>
                <div className={'counterContainer'}>
                    <button onClick={() => {
                        if (count > 1) {
                            setCount(count -= 1)
                        }
                    }} className={'counterBtn'}>
                        -
                    </button>
                    <div>
                        {count}
                    </div>
                    <button onClick={() => {
                        if (count < 4) {
                            setCount(count += 1)
                        }
                    }} className={'counterBtn'}>
                        +
                    </button>
                </div>
                <br/>
                <button onClick={() => {buyTickets()}} className={'ticketsBtn'}>BUY TICKETS</button>
            </div>
        </div>
    )
}

export default TicketModal;