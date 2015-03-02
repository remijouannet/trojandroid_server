if [[ -e "app.key" && -e "app.crt" ]]
then
	echo 'app.key and app.crt already exists'
	exit 1	
else
	#Generate a private key
	echo 'Generate a private key'	
	openssl genrsa -des3 -out app.key 1024

	#Generate a CSR
	echo 'Generate a CSR'
	openssl req -new -key app.key -out app.csr

	#Remove Passphrase from key
	echo 'Remove Passphrase from key'
	cp app.key app.key.org 
	openssl rsa -in app.key.org -out app.key

	#Generate self signed certificate
	echo 'Generate self signed certificate'
	openssl x509 -req -days 365 -in app.csr -signkey app.key -out app.crt

	#rm app.csr
fi
exit 0
