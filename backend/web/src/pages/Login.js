import { useState } from "react";
import api from "../services/api";
import { useNavigate } from "react-router-dom";

export default function Login() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();

    const login = async () => {
        try {
            const res = await api.post("token/", {
                username,
                password,
            });

            localStorage.setItem("access", res.data.access);
            localStorage.setItem("refresh", res.data.refresh);
            navigate("/dashboard");
        }   
        catch (err){
            console.log(err.response?.data);
            alert("Login failed");
        }
    };

    return (
        <div>
            <h2>Login</h2>
            <input placeholder="Username" onChange={e => setUsername(e.target.value)} />
            <input type="password" placeholder="Password" onChange={e => setPassword(e.target.value)} />
            <button onClick={login}>Login</button>
        </div>
    );
}
