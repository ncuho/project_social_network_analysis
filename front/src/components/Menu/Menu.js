import { Link } from 'react-router-dom'
import classes from './Menu.module.css'

function Menu() {
    return(
        <nav className={classes.menu}>
            <ul className={classes.menu_items}>
                <li className={classes.menu_item}>
                    <Link to="/" className={classes.menu_item_link}>Главная</Link>
                </li>
                <li className={classes.menu_item}>
                    <Link to="/login" className={classes.menu_item_link}>Вход</Link>
                </li>
                <li className={classes.menu_item}>
                    <Link to="/account" className={classes.menu_item_link}>Личный кабинет</Link>
                </li>
                <li className={classes.menu_item}>
                    <Link to="/register" className={classes.menu_item_link}>Регистрация</Link>
                </li>
            </ul>
        </nav>
    )
}

export default Menu