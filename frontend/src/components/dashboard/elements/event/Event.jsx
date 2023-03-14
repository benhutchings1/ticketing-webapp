import Carousel from "react-multi-carousel";
import "react-multi-carousel/lib/styles.css";
import Card from 'react-bootstrap/Card';
import react, { Component } from "react";



export default function Event(){
    const responsive = {
        superLargeDesktop: {
          
          breakpoint: { max: 4000, min: 3000 },
          items: 5
        },
        desktop: {
          breakpoint: { max: 3000, min: 1024 },
          items: 3
        },
        tablet: {
          breakpoint: { max: 1024, min: 464 },
          items: 2
        },
        mobile: {
          breakpoint: { max: 464, min: 0 },
          items: 1
        }
      };
      
      render () {
        let eventcards = this.state.event.map(event => {
            return (
                <col sm="4">
                    <eventcard event={event} />
                </col>
            )
        })
        return
        <container fluid>
            <row>
                {eventcards}
            </row>
        </container>
      }
      
      class Card extends Component {
        constructor(){
            super();
        }
        render () {
        return (
            <div>  
                <Card style={{ width: '18rem' }}>
                    <Card.Img variant="top" src="holder.js/100px180" />
                    <Card.Body>
                    <Card.Title>{}Concert</Card.Title>
                    <Card.Text>
                        Generic discribtion of the concert type
                    </Card.Text>
                    <Button variant="primary">Go somewhere</Button>
                    </Card.Body>
                </Card>
          </div> 
        );
      }
      export default Card;
      
      
}
