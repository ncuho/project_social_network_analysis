import { useState } from 'react'
import classes from './Register.module.css'


function Register() {

    var zapros = "http://127.0.0.1:8000/"

    var heder = {
    'accept': 'application/vnd.api+json',
    'X-CSRFToken': ' 80nfXWtzFBx4Mv3zvYJHnrn8KFhJmQ1tfgVCvHmLRfjGGVymAmoiHgtMysy8PfYI',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': '*',
    'Access-Control-Allow-Methods': '*',};

    const [login, setLogin] = useState('')
    const [password, setPassword] = useState('')
    const [rep_password, setRepPassword] = useState('')


    const [labelLogin, setLabelLogin] = useState('')
    const [labelPassword, setLabelPassword] = useState('')


    const onSubmit = async () => {
        if (password == rep_password){
            fetch(zapros+"register?login=" + login + "&pas=" + password,
            {
                method: 'POST',
                headers: heder,
                credentials: 'include',
            }
            ).then(res => console.log(res.json().then(t => {
                if (t.data != 'вы не зарегистрировались'){ 
                    document.cookie = "session_id=" + t.session_id + "; path=/;" 
                    window.location.href = '/'
                }
                else setTimeout(3000)
            })));
        }
        
    }

    return(
        <div className={classes.page_register}>
            <div className="materialContainer">
                <div className="box">
                    <div className="material-button alt-2"><span className="shape"></span></div>
                    <div className="title">REGISTER</div>
                    <div className="input">
                        <label htmlFor="regname">Username</label>
                        <input type="text" name="regname" onBlur={() => setLabelLogin('')} onFocus={() => setLabelLogin('label_focus_login')} onChange={(e) => setLogin(e.target.value)} id="regname" />
                        <span className="spin"></span>
                    </div>
                    <div className="input">
                        <label htmlFor="regpass">Password</label>
                        <input type="password" name="regpass"  value={password} onBlur={() => setLabelPassword('')} onFocus={() => setLabelPassword('label_focus_password')} onChange={(e) => setPassword(e.target.value)} id="regpass" />
                        <span className="spin"></span>
                    </div>
                    <div className="input">
                        <label htmlFor="reregpass">Repeat Password</label>
                        <input type="password" name="reregpass"  value={rep_password} onBlur={() => setLabelPassword('')} onFocus={() => setLabelPassword('label_focus_password')} onChange={(e) => setRepPassword(e.target.value)} id="reregpass" />
                        <span className="spin"></span>
                    </div>
                    <div className="button" id="test">
                        <button onClick={onSubmit}><span>NEXT</span></button>
                    </div>
                </div>
            </div>

        </div>
    )
}

export default Register