import { useState } from 'react'
import classes from './Login.module.css'

function Login() {


    const [login, setLogin] = useState('')
    const [password, setPassword] = useState('')

    const [labelLogin, setLabelLogin] = useState('')
    const [labelPassword, setLabelPassword] = useState('')


    const onSubmit = () => {
        fetch(`http://127.0.0.1:8000/login?login=${login}&password=${password}`)
        .then(res => res.json())
        .then(data => {
            console.log(data)
        })
    }

    const onSubmitReg = () => {
        fetch('http://127.0.0.1:8000/')
        .then(res => res.json())
        .then(data => {
            console.log(data)
        })
    }

    return(
        <div className={classes.page_login}>

            <div className="materialContainer">

                <div className="box">
                    <div className="title">LOGIN</div>
                    <div className="input">
                        <label htmlFor="name" className={labelLogin}>Username</label>
                        <input type="text" value={login} onBlur={() => setLabelLogin('')} onFocus={() => setLabelLogin('label_focus_login')} onChange={(e) => setLogin(e.target.value)} id="name" />
                        <span className="spin"></span>
                    </div>
                    <div className="input">
                        <label htmlFor="pass" className={labelPassword}>Password</label>
                        <input type="password" value={password} onBlur={() => setLabelPassword('')} onFocus={() => setLabelPassword('label_focus_password')} onChange={(e) => setPassword(e.target.value)} id="pass" />
                        <span className="spin"></span>
                    </div>
                    <div className="button login">
                        <button onClick={onSubmit}><span>GO</span> <i className="fa fa-check"></i></button>
                    </div>
                    <a href="" className="pass-forgot">Forgot your password?</a>
                </div>

                <div className="overbox">
                        <div className="material-button alt-2"><span className="shape"></span></div>

                        <div className="title">REGISTER</div>

                        <div className="input">
                            <label htmlFor="regname">Username</label>
                            <input type="text" name="regname" id="regname" />
                            <span className="spin"></span>
                        </div>

                        <div className="input">
                            <label htmlFor="regpass">Password</label>
                            <input type="password" name="regpass" id="regpass" />
                            <span className="spin"></span>
                        </div>

                        <div className="input">
                            <label htmlFor="reregpass">Repeat Password</label>
                            <input type="password" name="reregpass" id="reregpass" />
                            <span className="spin"></span>
                        </div>

                        <div className="button" id="test">
                            <button><span>NEXT</span></button>
                        </div>

                </div>

            </div>

        </div>
    )
}

export default Login