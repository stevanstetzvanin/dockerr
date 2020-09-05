#Requisitos: 
Docker 

Tutorial:
1) Faça um clone deste repositorio git clone https://github.com/joaobrunonardon/dockerr.git
2) Entre na pasta dockerr cd dockerr
3) Edite o arquivo data.json com suas credenciais
4) Execute o comando docker run -it  -v $PWD/data.json:/usr/src/app/data.json joaobruno/docker:1.1
