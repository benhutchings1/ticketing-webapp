import './ticketModal.css';
import './ticketModalMobile.css';
import {useEffect, useState} from "react";
import httpClient from "../../../../httpClient";
import {getCookie} from "../../../../helpers";
import {useNavigate} from "react-router-dom";

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

    let navigate = useNavigate();

    function buyTickets() {
        loading(true);
        httpClient.get(`/ticket/add`)
            .then(response => {
                let tickets = document.getElementById("ticketTypes");
                let ticketType = tickets.options[tickets.selectedIndex].text;

                let data = {
                    ticket_quantity: count,
                    event_id: event.event_id,
                    ticket_type: ticketType,
                    token: response.key
                }

                window.setTimeout(() => {
                    httpClient.post(`/ticket/add`, data, {
                        headers: {
                            "Content-Type": "application/json",
                            "X-CSRF-TOKEN": getCookie("csrf_access_token"),
                        }
                    })
                    .then(response => {
                        loading(false);
                        setOpen(false);
                        navigate("/account"); // tickets will then be shown on account page
                    })
                }, 500);
            })
            .catch(error => {
                console.log(error)
            });
    }

    // Prevent user from spamming the buy button
    function loading(bool) {
        if (bool) {
            document.querySelector(".ticketModalContainer").style.pointerEvents = "none";
        } else {
            setCount(1);
            document.querySelector(".ticketModalContainer").style.pointerEvents = "visiblePainted";
        }
    }

    return (
        <div onClick={() => {setOpen(false)}} style={{display: displayStyle}} className='modalContainer ticketModalContainer noSelect'>
            <div onClick={(e) => {e.stopPropagation();}} className='modalBoxContainer ticketModalBoxContainer'>
                <h2>Buy Tickets for {event.event_name}</h2>
                <div className='modalHeader'><b>Amount:</b></div>
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
                <div className='modalHeader'><b>Ticket Type:</b></div>
                <select id="ticketTypes">
                    <option value="standard">Standard</option>
                    <option value="deluxe">Deluxe</option>
                    <option value="vip">VIP</option>
                </select>
                <br/>
                <button onClick={() => {buyTickets()}} className={'ticketsBtn ticketBtnModal'}>BUY TICKETS</button>
            </div>
        </div>
    )
}

export default TicketModal;