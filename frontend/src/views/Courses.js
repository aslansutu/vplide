import React from 'react';
import { useNavigate } from "react-router-dom";


const Courses = () => {

	const SignInStyle = {
		color: "white",
		backgroundColor: "DimGray",
		borderWidth: "medium",
		borderColor: "#969696",
		borderRadius: "15px",
		textAlign: "center",
		padding: "25px",
		fontFamily: "Georgia"
	};

	const PopUpStyle = {
		position: "absolute",
		left: "50%",
		top: "20%",
		transform: "translateX(-50%)",
		height: "400px",
		borderWidth: "medium",
		borderStyle: "groove",
		borderColor: "#969696",
		borderRadius: "15px",
		padding: "25px",
		fontFamily: "Georgia"
	};

	const ButtonStyle = {
		position: "absolute",
		left: "50%",
		transform: "translateX(-50%)",
		color: "white",
		backgroundColor: "DimGray",
		borderWidth: "medium",
		borderStyle: "groove",
		borderColor: "#969696",
		borderRadius: "15px",
		padding: "15px",
		fontFamily: "Georgia"
	};


    let navigate = useNavigate(); 
    const routeChange = () =>{ 
    let path = `/`; 
    navigate(path);
    }

	return (
		<>
				<section style={PopUpStyle}>
					<h1 style={SignInStyle}>Select a Course</h1>
                        <br></br>
                        <button style={ButtonStyle} onClick={routeChange}>
                            CENG111
                        </button>
						<br></br>
                        <br></br>
                        <br></br>
						<button style={ButtonStyle} onClick={routeChange}>
                            CENG315
                        </button>
						<br></br>
                        <br></br>
                        <br></br>
						<button style={ButtonStyle} onClick={routeChange}>
                            CENG491
                        </button>
				</section>
		</>
	);
};

export default Courses;