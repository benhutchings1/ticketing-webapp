import {useEffect, useState} from "react";
import './Shop.css';
import {useNavigate} from "react-router-dom";
import {SearchBar, Ticket} from "../../elements";
import httpClient from "../../../../httpClient";


const Shop = (props) => {
    const user = props.user;
    const [events, setticket] = useState([]);
    
    const setCurrentEvent = props.setCurrentEvent;

    const navigate = useNavigate();

    // Once user is updated, check if valid
    useEffect(() => {
        if (user == null) {
            navigate("/")
        }
    }, [user])

    useEffect(() => {
        httpClient.get('/ticket_list')
        .then(response => {
            setticket(response)
        })
        .catch(error => {
            console.log(error)
            if (error.response && error.response.status === 401) {
                alert(error.response.data.msg);
            }
        });
    }, [])

    const ticketList = Ticket.map((item, index) =>
        <Ticket key={`Ticket${index}`}
               id={item.event_id}
               item={item}
               setCurrenteEvent={setCurrentEvent}
        />)

    //render () {
        return (
            <div className={'contentContainer'}>
                <SearchBar/>
                <h1 className={'dashboardTitle'}>SHOP</h1>
            </div>
        )
    //}
}

export default Shop;