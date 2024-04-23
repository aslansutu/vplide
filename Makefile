start:
	sudo docker-compose up --build
	
end:
	sudo docker-compose down --rmi all -v

restart: end start