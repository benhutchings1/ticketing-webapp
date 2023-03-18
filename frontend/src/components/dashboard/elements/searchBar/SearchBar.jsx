import './searchBar.css';
import './searchBarMobile.css';
import {useEffect, useState} from "react";
import { createSearchParams, useNavigate } from 'react-router-dom';
import {Search} from "../../../../img";

const SearchBar = (props) => {
    const [searchValue, setSearchValue] = useState("");

    const navigate = useNavigate();

    const searchEvents = (event) => {
        // checks if string only contains whitespaces
        if(searchValue.trim().length) {
            event.preventDefault();
            navigate({
                pathname: "/search",
                search: createSearchParams({
                    searchParams: searchValue
                }).toString()
            });
        }
    }

    //TODO: now that searchValue is the search parameter, search and create event list using that parameter

    return (
        <div>
            <form className='searchBarContainer' onSubmit={searchEvents}>
                <img src={Search} className={'searchBarIcon'} />
                <input
                type="text"
                className={'searchBar'} 
                placeholder={'SEARCH'}
                onChange={(e) => setSearchValue(e.target.value)}
                />
            </form>
        </div>

    )
}

export default SearchBar;