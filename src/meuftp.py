try:
	from pyftpdlib.authorizers import DummyAuthorizer
	from pyftpdlib.handlers import FTPHandler
	from pyftpdlib.servers import FTPServer
except:
	print("\033[0;31mOps, você não tem o que é preciso para executar este programa.\033[0;0m")
	print("Para instalar as dependências, envie este comando no seu terminal: \033[1mpip install pyftpdlib==1.5.7\033[0m")
	input("PRESSIONE [ENTER] PARA SAIR... ")
	exit()

import logging
import socket
import os

permission: str = None
path: str = os.getcwd()
address: tuple[str, int] = (socket.gethostbyname(socket.gethostname()), 2005)

handler: FTPHandler
authorizer: DummyAuthorizer

logger = logging.getLogger("pyftpdlib")
logger.setLevel(logging.INFO)
fh = logging.FileHandler("meuftp.log")
fh.setFormatter(logging.Formatter("[%(asctime)s] %(message)s", "%Y-%m-%d %H:%M:%S"))
logger.addHandler(fh)

def ask_for_permission():

	global permission
	perm_input: str
	perm_name: str

	print("Selecione as permissões dos usuários que acessarão seus arquivos")
	print()
	print("\033[4mV\033[0mISUALIZADOR - Permite visualizar e baixar arquivos e diretórios.")
	print("\033[4mA\033[0mDICIONADOR - Todas as permissões anteriores + subir novos arquivos e diretórios.")
	print("\033[4mE\033[0mDITOR - Todas as permissões anteriores + editar, renomear e excluir arquivos e diretórios existentes.")
	print("A\033[4mD\033[0mINISTRADOR - Todas as permissões anteriores + editar os metadados dos arquivos.")

	while permission == None:

		perm_input = input("> ").upper()

		match perm_input:

			case "" | "V" | "VISUALIZADOR":
				permission = "elr"
				perm_name = "VISUALIZADOR"

			case "A" | "ADICIONADOR":
				permission = "elrmw"
				perm_name = "ADICIONADOR"

			case "E" | "EDITOR":
				permission = "elradfmw"
				perm_name = "EDITOR"

			case "D" | "ADMINISTRADOR":
				permission = "elradfmwMT"
				perm_name = "ADMINISTRADOR"

		if permission == None:
			print("\033[0;31mEsta permissão não é válida.\033[0m")

	print(f"Permissão selecionada: \033[1m{perm_name}\033[0m")

def init():

	global handler
	global authorizer
	global address
	global path
	global permission

	handler = FTPHandler
	authorizer = DummyAuthorizer()

	authorizer.add_anonymous(path, perm=permission)

	handler.authorizer = authorizer

	handler.log_prefix = "<%(remote_ip)s>"

	handler.on_file_received = lambda s, f: print(f'<x> subiu o arquivo \033[1m"{os.path.basename(f)}"\033[22m')
	handler.on_file_sent     = lambda s, f: print(f'<x> baixou o arquivo \033[1m"{os.path.basename(f)}"\033[22m')
	handler.on_connect       = lambda s: print("\033[0;33m<x> se conectou ao servidor\033[0m")
	handler.on_disconnect    = lambda s: print("\033[0;33m<x> se desconectou ao servidor\033[0m")

	handler.on_incomplete_file_sent     = lambda s, f: print(f"\033[0;33m<x> tentou baixar o arquivo \033[1m{os.path.basename(f)}\033[22m mas falhou\033[0m")
	handler.on_incomplete_file_received = lambda s, f: print(f"\033[0;33m<x> tentou subir o arquivo \033[1m{os.path.basename(f)}\033[22m mas falhou\033[0m")

	server = FTPServer(address, handler)

	# Limite de conexões
	server.max_cons = 10
	server.max_cons_per_ip = 5

	print(f"Diretório alvo: \033[1m\"{path}\"\033[22m")
	print(f"Endereço do servidor: \033[1m{address[0]}:{address[1]}\033[22m")
	print("Protocolo de transferência: File Transfer Protocol (FTP)")
	print()
	print(f"Servidor iniciado com URI de acesso \033[1m\"ftp://{address[0]}:{address[1]}/\"\033[22m")

	# Começar o servidor FTP
	server.serve_forever()


if __name__ == "__main__":
	print("Bem vindo ao MeuFTP!")
	ask_for_permission()
	print()
	init()