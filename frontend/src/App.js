import { Route, Routes } from 'react-router-dom';
import './App.css';
import Home from './pages/Home';
import Login from './pages/Login';
import Account from './pages/Account';
import Header from './components/Header/Header';

function App() {
  return (
    <div className="App">
      
      <Header />
 
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/account" element={<Account />} />
      </Routes>
    </div>
  );
}

export default App;
