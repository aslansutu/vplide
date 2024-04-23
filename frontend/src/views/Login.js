import { useState, useEffect } from 'react';
import { useNavigate } from "react-router-dom";

const Login = () => {
	const navigate = useNavigate();

	const [user, setUser] = useState('');
	const [pwd, setPwd] = useState('');

	function handleUsername(e) {
		setUser(e.target.value);
	}

	function handlePassword(e) {
		setPwd(e.target.value);
	}

	const handleSubmit = async (e) => {
		e.preventDefault();
		window.location.href = "http://localhost:3000/";
		// fetch(`${process.env.REACT_APP_BASE_URL + '/api/login/'}`, {
		// 	method: "POST",
		// 	headers: {
		// 		Accept: "application/json",
		// 		"Content-Type": "application/json",
		// 	},
		// 	body: JSON.stringify({
		// 		"username": user,
		// 		"password": pwd,
		// 		"service": "tserv"
		// 	}),
		// }).then((response) => {
		// 	if (response.status !== 200) {
		// 		throw new Error(response.statusText);
		// 	}
		// 	return response.json();
		// }).then((response) => {
		// 	navigate("/")
		// 	// console.log(response);

		// }).catch((err) => {
		// 	console.log(err);
		// })
	};

	return (
		<div className="container">
			<div className="screen">
				<div className="screen__content">
					<div className="login">
						<div>
							<img src="/vplide_trans.png" alt="VPLIDE" className="vplideLogo2" />
						</div>
						<div>
							<form>
								<div className="login-input-group marginFromTop">
									<label className="login-input-underlined">
										<input type="text" onChange={handleUsername} required />
										<span className="login-input-label">Username</span>
									</label>
								</div>
								<div className="login-input-group">
									<label className="login-input-underlined">
										<input type="password" onChange={handlePassword} required />
										<span className="login-input-label">Password</span>
									</label>
								</div>
							</form>
							<button className="button login__submit" onClick={handleSubmit}>
								<span className="button__text">LOG IN NOW</span>
							</button>
						</div>

					</div>
				</div>
				<div className="screen__background">
					<span className="screen__background__shape screen__background__shape4"></span>
					<span className="screen__background__shape screen__background__shape3"></span>
					<span className="screen__background__shape screen__background__shape2"></span>
					<span className="screen__background__shape screen__background__shape1"></span>
				</div>
			</div>
		</div>
	);
};

export default Login;