import './searchBar.css';
import './searchBarMobile.css';
import {Search} from "../../../../img";

const SearchBar = (props) => {
    return (
        <div className={'searchBarContainer'}>
            <img src={Search} className={'searchBarIcon'} />
            <input className={'searchBar'} placeholder={'SEARCH'} />
        </div>

    )
}

export default SearchBar;