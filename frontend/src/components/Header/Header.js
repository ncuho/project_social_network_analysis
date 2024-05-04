import classes from './Header.module.css'
import Menu from '../Menu/Menu'


function Header() {
    return(
        <header className={classes.header}>
            <div className="container">
                <div className={classes.header_container}>
                    
                    <div className={classes.logo}>
                        Logo
                        {/* <img src="/logo.png" alt="Логотип" /> */}
                    </div>
                    
                    <Menu />
                </div>  
            </div>  
        </header>
    )
}

export default Header